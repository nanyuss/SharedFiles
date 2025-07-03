from pymongo import MongoClient
from pymongo.database import Database
from gridfs import GridFS
from io import BytesIO

from env import ENV
from .utils import convert_size

class MongoFiles:
    def __init__(self) -> None:
        self.clusters: dict[str, str] | None = ENV.CLUSTERS

        self.db_name = 'files'
        self.max_size: int = 512 * 1024 * 1024 # Limite máximo de 512MB
        self.client: MongoClient = None
        self.db: Database = None
        self.fs: GridFS = None

    def _get_cluster_size(self, db: Database) -> int:
        """Pega o tamanho do cluster em bytes."""
        stats = db.command('collStats', 'fs.chunks')
        return stats['size']
    
    def _check_cluster_space(self, db: Database, file_size: int) -> bool:
        """Verifica se o cluster tem espaço suficiente para o arquivo."""
        current_size = self._get_cluster_size(db)
        return current_size + file_size <= self.max_size
    
    def _switch_cluster(self, cluster_uri: str) -> None:
        """Troca o cluster atual."""
        self.client = MongoClient(cluster_uri)
        self.db = self.client[self.db_name]
        self.fs = GridFS(self.db)

    def _get_file_from_cluster(self, file_id: str, cluster_uri: str) -> dict | None:
        """Pega um arquivo do cluster."""
        client = MongoClient(cluster_uri)
        db = client[self.db_name]
        fs = GridFS(db)
        
        try:
            file = fs.find_one({'_id': file_id})
            if file:
                file_info = {
                    'file_id': str(file._id),
                    'filename': file.filename,
                    'mimetype': file.content_type,
                    'size': file.length,
                    'upload_date': file.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'url': file.url
                }
                return file_info, file
        except Exception:
            pass
        return None, None
    
    def _get_num_files(self, db: Database) -> int:
        """Pega o número de arquivos no cluster."""
        return db.fs.files.count_documents({})

    def _get_average_file_size(self, db: Database) -> str:
        """Pega a média do tamanho de arquivo no cluster."""
        num_files = self._get_num_files(db)
        total_size = self._get_cluster_size(db)
        return convert_size(total_size / num_files if num_files > 0 else 0.0)

    def _get_files_count_by_type(self, db: Database) -> dict[str, int]:
        """Pega o número de arquivos por tipo."""
        result = db.fs.files.aggregate([
            {'$group': {'_id': '$contentType', 'count': {'$sum': 1}}}
        ])
        return {item['_id']: item['count'] for item in result}
    
    def upload_file(self, file_id: str,  filename: str, content_type: str, file_data: bytes, base_url: str) -> dict:
        """Faz o upload de um arquivo para um cluster.
        
        Raises:
            Exception: Se todos os clusters estiverem cheios ou não tiverem espaço suficiente para o arquivo.
        """

        # Percorre todas as clusters
        for _, uri in self.clusters.items():
            self._switch_cluster(uri)

            if self._check_cluster_space(self.db, len(file_data)): # Verifica se ela tem espaço

                file_url = f'{base_url}/files/{file_id}'
                self.fs.put(file_data, _id=file_id, filename=filename, content_type=content_type, url=file_url)

                return {
                    'file_id': file_id,
                    'url': file_url
                } 
            
        raise Exception('Todas as clusters estão cheios ou não têm espaço suficiente para o arquivo')
    
    def get_file(self, file_id: str) -> tuple[dict, GridFS | None]:
        """Pega um arquivo de um cluster."""
        for _ ,uri in self.clusters.items():
            file_info, file = self._get_file_from_cluster(file_id, uri)
            if file_info and file:
                return file_info, BytesIO(file.read())
            
        raise ValueError('Arquivo não encontrado em nenhum cluster')
    
    def delete_file(self, file_id: str) -> bool:
        """Deleta um arquivo de um cluster."""
        for _, uri in self.clusters.items():
            self._switch_cluster(uri)
            try:
                self.fs.delete(file_id)
                return True
            except Exception:
                pass
        return False
    
    async def list_files(self) -> list[dict]:
        all_files = []
        for _, uri in self.clusters.items():
            client = MongoClient(uri)
            db = client[self.db_name]
            fs = GridFS(db)
            for file in fs.find():
                all_files.append({
                    'file_id': str(file._id),
                    'filename': file.filename,
                    'mimetype': file.content_type,
                    'size': file.length,
                    'upload_date': file.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'url': file.url 
                })
        return all_files
    
    async def get_clusters_status(self) -> list[dict]:
        """Pega o status de todos os clusters."""
        status = []
        for name, uri in self.clusters.items():
            self._switch_cluster(uri)
            cluster_size = self._get_cluster_size(self.db)
            status.append({
                'name': name,
                'total_size': convert_size(cluster_size),
                'storage': {
                    'avaliable': convert_size(self.max_size - cluster_size),
                    'used': convert_size(cluster_size),
                    'total': convert_size(self.max_size),
                },
                'average_file_size': self._get_average_file_size(self.db),
                'files_count': {
                    'by_type': self._get_files_count_by_type(self.db),
                    'total': self._get_num_files(self.db)
                },
                'status': 'OK' if self._check_cluster_space(self.db, 0) else 'FULL'
            })
                
        return status
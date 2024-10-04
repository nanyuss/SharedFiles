import pymongo
from pymongo import MongoClient
from pymongo.database import Database, Collection
from gridfs import GridFS
from uuid import uuid4
from decouple import config

import pytz
from datetime import datetime

class _BaseDB:
    def __init__(self, db_name: str, collection: str) -> None:
        client: MongoClient = MongoClient(config('MONGO_URI'))
        db: Database = client[db_name]
        self.database: Collection = db[collection]

class ClusterManagerFiles:
    def __init__(self, max_size: int = 512 * 1024 * 1024) -> None:
        self.uris: list[str] = [
            config('MONGO_URI_FILES_1'),
            config('MONGO_URI_FILES_2'),
            config('MONGO_URI_FILES_3'),
            config('MONGO_URI_FILES_4')
        ]

        self.clusters_names: list[str] = [
            'Fire',
            'Valley',
            'Star',
            'Nano'
        ]

        self.db_name = 'files'
        self.max_size: int = max_size
        self.client: MongoClient = None
        self.db: Database = None
        self.fs: GridFS = None

    def _get_cluster_size(self, db: Database) -> int:
        stats = db.command("collStats", "fs.chunks")
        return stats["size"]
    
    def _check_cluster_space(self, db: Database, file_size: int) -> bool:
        current_size = self._get_cluster_size(db)
        return current_size + file_size <= self.max_size
    
    def _switch_cluster(self, cluster_uri: str) -> None:
        self.client = MongoClient(cluster_uri)
        self.db = self.client[self.db_name]
        self.fs = GridFS(self.db)
    
    def _get_file_from_cluster(self, file_id: str, cluster_uri: str) -> dict | None:
        client = MongoClient(cluster_uri)
        db = client[self.db_name]
        fs = GridFS(db)
        
        try:
            file = fs.find_one({"_id": file_id})
            if file:
                file_info = {
                    'file_id': str(file._id),
                    'filename': file.filename,
                    'mimetype': file.content_type,
                    'size': file.length,
                    'upload_date': file.upload_date.strftime("%Y-%m-%d %H:%M:%S"),
                    'url': f'{config("DEFAULT_URL")}/api/files/{file._id}' 
                }
                return file_info, file
        except Exception as e:
            pass
        return None, None
    
    def _format_data_br(self, date: datetime) -> str:
        date_formated = date.astimezone(pytz.timezone('America/Sao_Paulo'))
        return date_formated.strftime('%d/%m/%Y %H:%M:%S')
    
    def _get_num_files(self, db: Database) -> int:
        return db.fs.files.count_documents({})

    def _get_average_file_size(self, db: Database) -> str:
        num_files = self._get_num_files(db)
        total_size = self._get_cluster_size(db)
        return self._convert_size(total_size / num_files if num_files > 0 else 0.0)

    def _get_files_count_by_type(self, db: Database) -> dict[str, int]:
        files_count_by_type = {}
        for file in db.fs.files.find():
            mime_type = file['contentType']
            if mime_type in files_count_by_type:
                files_count_by_type[mime_type] += 1
            else:
                files_count_by_type[mime_type] = 1
        return files_count_by_type
    
    def _convert_size(self, _bytes: int) -> str:
        return f"{_bytes // 1048576}MB"

    def upload_file(self, file_id: str,  filename: str, content_type: str, file_data: bytes) -> dict:
        for uri in self.uris:
            self._switch_cluster(uri)

            if self._check_cluster_space(self.db, len(file_data)):

                file_url = f'{config("DEFAULT_URL")}/api/files/{file_id}'
                self.fs.put(file_data, _id=file_id, filename=filename, content_type=content_type, url=file_url)

                return {
                    'file_id': file_id,
                    'url': file_url
                } 
            
        raise Exception("Todos os clusters estão cheios ou não têm espaço suficiente para o arquivo")
    
    def get_file(self, file_id: str) -> tuple[dict, GridFS | None]:
        for uri in self.uris:
            file_info, file = self._get_file_from_cluster(file_id, uri)
            if file_info and file:
                return file_info, file
            
        raise ValueError("Arquivo não encontrado em nenhum cluster")
    
    def delete_file(self, file_id: str) -> bool:
        for uri in self.uris:
            client = MongoClient(uri)
            db = client[self.db_name]
            fs = GridFS(db)
            try:
                fs.delete(file_id)
                return True
            except:
                pass
        return False
    
    async def get_all_files(self) -> list[dict]:
        all_files = []
        for uri in self.uris:
            client = MongoClient(uri)
            db = client[self.db_name]
            fs = GridFS(db)
            for file in fs.find():
                all_files.append({
                    'file_id': str(file._id),
                    'filename': file.filename,
                    'mimetype': file.content_type,
                    'size': file.length,
                    'upload_date': self._format_data_br(file.upload_date),
                    'url': f'{config("DEFAULT_URL")}/api/files/{file._id}' 
                })
        return all_files
    
    async def get_clusters_status(self) -> list[dict[str, object]]:
        clusters_status = []
        for i, uri, in enumerate(self.uris):
            try:
                client: MongoClient = MongoClient(uri)
                db: Database = client[self.db_name]

                used_size = self._get_cluster_size(db)
                avaliable_size = self.max_size - used_size

                clusters_status.append(
                    {
                        'name': self.clusters_names[i],
                        'total_size': self._convert_size(self.max_size),
                        'storage': {
                            'avaliable': self._convert_size(avaliable_size),
                            'used': self._convert_size(used_size),
                            'total': self._convert_size(self.max_size),
                        },
                        'avarage_file_size': self._get_average_file_size(db),
                        'files_count': {
                            'by_type': self._get_files_count_by_type(db),
                            'total': self._get_num_files(db)
                        },
                        'status': 'OK' if avaliable_size > 0 else 'FULL'
                    }
                )
            except Exception as e:
                print(f"Erro ao obter o status das clusters: {str(e)}")
                clusters_status.append({
                    'name': self.clusters_names[i],
                    'status': 'ERROR',
                    'error': str(e)
                })


        return clusters_status
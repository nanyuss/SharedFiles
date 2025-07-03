import sqlite3
from io import BytesIO
from pathlib import Path

from .utils import get_file_path, get_file_size

class SQLiteFiles:
    def __init__(self) -> None:
        self.upload_dir = Path('./uploads')
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        self.db_path = Path('./metadata.db')
        self.conn = sqlite3.connect(self.db_path)

        self.max_size = 100 * 1024 * 1024  # 100MB
    
    def upload_file(self, file_id: str, filename: str, content_type: str, file_data: bytes, base_url: str) -> dict:
        """Faz o upload de um arquivo enviando os metadados para o SQLite."""
        if len(file_data) > self.max_size:
            raise Exception('Arquivo excede o limite de tamanho permitido.')
        
        path = get_file_path(file_id)
        with open(path, 'wb') as f:
            f.write(file_data)

        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO File (id, filename, mimetype, size, url)
            VALUES (?, ?, ?, ?, ?)
        ''', (file_id, filename, content_type, get_file_size(path), f'{base_url}/files/{file_id}'))
        self.conn.commit()

        return {
            'file_id': file_id,
            'url': f'{base_url}/files/{file_id}'
        }
    
    def get_file(self, file_id: str) -> tuple[dict, object] | None:
        """Pega os metadados de um arquivo do SQLite."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM File WHERE id = ?', (file_id,))
        result = cursor.fetchone()
        if result:
            path = get_file_path(file_id)
            with open(path, 'rb') as file:
                content = file.read()
            return {
                'file_id': result[0],
                'filename': result[1],
                'mimetype': result[2],
                'size': result[3],
                'upload_date': result[4],
                'url': result[5]
            }, BytesIO(content)
        return None
    
    def delete_file(self, file_id: str) -> bool:
        """Deleta um arquivo do SQLite."""
        file = self.get_file(file_id)
        if not file:
            return False
        
        try:
            path = get_file_path(file_id)
            path.unlink()
        except FileNotFoundError:
            pass

        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM File WHERE id = ?', (file_id,))
        self.conn.commit()
        return True
    
    async def list_files(self) -> list[dict]:
        """Lista todos os arquivos do SQLite"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM File')
        result = cursor.fetchall()
        return [{
            'file_id': row[0],
            'filename': row[1],
            'mimetype': row[2],
            'size': row[3],
            'upload_date': row[4],
            'url': row[5]
        } for row in result]
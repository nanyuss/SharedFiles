import os
import sys
import sqlite3
import pymongo

from env import ENV, _is_valid_uri
from .mongo import MongoFiles
from .sqlite import SQLiteFiles

class DatabaseClient:
    def __init__(self) -> None:
        self._mongo_uri: str = ENV.MONGO_URI
        self._sqlite_path: str = 'metadata.db'
        self.db: pymongo.MongoClient | sqlite3.Connection = None
        self.db_type: str = 'SQLite'
        self.files: MongoFiles | SQLiteFiles = None

        self._connect() # Realiza a conexão automaticamente ao instanciar
    
    def _connect(self):
        """Conecta ao banco de dados."""
        if _is_valid_uri(self._mongo_uri):
            if not ENV.CLUSTERS:
                print('É nescessário ter no mínimo 1 cluster para usar o armazenamento remoto.')
                sys.exit(1)

            self.db = pymongo.MongoClient(self._mongo_uri)
            self.db_type = 'Mongo'
            self.files = MongoFiles()
            print('Conectado ao MongoDB. O armazenamento será remoto')
        else:
            if not os.path.exists(self._sqlite_path):
                # Executa o script de criação do banco local, se necessário
                with open('init.sql') as f:
                    script = f.read()
                with sqlite3.connect(self._sqlite_path) as conn:
                    conn.executescript(script)

            self.db = sqlite3.connect(self._sqlite_path)
            self.files = SQLiteFiles()
            print('Conectado ao SQLite. O armazenamento será local')
import sqlite3
from abc import ABC, abstractmethod

SQL_TABELA_ARQUIVOS_PROCESSADOS = """
CREATE TABLE IF NOT EXISTS ArquivoProcessado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    modelo_processamento TEXT NOT NULL
);
"""

SQL_TABELA_TOKENS = """
CREATE TABLE IF NOT EXISTS Token (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor_token TEXT NOT NULL UNIQUE,
    quantidade INTEGER NOT NULL,
    formato TEXT,
    data_criacao TEXT NOT NULL
);
"""

class DatabaseABS(ABC):
    _db_instance = None
    
    def __init__(self, modo_teste:bool):
        self.__modo_teste = modo_teste
        if DatabaseABS._db_instance is None:
            if self.__modo_teste:
                DatabaseABS._db_instance = sqlite3.connect(":memory:")
            else:
                DatabaseABS._db_instance = sqlite3.connect("modulos/database.db")
            DatabaseABS._db_instance.execute("PRAGMA journal_mode=WAL")  
        self.__db = DatabaseABS._db_instance
        self.__criar_tabelas()
    
    @property
    def db(self):
        return self.__db
    
    def __criar_tabelas(self) -> None:
        cursor = self.__db.cursor()
        cursor.execute(SQL_TABELA_ARQUIVOS_PROCESSADOS)
        cursor.execute(SQL_TABELA_TOKENS)
        cursor.close()

        

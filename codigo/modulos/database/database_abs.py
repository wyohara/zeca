import sqlite3
from abc import ABC, abstractmethod

SQL_TABELA_ARQUIVOS_PROCESSADOS = """
CREATE TABLE IF NOT EXISTS ArquivoProcessado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    modelo_processamento TEXT NOT NULL,
    UNIQUE(nome, modelo_processamento)
);
"""

SQL_TABELA_TOKENS = """
CREATE TABLE IF NOT EXISTS Token (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor_token TEXT NOT NULL UNIQUE,
    quantidade INTEGER NOT NULL,
    token_fixo BOOLEAN DEFAULT FALSE
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
                DatabaseABS._db_instance = sqlite3.connect("modulos/database/database.db")
                
        DatabaseABS._db_instance.execute("PRAGMA journal_mode=WAL") 
        self.__db = DatabaseABS._db_instance

        
        cursor = self.__db.cursor()
        cursor.execute(SQL_TABELA_ARQUIVOS_PROCESSADOS)
        cursor.execute(SQL_TABELA_TOKENS)
        cursor.close()

    @property
    def fechar_db(self):
        if self.__db is not None:
            self.__db.close()
            self.__db = None
            DatabaseABS._db_instance = None
            return True
        return False
    
    @property
    def db(self):
        return self.__db

from dataclasses import dataclass
from typing import Final
import os

@dataclass(frozen=True)   
class ModeloProcessamento:
    TRIE: Final[str] = 'trie'
    BAG:Final[str] = 'bag'

@dataclass(frozen=True)   
class FormatoTexto:
    HEX: Final[str] = 'hex'
    UTF8:Final[str] = 'utf-8'

@dataclass(frozen=True)   
class TokensEspeciais:
    UNKNOWN: Final[str] = '[unk]'



@dataclass(frozen=True)
class ConstanteTokenizador:
    # Constantes tipadas como Final
    APP_NAME: Final[str] = "zeca"
    VERSION: Final[str] = "0.1a"

    FORMATO_TEXTO: Final = FormatoTexto
    MODELO_PROCESSAMENTO:Final = ModeloProcessamento
    TOKENS_ESPECIAIS: Final = TokensEspeciais
    
    # Constantes de ambiente
    @property
    def API_KEY(self) -> str:
        #return os.getenv("API_KEY", "")
        return None
        

#Criando o Singleton
CONST_TOKENIZADOR = ConstanteTokenizador()
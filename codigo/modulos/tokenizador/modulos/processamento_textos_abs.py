from typing import Literal
from abc import ABC, abstractmethod
from pathlib import Path

from modulos.tokenizador.modulos.ferramentas_tokenizador import FerramentasTokenizador
from modulos.database.db_arquivos_textos import DatabaseArquivosTextos, ArquivoTextoObject
from modulos.database.db_tokens import DatabaseTokens,TokenObject
from modulos.constantes.constante_tokenizador import CONST_TOKENIZADOR

class ProcessamentoDeTextoABS(ABC):
    def __init__(self, modo_teste:bool):
        """
        Classe abstrata que controla os passos paralelos da tokenização
        - leitura dos corpus de texto
        - controle dos textos lidos
        - salvamento do token no banco de dados
        """
        self._db_textos = DatabaseArquivosTextos(modo_teste=modo_teste)
        self._db_tokens = DatabaseTokens(modo_teste=modo_teste)
        self._ferramentas = FerramentasTokenizador()
        self.__dataset = Path(__file__).parent / "dataset"
        self._modelo_processamento = ""


    def processar_dataset_textos(self, formato: str, status:bool):
        '''
        Método que carrega e processa os arquivos de texto
            Args:
                - formato: formato do token, são aceitos 'utf-8'(unicode) e 'hex' (hexadecimal)
                - status: exibe informações do processamento]

            Returns:
                True: o processamento ocorreu sem problemas

            Raises:
                ValueError: formato diferente de hex ou utf-8

        '''
        if formato not in CONST_TOKENIZADOR.FORMATO_TEXTO.LISTA:
            raise ValueError
        
        #verifica se o texto do path de dataset já foi processado
        for caminho, nome_texto in self.__get_lista_textos():
                if not self.__is_texto_processado(nome_texto, self._modelo_processamento):
                    if status:
                        print(f"> [{self._modelo_processamento}] - Processando: {nome_texto} - {caminho}")
                    
                    arq = open(caminho, "r", encoding="utf-8")
                    texto = arq.read()
                    arq.close()                    
                    lista_tokens = self._recortar_tokens(formato=formato, texto=texto)

                    #salvando os dados
                    self._db_tokens.inserir_tokens(lista_tokens=lista_tokens)
                    self._db_textos.set_arquivo_processado(ArquivoTextoObject(0,nome_texto,'',self._modelo_processamento))
        return True
    
    def __get_lista_textos(self)->list[(str, str)]:
        '''
        Método que carrega a lista de texto do dataset
        return:
            list[(str, str)]: contendo o caminho completo e o nome do arquivo
        '''
        try:
            dataset = []
            for caminho in self.__dataset.iterdir():
                if caminho.is_file():
                    dataset.append((caminho, caminho.name))
            return dataset
        except FileNotFoundError:
            return []

    @abstractmethod
    def _recortar_tokens(self, formato, texto) -> list[TokenObject]:
         """
         Método abstrato que realiza os recortes de tokens, ele é implementado em cada algoritmo de tokenização
         """
         pass
    
    def __is_texto_processado(self, name, modelo_processamento) -> bool:
        #Verifica se o texto já foi processado para o numero de bytes definidos
        texto = self._db_textos.get_texto_processado(name, modelo_processamento)
        if texto is None:
            return False
        else:
            return True
from typing import Literal
from abc import ABC, abstractmethod
from pathlib import Path

from modulos.tokenizador.ferramentas_tokenizador import FerramentasTokenizador
from modulos.database.db_arquivos_textos import DatabaseArquivosTextos, ArquivoTextoObject
from modulos.database.db_tokens import DatabaseTokens,TokenObject

class ProcessamentoDeTextoABS(ABC):
    def __init__(self, modo_teste:bool):
        """
        Classe abstrata que controla os passos paralelos da tokenização
        - leitura dos corpus de texto
        - controle dos textos lidos
        - salvamento do token no banco de dados
        """
        self.__db_textos = DatabaseArquivosTextos()
        self.__db_token = DatabaseTokens()
        self._ferramentas = FerramentasTokenizador()
        self.__dataset = Path(__file__).parent / "dataset"
        self._modelo_processamento = ""
        self.__modo_teste = modo_teste

    def processar_dataset_textos(self, formato: str, status):
        '''
        Método principal que manipula os textos, ele é chamado externamente
        '''
        #verifica se o texto do path de dataset já foi processado
        for caminho, nome_texto in self.__get_lista_textos():
                if not self.__is_texto_processado(nome_texto, self._modelo_processamento):
                    if status:
                        print(f"> [{self._modelo_processamento}] - Processando: {nome_texto} - {caminho}")
                    
                    arq = open(caminho, "r", encoding="utf-8")
                    texto = arq.read()
                    arq.close()                    
                    lista_tokens = self._recortar_tokens(formato, texto)
                    self.__db_token.inserir_tokens(token_list=lista_tokens)
                    self.__marcar_texto_como_processado(nome_arquivo=nome_texto, descricao ='', modelo_processamento=self._modelo_processamento)
    
    def __get_lista_textos(self):
        # Retorna a lista de textos processados no formato [caminho, nome_arquivo]
        dataset = []
        for arq in self.__dataset.iterdir():
            if arq.is_file():
                dataset.append([arq, arq.name])
        return dataset
    
    @abstractmethod
    def _recortar_tokens(self, formato, texto) -> list[TokenObject]:
         """
         Método abstrato que realiza os recortes de tokens, ele é implementado em cada algoritmo de tokenização
         """
         pass
    
    def __is_texto_processado(self, name, modelo_processamento) -> bool:
        #Verifica se o texto já foi processado para o numero de bytes definidos
        texto = self.__db_textos.get_texto_processado(name, modelo_processamento)
        if texto is None:
            return False
        else:
            return True
    
    def __marcar_texto_como_processado(self, nome_arquivo:str, descricao, modelo_processamento):
        # cria o objeto de manipulação de texto e verifica, se existir atualiza, senão salva
        arq_texto = ArquivoTextoObject(nome=nome_arquivo, descricao=descricao, modelo_processamento=modelo_processamento)
        
        texto = self.__db_textos.get_texto_processado(nome_arquivo, self._modelo_processamento)
        if texto is None:
            self.__db_textos.set_arquivo_processado(arq_texto)
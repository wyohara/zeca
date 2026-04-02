from datetime import date
import sqlite3
import json
from modulos.database.database_abs import DatabaseABS
from modulos.constantes.constante_tokenizador import ConstanteTokenizador

class ArquivoTextoObject():
    def __init__(self, id=0, nome='', descricao='',  modelo_processamento=''):
        '''
        Classe que controla a database de arquivos processados para gerar tokens
            Args:
                modo_teste: define se o banco de dados será no modo teste (em memória)
        '''
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.modelo_processamento = modelo_processamento
    
    def __str__(self):
        return f"Arquivo de texto do tipo ArquivoTextoObject\n\t>id {self.id} - '{self.nome}' e modelo '{self.modelo_processamento}'"
    
    def validar_nome(self):
        try:
            return len(self.nome) > 0 and isinstance(self.nome, str)
        except Exception:
            return False
    
    def validar_processamento(self):
        return self.modelo_processamento in ConstanteTokenizador.MODELO_PROCESSAMENTO.LISTA


class DatabaseArquivosTextos():
    def __init__(self, modo_teste=False):
        self.__pasta_json = 'modulos/arquivo_dados/temp/arquivos_processados.json'
        self.__arquivos = {}
        # carregando os arquivos se existir
        try:
            with open(self.__pasta_json, 'r') as f:
                self.__arquivos = json.load(f)
        except FileNotFoundError:
            self.__arquivos = {}
    
    def salvar_json(self, dados:dict):
         #salvando a árvore em dicionário minificado
        json_minificado = json.dumps(dados, separators=(',', ':'))
        with open(self.__pasta_json, 'w') as f:
            f.write(json_minificado)

    def get_lista_nomes_arquivos_processados(self, modelo_processamento='')->list[str]:
        '''
        Método que retorna uma lista de arquivos processados
        Args:
            modelo_processamento: modelo usado para criar tokens
        Return
            list[str]: lista dos nomes dos textos
        '''
        if modelo_processamento not in ConstanteTokenizador.MODELO_PROCESSAMENTO.LISTA:
            raise ValueError

        nomes = []
        for arquivo in self.__arquivos.keys():
            nomes.append(arquivo)
    
    def set_arquivo_processado(self, arq_texto:ArquivoTextoObject) -> int:
        '''
        Insere um arquivo de texto no banco de dados de arquivos processados.
            Args:
                arq_texto (ArquivoTextoObject): Objeto contendo os dados do arquivo a ser inserido.
                    O objeto deve conter os atributos:
                    - nome: Nome do arquivo
                    - descricao: Descrição do conteúdo
                    - modelo_processamento: Modelo utilizado no processamento
            
            Returns:
                Optional[int]: ID do registro inserido no banco de dados em caso de sucesso.
                None: se houver violação de integridade.
            
            Raises:
                sqlite3.IntegrityError: Se ocorrer um erro de banco de dados relacionado a integridade.
                ValueError: Se ocorrer um erro de integridade no objeto
        '''
         # caso insira um arquivo com id ocorre erro de integridade
        if arq_texto.id >0:
            raise ValueError
        
        # validando os campos de nome e arquivo processado
        if not (arq_texto.validar_nome() and arq_texto.validar_processamento()):
            raise ValueError
        
        if arq_texto.nome not in self.__arquivos.keys():
            self.__arquivos[arq_texto.nome] = {'descricao': arq_texto.descricao, 'modelo_processamento': arq_texto.modelo_processamento}
        
        self.salvar_json(self.__arquivos)
        return True
        
    def get_texto_processado(self, nome:str, modelo_processamento:str) -> ArquivoTextoObject:
        '''
        Busca um arquivo de texto processado pelo nome do arquivo e método de processamento.
            Args:
                nome: Nome do arquivo
                modelo_processamento: Modelo utilizado no processamento
            
            Returns:
                Optional[ArquivoTextoObject]: Objeto contendo os dados do arquivo de texto
                None: se houver violação de integridade ou nenhum resultado.
            
            Raises:
                sqlite3.IntegrityError: Se ocorrer um erro de banco de dados relacionado a integridade.
        '''
        
        try:
            arq = self.__arquivos[nome]
            if arq['modelo_processamento'] == modelo_processamento:
                return ArquivoTextoObject(nome=nome, descricao=arq['descricao'], modelo_processamento=arq['modelo_processamento'])
            else:
                raise ValueError
        except KeyError:
            return None
        

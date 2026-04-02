from datetime import date
import sqlite3
import json
from modulos.database.database_abs import DatabaseABS
from modulos.constantes.constante_tokenizador import ConstanteTokenizador
from modulos.tokenizador.modulos.ferramentas_tokenizador import FerramentasTokenizador as ft


class TokenObject():
    def __init__(self, id=0, valor_token='', quantidade=0,token_fixo=0):
        self.id=id
        self.valor_token=valor_token
        self.quantidade=quantidade
        self.token_fixo=token_fixo
    
    def __str__(self):
        return f"Arquivo de tokens tipo TokenObject\n\t>id {self.id} - '{self.valor_token}', modelo '{self.quantidade}'"
    
    def get_tamanho_token(self):
        return len(self.valor_token)
    
    def validar_valor_token(self):
        return len(self.valor_token)>0 and isinstance(self.valor_token, str)
    
    def validar_quantidade(self):        
        return self.quantidade>0 and isinstance(self.quantidade, int)


class DatabaseTokens():
    def __init__(self, modo_teste=False):
        '''
        Classe que controla a database de tokens
            Args:
                modo_teste: define se o banco de dados será no modo teste (em memória)
        '''
        self.__pasta_json = 'modulos/arquivo_dados/temp/tokens.json'
        self.__tokens = {}
        try:
            self.__contador = self.__tokens['contador']
        except KeyError:
            self.__contador = self.__tokens['contador']=0
        # carregando os arquivos se existir
        try:
            with open(self.__pasta_json, 'r') as f:
                self.__tokens = json.load(f)
        except FileNotFoundError:
            self.__tokens = {}
            self.__definir_tokens_fixos()
        
    def salvar_json(self, dados:dict):
         #salvando a árvore em dicionário minificado
        json_minificado = json.dumps(dados, separators=(',', ':'))
        with open(self.__pasta_json, 'w') as f:
            f.write(json_minificado)
    
    def __definir_tokens_fixos(self)->int:
        '''
        Método que cria os tokens fixos obrigatórios
        '''
        TOKENS = [',', '?', '!', '{', '}', '[', ']', '(', ')', ';', '_', '/', '|', '@', '#', '\'', '’', '"', '”', '-', '—', '...', '.',# Originais (sem duplicar com os que vêm depois)
                  'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',# Letras minúsculas
                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',# Letras maiúsculas
                  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                  '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',# Números                  
                  '+', '-', '*', '/', '%', '**', '//', # Operadores aritméticos
                  '==', '!=', '<', '>', '<=', '>=',# Operadores de comparação
                  'and', 'or', 'not',# Operadores lógicos
                  '=', '+=', '-=', '*=', '/=', '%=', '**=', '//=',# Operadores de atribuição
                  '&', '|', '^', '~', '<<', '>>',# Operadores bitwise
                  ':', ';', '@', '$', '`', ' ',# Símbolos e pontuação (apenas os que não estão nos originais)
                  '->', ':='# Outros operadores
                  '\n', ' ', '\t'# Espaçadores
                ]
        
        self.__tokens['tokens_fixos']={}
        fixo = self.__tokens['tokens_fixos']

        for tk in TOKENS:
            self.__contador+=1
            fixo[ft.texto_para_hex(tk)]={'quantidade':1, 'token_fixo':1, 'id':self.__contador}
        
        self.salvar_json(self.__tokens)
    
    def get_tokens_fixos(self,)-> list[TokenObject]:
        '''
        Recupera uma lista de tokens fixos do banco de dados
            Args:
            
            Returns:
                list[TokenObject]: lista de tokens
                None: se houver violação de integridade.
                -1: se formato inválido
            
            Raises:
                sqlite3.IntegrityError: Se ocorrer um erro de banco de dados relacionado a integridade.
                valueError: formato ou quantidade inválidos
        '''        

        tokens = []
        for tk in self.__tokens['tokens_fixos'].keys():
            tk_fixo = self.__tokens['tokens_fixos'][tk]
            tokens.append(TokenObject(id=tk_fixo['id'],valor_token=tk, quantidade=tk_fixo['quantidade'], token_fixo=tk_fixo['token_fixo']))
        return tokens
    

    def get_tokenObjects(self, quantidade=10000)-> list[TokenObject]:
        '''
        Recupera uma lista de tokens do banco de dados
            Args:
                quantidade: tamanho do bloco de tokens recuperado
            
            Returns:
                list[TokenObject]: lista de tokens
                None: se houver violação de integridade.
                -1: se formato inválido
            
            Raises:
                sqlite3.IntegrityError: Se ocorrer um erro de banco de dados relacionado a integridade.
                valueError: formato ou quantidade inválidos
        '''        
        try:
            resultado_parcial = []
            for chave, valor in self.__tokens['tokens'].items():
                resultado_parcial.append((chave, valor['quantidade'], valor['token_fixo'], valor['id']))
            resultado_parcial =  sorted(resultado_parcial, key=lambda x: x[1], reverse=True)

            resultado =[]
            for i in range(quantidade):
                r = resultado_parcial[i]
                resultado.append(TokenObject(valor_token=r[0], quantidade=r[1], token_fixo=r[2], id=r[3]))
            return resultado
        except KeyError:
            return []
    
    def get_lista_valores(self)->list[str]:
        '''
        Método que retorna uma lista de tokens do banco de dados ordenados do maior para o menor por formato

        Params:
        
        Return:
            list[str]: lista de tokens ordenados do maior para o menor
        '''
        tokens = []
        tokens.extend(list(self.__tokens['tokens_fixos'].keys()))
        tokens.extend(list(self.__tokens['tokens'].keys()))
        return tokens

    
    def get_token(self, valor_token:str)->TokenObject:
        '''
        Recupera uma lista de tokens do banco de dados pelo valor do token
            Args:
                valor_token: valor do token
            
            Returns:
                list[TokenObject]: lista de tokens
                None: se houver violação de integridade.
                -1: se formato inválido
            
            Raises:
                sqlite3.IntegrityError: Se ocorrer um erro de banco de dados relacionado a integridade.
                valueError: formato ou quantidade inválidos
        '''

        if valor_token in self.__tokens['tokens_fixos'].keys():
            tk = self.__tokens['tokens_fixos'][valor_token]
            return(TokenObject(valor_token=valor_token, 
                               quantidade=tk['quantidade'],
                               token_fixo=tk['token_fixo'],
                               id=tk['id']
                               ))
        if valor_token in self.__tokens['tokens'].keys():
            tk = self.__tokens['tokens'][valor_token]
            return(TokenObject(valor_token=valor_token, 
                               quantidade=tk['quantidade'],
                               token_fixo=tk['token_fixo'],
                               id=tk['id']
                               ))
        return None


    def inserir_tokens(self, lista_tokens:list[TokenObject]):
        '''
        Insere uma lista de tokens no banco de dados de arquivos processados.
            Args:
                token_list (list[TokenObject]): lista de Objetos tokens
                    O objeto deve conter os atributos:
                    - valor: Valor do token
                    - quantidade: número de ocorrencias
                    - formato: formato do token ('utf-8' ou 'hex')
                    - data_criacao: data de criação
                bloco: tamanho do bloco inserido no banco de dados. Evita sobrecarregar a memória
            
            Returns:
                Optional[int]: ID do registro inserido no banco de dados em caso de sucesso.
                None: se houver violação de integridade.
            
            Raises:
                sqlite3.IntegrityError: Se ocorrer um erro de banco de dados relacionado a integridade.
                TypeError: Se ocorrer a informação não estiver em uma lista.
                ValueError: Erro de integridade nos objetos
        '''
        self.__tokens['tokens']={}
        tk_opcional = self.__tokens['tokens']

        for tk in lista_tokens:
            self.__contador +=1
            chave = (tk.valor_token)
            if tk.valor_token in tk_opcional.keys():      
                tk_opcional[chave]['quantidade'] += tk.quantidade
            else:
                tk_opcional[chave] = {'quantidade':tk.quantidade, 'token_fixo':tk.token_fixo, 'id':self.__contador}
        
        self.salvar_json(self.__tokens)
        return True        

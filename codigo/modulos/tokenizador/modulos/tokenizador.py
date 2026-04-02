from modulos.database.db_tokens import DatabaseTokens, TokenObject
from modulos.tokenizador.modulos.ferramentas_tokenizador import FerramentasTokenizador as ft
from modulos.constantes.constante_tokenizador import CONST_TOKENIZADOR

class Tokenizador():
    def __init__(self, quantidade:int):
        self.__tokens = {}
        self.__rev_tokens = {}
        self.__maior_token=0
        self.__db = DatabaseTokens()

        if quantidade<0: raise ValueError

        #carregando o tokenizador
        self.__montar_tokens(quantidade=quantidade)
    
    @property
    def tamanho_tokenizador(self):
        return len(self.__tokens.keys())
    
    @property
    def get_lista_tokens(self):
        return self.__tokens


    def __montar_tokens(self,  quantidade:int):
        '''
        Método que monta as listas usadas para criar e defazer tokens
        Params:
            formato: formato dos tokens usados. Pode ser hex ou utf-8
            quantidade: total de tokens usados, composto de tokens fixos e variaveis
        '''
        #recuperanto os tokens fixos e opcionais
        tokens = self.__db.get_tokens_fixos()
        quantidade -= len(tokens)
        tokens_opcionais = []

        print(quantidade)

        if quantidade>0:
            tokens_opcionais = self.__db.get_tokenObjects(quantidade=quantidade)
            tokens.extend(tokens_opcionais)
        
        for tk in tokens:
            # recupera o maior token para fazer uma busca gulosa
            if self.__maior_token<len(tk.valor_token):
                self.__maior_token = len(tk.valor_token)
            
            # salva o dicionário de tokens e o dicionário reverso
            self.__tokens[tk.valor_token] = tk.id
            self.__rev_tokens[tk.id] =  ft.hex_para_texto(tk.valor_token)

    def transformar_texto_em_tokens(self, texto:str, status=False):
        resultado = []
        nao_achou = True
        while len(texto)>0:
            for i in range(int(self.__maior_token/2),0,-1):
                if i<=len(texto):
                    bloco = ft.texto_para_hex(texto[:i])
                    if status:
                        print(texto[:i], texto)
                    if bloco in self.__tokens.keys():
                        resultado.append(self.__tokens[bloco])
                        texto = texto[i:]
                        nao_achou = False
                        break
            if nao_achou:
                resultado.append('[unk]')
                texto = texto[i:]
        return resultado
    
    def transformar_tokens_em_texto(self, texto_tokenizado:list[str], hexadecimal=False, concatenar=False):
        resultado = []
        print(self.__rev_tokens)
        for tk in texto_tokenizado:
            if tk in self.__rev_tokens.keys():
                if hexadecimal:
                    resultado.append(self.__rev_tokens[tk])
                else:
                    resultado.append(ft.hex_para_texto(self.__rev_tokens[tk]))
        texto = ''
        if concatenar:
            for i in resultado:
                texto += i
            return texto
        else:
            return resultado

from modulos.database.db_tokens import DatabaseTokens, TokenObject
from modulos.tokenizador.modulos.ferramentas_tokenizador import FerramentasTokenizador
from modulos.constantes.constante_tokenizador import CONST_TOKENIZADOR

class Tokenizador(FerramentasTokenizador):
    def __init__(self, quantidade:int, formato:str):
        self.__tokens = {}
        self.__rev_tokens = {}
        self.__maior_token=0

        if quantidade<0: raise ValueError

        #carregando o tokenizador
        self.__montar_tokens(quantidade=quantidade, formato=formato)

    def __montar_tokens(self, formato:str, quantidade:int):
        '''
        Método que monta as listas usadas para criar e defazer tokens
        Params:
            formato: formato dos tokens usados. Pode ser hex ou utf-8
            quantidade: total de tokens usados, composto de tokens fixos e variaveis
        '''
        #recuperanto os tokens fixos e opcionais
        tokens = DatabaseTokens().get_tokens_fixos(formato)
        quantidade -= len(tokens)
        if quantidade>0:
            tokens += DatabaseTokens().get_tokenObjects(quantidade=quantidade, formato=formato)

        for tk in tokens:
            # para evitar falha no dicionário usa hexadecimal
            hex_tk = self.converter_texto_para_hex(tk.valor_token) 

            # recupera o maior token para fazer uma busca gulosa
            if self.__maior_token<len(hex_tk):
                self.__maior_token = len(hex_tk)
            
            # salva o dicionário de tokens e o dicionário reverso
            self.__tokens[hex_tk] = tk.id
            self.__rev_tokens[tk.id] = tk.valor_token

    def transformar_texto_em_tokens(self, texto:str, status=False):
        resultado = []
        nao_achou = True
        while len(texto)>0:
            for i in range(self.__maior_token,0,-1):
                if i<=len(texto):
                    bloco = self.converter_texto_para_hex(texto[:i])
                    if status:
                        print(texto[:i], texto)
                    if bloco in self.__tokens:
                        resultado.append(self.__tokens[bloco])
                        texto = texto[i:]
                        nao_achou = False
                        break
            
            if nao_achou:
                resultado.append('[unk]')
                texto = texto[i:]
        return resultado
    
    def transformar_tokens_em_texto(self, texto_tokenizado:list[str], concatenar=False):
        resultado = []
        for tk in texto_tokenizado:
            if tk in self.__rev_tokens:
                resultado.append(self.__rev_tokens[tk])
        texto = ''
        if concatenar:
            for i in resultado:
                texto += i
            return texto
        else:
            return resultado

    @property
    def get_token_list(self):
        return self.__tokens

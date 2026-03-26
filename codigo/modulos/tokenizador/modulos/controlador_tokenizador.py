from modulos.database.db_tokens import DatabaseTokens, TokenObject
from modulos.tokenizador.ferramentas_tokenizador import FerramentasTokenizador
from modulos.constantes.constante_tokenizador import CONST_TOKENIZADOR

class ControladorTokenizador(FerramentasTokenizador):
    def __init__(self, formato_tokens:str, total_tokens=100000):
        super().__init__()

        self.__db = DatabaseTokens()
        self.__tokens = {}
        self.__reverso_tokens = {}

        self.__gerar_tokenizador(total_tokens, formato_tokens)

    
    def __gerar_tokenizador(self, total_tokens:int, formato:str):
        tam_tokens= set()

        for i, tk in enumerate(self.__db.get_tokenObjects(total_tokens, formato)):
            tam_tokens.add(tk.get_tamanho_token())
                        
            #gerando o dicionário de tokenização
            self.__tokens[tk.valor_token] = tk.id

            #gerando o dicionário de reversão
            self.__reverso_tokens[tk.id] = tk.valor_token                     
        self.__tokens["tam_tokens"] = sorted(list(tam_tokens),reverse=True)    

    def tokenizar(self, texto:str, formato):
        step_token_desconhecido = 1
        if formato == CONST_TOKENIZADOR.FORMATO_TEXTO.HEX:
            texto = self.converter_texto_para_hex(texto)
            step_token_desconhecido = 2
        elif formato == CONST_TOKENIZADOR.FORMATO_TEXTO.UTF8:
            step_token_desconhecido = 1
        else:
            raise ValueError
        
        resultado = []
        print(texto)
        while(len(texto))>0:            
            for i, tam in enumerate(self.__tokens["tam_tokens"]):
                if str(texto[:tam]) in self.__tokens.keys():
                    resultado.append(self.__tokens[texto[:tam]])
                    print(texto[:tam], len(texto[:tam]))
                    texto = texto[tam:]
                    break
                
            if len(texto)>0:
                resultado.append(CONST_TOKENIZADOR.TOKENS_ESPECIAIS.UNKNOWN)
                texto = texto[step_token_desconhecido:]
        return resultado
    
    def reverter_tokens(self, tokens:list[str], gerar_texto=False)->list:
        resultado = []
        for i, tk in enumerate(tokens):
            if tk != CONST_TOKENIZADOR.TOKENS_ESPECIAIS.UNKNOWN:
                resultado.append(self.__reverso_tokens[tk])
            else:
                resultado.append(CONST_TOKENIZADOR.TOKENS_ESPECIAIS.UNKNOWN)
        if gerar_texto:
            return ["".join(resultado)]
        else:
            return resultado
                
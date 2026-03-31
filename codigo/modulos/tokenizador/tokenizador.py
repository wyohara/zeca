from modulos.tokenizador.modulos.processadores_texto.processamento_texto_trie import ProcessamentoTextoTrie
from modulos.tokenizador.modulos.tokenizador import ControladorTokenizador
from modulos.constantes.constante_tokenizador import CONST_TOKENIZADOR

class Tokenizador():
    def __init__(self, formato_tokens=CONST_TOKENIZADOR.FORMATO_TEXTO.HEX, tam_tokens=100000):
        super().__init__()
        self.__controlador_tokenizador = ControladorTokenizador(tam_tokens, formato_tokens)
        
    def processar_dataset_textos(self, formato=CONST_TOKENIZADOR.FORMATO_TEXTO.HEX, status=True):
        ProcessamentoTextoTrie().processar_dataset_textos(formato=formato, status=status)

    def transformar_texto_em_tokens(self, texto="Testando o token", formato=CONST_TOKENIZADOR.FORMATO_TEXTO.HEX):
        return self.__controlador_tokenizador.tokenizar(texto, formato)
    
    def transformar_tokens_em_texto(self,lista_Tokens:list, gerar_texto=False):
        return self.__controlador_tokenizador.reverter_tokens(lista_Tokens, gerar_texto)

    




    


from modulos.tokenizador.modulos.ferramentas_tokenizador import FerramentasTokenizador
import re
from typing import Final


class PreprocessamentoTexto(FerramentasTokenizador):
    def __init__(self,texto):
        self.CARACTERES:Final = [',','?','!','{','}','[',']','(',')',';','_','/','\\','|','@','#','\t']
        self.CARACTERES_ENTRE_LETRAS:Final = ['\'','’','"','”','-','—','...', '.']
        self.__texto = texto

    def get_texto(self)->str:
        self.__trocar_caracteres_entre_letras()
        self.__trocar_caracteres_antes_ou_depois_letras()
        self.__trocar_caracteres()
        return self.__texto

    def __trocar_caracteres_entre_letras(self):
        texto = self.__texto
        for letra in self.CARACTERES_ENTRE_LETRAS:
            letra_escapada = re.escape(letra)  # Escapa caracteres especiais
            padrao = rf'(?<=[\w]){letra_escapada}(?=[\w])'
            texto = re.sub(padrao, ' ', texto, flags=re.UNICODE)
        self.__texto = texto
         
    
    def __trocar_caracteres_antes_ou_depois_letras(self):
        texto = self.__texto
        for caractere in self.CARACTERES_ENTRE_LETRAS:
            # Escapa caracteres especiais para regex
            caractere_escapado = re.escape(caractere)
            
            # Substitui caractere antes da letra
            padrao_depois = rf'{caractere_escapado}(?=[\w])'
            texto = re.sub(padrao_depois, ' ', texto, flags=re.UNICODE)
            
            # Substitui caractere depois da letra
            padrao_antes = rf'(?<=[\w]){caractere_escapado}'
            texto = re.sub(padrao_antes, ' ', texto, flags=re.UNICODE)
        self.__texto = texto
    
    def __trocar_caracteres(self):
        texto = self.__texto
        for letra in self.CARACTERES:
            texto = texto.replace(letra, ' ')
        self.__texto = texto
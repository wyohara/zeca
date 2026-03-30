import hashlib

class FerramentasTokenizador():
    @staticmethod
    def converter_hex_para_texto(texto_hex):
        return bytes.fromhex(texto_hex).decode('utf-8',errors='surrogateescape')
    
    @staticmethod
    def converter_texto_para_hex(texto:str):
        if type(texto)== str:
            return texto.encode('utf-8').hex()
        else:
            raise TypeError

    @staticmethod
    def gerar_hash(texto:str):
        return hashlib.sha256(str(texto).encode('utf-8'))

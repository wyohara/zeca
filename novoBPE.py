import time


class NovoBPE ():

    def montar_arvore(self,texto:str):        
        texto = texto.replace("\n", " ")
        trie = {}
        for palavra in texto.split(" "):
            trie = self.criar_arvore(palavra, trie)
        self.tokens = []
        print(trie)

        while( trie!={}):
            tk= ''
            busca = self.percorrer_arvore(trie, tk)
            self.tokens.append(busca)
        print(self.tokens)

    
    def percorrer_arvore(self, arvore:dict, chave="", tk=''):
        if chave != "":
            if len(arvore[chave])==1:
                resposta = (tk, arvore[chave]["valor"])
                del(arvore[chave])
                return resposta                
            arvore = arvore[chave]        
  
        for k in arvore.keys():
            if k != "valor":
                tk+=k
                return self.percorrer_arvore(arvore, k, tk)

    def criar_arvore(self, palavra:str, dicionario:dict):
        if len(palavra) == 0:
            return dicionario
        letra = palavra[0]
        try:
            dicionario[letra]["valor"] +=1
        except KeyError:
            dicionario[letra] ={"valor":1}
        

        tokens = self.criar_arvore(palavra[1:], dicionario[letra])
        return dicionario

if __name__ == "__main__":

    f = open("teste_e_relatorios/tokenizador/livro_teste.txt", "r", encoding="utf8")
    texto = f.read()
    f.close()

    #texto = "oi como vai esse é meu texto"

    inicio = time.perf_counter()
    NovoBPE().montar_arvore(texto)
    fim = time.perf_counter()

    print(f"tempo {inicio} - {fim} = {fim-inicio}")

    #1034880 tokens
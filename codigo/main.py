import numpy as np

from modulos.tokenizador.modulos.controlador_tokenizador import ControladorTokenizador
from modulos.tokenizador.modulos.processadores_texto.processamento_texto_trie import ProcessamentoTextoTrie
from modulos.embeding.embeding import Embeding
from modulos.tokenizador.tokenizador import Tokenizador

def testando_embeding():
    X = np.array([[1., 0., 1.],  [0., 1., 0.],  [1., 1., 1.]])
    Y =  np.array([
            [0.5, 0.2, 0.3],
            [0.1, 0.9, 0.0],
            [0.8, 0.7, 0.6]
        ])

    embeding = Embeding()
    saida_inicial = embeding.foward(X)
    embeding.gerar_loss(saida_inicial, Y)
    for i in range(1000):
        saida_final = embeding.backward(X, Y)
        embeding.gerar_loss(saida_final, Y)


def get_livro_teste():
    f = open("teste_e_relatorios/tokenizador/livro_teste.txt", "r",encoding="utf-8")
    texto = f.read()
    f.close()
    return texto


if __name__ == "__main__":
    tkr = Tokenizador()
    tkr.processar_dataset_textos()
    res = tkr.transformar_texto_em_tokens("oi tudo bem como vai?")
    print('tokens ',res)
    rev_res = tkr.transformar_tokens_em_texto(res,gerar_texto=True)
    print(rev_res)
    print("fim")
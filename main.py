import numpy as np

from lib.tokenizador.tokenizador import Tokenizador
from lib.embeding.embeding import Embeding

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
    tkr.gerar_tokenizador()
    tkr.processar_dataset_textos()
    tokens = tkr.transformar_texto_em_tokens("Primeiro teste")
    print("tokens: ", tokens)
    arr = tkr.transformar_tokens_em_array(tokens,True)
    print(arr)
    arr = tkr.transformar_tokens_em_array(tokens,False)
    print(arr)
    rev_tokens = tkr.transformar_tokens_em_texto(tokens)
    print("Tokens reverso: ", rev_tokens)

    relatorio = tkr.relatorio(get_livro_teste(),tkr.gerar_tokenizador())
    relatorio.get_total_tokens_palavra()
    relatorio.get_total_tokens_unicos()
    relatorio.get_entropia_dos_tokens()
    relatorio.get_curva_vocabulario()
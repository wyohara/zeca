from modulos.database.tokenizador_object import TokenizadorObject
from modulos.database.db_tokens import DatabaseTokens

import math
import matplotlib.pyplot as plt
import numpy as np

class RelatorioTokenizador():
    def __init__(self, texto:str, tokenizador_analisado:TokenizadorObject ):
        self.__dados ={}
        self.__dados["texto"] = texto
        self.__dados["tam_texto"] = len(texto)
        self.__dados["total_plavras"] = len(texto.replace("\n", ' ').split(" "))
        self.__dados["tokenizador"] = tokenizador_analisado
        self.__dados["tam_tokenizador"] = tokenizador_analisado.get_tamanho_tokenizador()
        self.__dados["texto_tokenizado"] = tokenizador_analisado.tokenizar(texto)
        self.__dados["total_tokens_no_texto"] = len(self.__dados["texto_tokenizado"])

    def get_total_tokens_palavra(self, status = True):       
        dados = self.__dados
        if status:
            print(f'''>>> Relatório de Tokens por Palavras:
                    - Tokenizador com {dados["tam_tokenizador"]} tokens;
                    - Texto com {dados["tam_texto"]} palavras;
                    - Texto com {dados["total_tokens_no_texto"]} tokens;
                    - Total: o tokenizador usa {dados["total_tokens_no_texto"]/dados["tam_texto"]:.2f} tokens/palavras.''')
        return dados["total_tokens_no_texto"]/dados["tam_texto"]
    
    def get_total_tokens_unicos(self, status=True):             
        dados = self.__dados
        tokens_unicos = 0
        for token in dados["texto_tokenizado"]:
            if dados["texto_tokenizado"].count(token) ==1:
                tokens_unicos +=1
        
        if status:
            print(f'''>>> Relatório de Total de tokens unicos:
                    - Tokenizador com {dados["tam_tokenizador"]} tokens;
                    - Texto com {dados["tam_texto"]} palavras;
                    - Percentual de tokens unicos: {tokens_unicos} ou {(tokens_unicos/dados["total_tokens_no_texto"])*100:.2f}%''')
        return tokens_unicos
    
    def get_entropia_dos_tokens(self, status=True):             
        dados = self.__dados

        entropia = 0
        for token in dados["texto_tokenizado"]:
            ocorrencia= dados["texto_tokenizado"].count(token)
            frequencia = ocorrencia/dados["tam_tokenizador"]
            entropia += -frequencia*math.log2(frequencia)
        
        if status:
            print(f'''>>> Relatório da Entropia:
                        Baseado na Lei de Zipf, que descreve a distribuição de frequências em línguas naturais. Espera-se entropia  entre 7,5 e 10. 
                        Mede a estabilidade dos tokens usados.
                        - Tokenizador com {dados["tam_tokenizador"]} tokens;
                        - Texto com {dados["tam_texto"]} palavras;                     
                        - Entropia {entropia:.4f}''')
        return entropia


    def get_curva_vocabulario(self, token_min=50000, token_max=500000, step=10000, salvar=False, status=True):
        dados = self.__dados
        resultados = []
        for q in range(token_min, token_max, step):
            tkr = DatabaseTokens().get_tokenObjects(quantidade= q)
            print(f">>>> Gerando tokenizador com {q} tokens")
            resultados.append([(len(tkr.tokenizar(dados["texto"]))/dados["total_plavras"]), q])

        
        relacao_token_palavra_y = [resultado[0] for resultado in resultados]
        valores_x = [resultado[1] for resultado in resultados]

        # Criar o gráfico
        plt.figure(figsize=(10, 6))
        coordenadas_joelho = self.__gerar_joelho(valores_x, relacao_token_palavra_y)
        plt.axvline(coordenadas_joelho[0], color='r', linestyle='--', label=f'Joelho X: {coordenadas_joelho[0]}')
        plt.axhline(coordenadas_joelho[1], color='y', linestyle='--', label=f'Joelho Y: {coordenadas_joelho[1]:.2f}')
        plt.plot(valores_x, relacao_token_palavra_y, linestyle='-', color='blue', label='Relação token/palavra')
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Personalizar gráfico
        plt.xlabel('Tamanho do Vocabulário de tokens')
        plt.ylabel('Relação token/palavra')
        plt.title('Relação entre Tamanho do Vocabulário de tokens e o texto analisado')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()


        if status:
            plt.show()
        if salvar:
            plt.savefig()

        return resultados

    
    def __gerar_joelho(self, x:list, y:list):
        # Extrair x e y (x é o tamanho do vocabulário, y é a métrica)
        x = np.array(x)
        y = np.array(y)

        # Normalizar os dados para [0,1]
        x_norm = (x - x.min()) / (x.max() - x.min())
        y_norm = (y - y.min()) / (y.max() - y.min())

        # Criar a linha reta entre o primeiro e o último ponto normalizado
        # Primeiro ponto: (0, y_norm[0]), último: (1, y_norm[-1])
        y_reta = np.linspace(y_norm[0], y_norm[-1], len(x_norm))

        # Calcular a distância vertical entre a curva normalizada e a reta
        distancias = np.abs(y_norm - y_reta)

        # O joelho é o ponto com maior distância
        indice_joelho = np.argmax(distancias)
        joelho_x = x[indice_joelho]
        joelho_y = y[indice_joelho]
        return(joelho_x, joelho_y)
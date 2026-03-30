from modulos.tokenizador.modulos.processamento_textos_abs import ProcessamentoDeTextoABS
from modulos.constantes.constante_tokenizador import CONST_TOKENIZADOR
from modulos.database.db_tokens import TokenObject
from modulos.tokenizador.modulos.preprocessamento_texto import PreprocessamentoTexto


class ProcessamentoTextoTrie (ProcessamentoDeTextoABS):
    """
    Algoritmo que usa a arvore de trie para tokenização. Apenas para teste
    Outros algoritmos:
    'BPE (GPT-2)': AutoTokenizer.from_pretrained('gpt2'),
    'WordPiece (BERT)': AutoTokenizer.from_pretrained('bert-base-uncased'),
    'SentencePiece (XLM-R)': AutoTokenizer.from_pretrained('xlm-roberta-base'),
    'Unigram (ALBERT)': AutoTokenizer.from_pretrained('albert-base-v2'),
        
    """
    def __init__(self, modo_teste=False):
        super().__init__(modo_teste)
        self._modelo_processamento = CONST_TOKENIZADOR.MODELO_PROCESSAMENTO.TRIE
        self.__arvore={}

    def _recortar_tokens(self, texto:str, formato:str):    
        """
        Método central que gerencia toda a criação da árvore de trier
        Percorre o corpus separando em palavras e aplica o processamento, após isso
        gera a chave que é transformada em tokens e salvo no banco de dados.
        Processa apenas a cópia da árvore original para manter a lógica dos tokens

        Params:
            texto: corpus do texto usado para tokenizar
            formato: formato de saída, pode ser utf-8 ou hex
        Returns:
            list[TokenObject]: lista de objetos tokens
        """

        #remontando a árvore de Trie para continuar
        for tokens in self._db_tokens.get_lista_valores_tokens(formato):
            self.__arvore = self.__montar_arvore_trie(tokens,self.__arvore, formato, contar_tokens=False)

        #aplicando o preprocessamento de texto
        texto = PreprocessamentoTexto(texto).get_texto()

        #aplicando o algoritmo ao texto
        for i, palavra in enumerate(self.__get_palavras_recortadas(texto=texto, formato=formato)):
            self.__arvore = self.__montar_arvore_trie(palavra, self.__arvore, formato)

        resposta = self.__montar_lista_tokens(formato, self.__arvore)
        return resposta
        

    def __get_palavras_recortadas(self, texto:str, formato:str)-> list[str]:
        '''
        Método que recorta as palavras do texto e aplica as regras de modificação.
        O método ignora quebra de linha e espaços.
        Args:
            texto: Texto bruto a ser refatorado
            formato: Formatos aceitos de codificação (utf-8 e hex)
        Returns:
            list[str]: lista de palavras recortadas
        Raises:
            ValueError: solicita um formato inválido
        '''
        palavras = texto.replace('\n',' ').split()
        lista_palavras = []
        if not palavras:
            raise ValueError
        for palavra in palavras:
            if formato.lower() == CONST_TOKENIZADOR.FORMATO_TEXTO.UTF8:
                pass
            elif formato.lower() == CONST_TOKENIZADOR.FORMATO_TEXTO.HEX:
                palavra = self._ferramentas.converter_texto_para_hex(palavra)
            else:
                raise ValueError
            lista_palavras.append(palavra)
        return lista_palavras

    
    def __montar_arvore_trie(self, palavra:str, arvore:dict, formato:str, contar_tokens=True) -> dict:
        """
        Método que monta a ávore de trie. Cria um dicionário onde a chave é cada caractere. 
        Caso a sequência de caracteres não exista é criada uma ramificação e a chave fim, 
        indicando o número de vezes que o contador passou pela bifurcação.

        Obs: 
            - A árvore precisa encontrar duas vezes o mesmo prefixo para bifurcar
            - Internamente o radical vira uma nova árvore, mas seu contador é 
            somado pela regra de integridade do banco de dados.
        
        Params:
            palavra: palavra processada que será usada na árvore
            arvore: ávore que será usada no processo
            contar_tokens: incrementa o contador de tokens

        Returns:
            arvore: a árvore inicial atualizada com os novos valores

        """
        no_atual = arvore
        raiz = True

        # cria o step do range, se for hex irá andar 2 bytes (1 char UNICODE) se utf-8 uma letra
        step = 1 
        if formato == CONST_TOKENIZADOR.FORMATO_TEXTO.HEX: step = 2
        for i in range(0,len(palavra), step):
            letra = palavra[i:i+step]
            # Cria o nó fim para uma bifurcação
            if letra not in no_atual :
                # verifica se é raiz para não criar a chave fim no início da árvore
                if (len(no_atual.keys())==1 and not raiz):
                    no_atual['fim'] = 1
                no_atual[letra] = {}
            
            # incrementao contador de fim
            if ('fim' in no_atual.keys()) and contar_tokens:
                no_atual['fim'] += 1

            # Se for a última letra, marca como fim de palavra
            if i == len(palavra) - step:
                no_atual[letra]['fim'] = 1
            
            no_atual = no_atual[letra] #incrementa a árvore para o próximo nó
            raiz = False # marca como não sendo mais raiz
        return arvore

    
    def __montar_lista_tokens(self, formato:str, arvore:dict) -> list[TokenObject]:
        """
        A partir do dicionário da Trie, retorna uma lista de TokenObject
        Params:
            formato: formato do texto em 'utf-8' ou 'hex'
            arvore: a árvore usada para criar tokens
        
        Returns:
            list[TokenObject]: lista de objetos de token para salvar no bd
        """
        
        pilha = [[arvore, ""]]  # (nó_atual, token)
        
        resposta = []
        while pilha:
            no_atual, token = pilha.pop()
        
            # Primeiro, verifica se o nó atual tem 'fim' diretamente e zera os tokens
            if 'fim' in no_atual:
                resposta.append(TokenObject(valor_token=token, quantidade=no_atual['fim'], formato=formato))
                token = ''
            
            # Depois, processa os filhos (exceto 'fim')
            #amarrado com try, caso entre por acidente em uma chave 'fim'
            try:
                for chave, valor in no_atual.items():
                    if chave != 'fim':
                        pilha.append((valor, token + chave)) 
            except AttributeError:
                pass
    
        return resposta
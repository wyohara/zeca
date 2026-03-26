from modulos.tokenizador.modulos.processamento_textos_abs import ProcessamentoDeTextoABS
from modulos.constantes.constante_tokenizador import CONST_TOKENIZADOR
from modulos.database.db_tokens import TokenObject


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
        self.__arvore_trie ={}
        self._modelo_processamento = CONST_TOKENIZADOR.MODELO_PROCESSAMENTO.TRIE
    
    def _recortar_tokens(self,formato, texto:str):    
        """
        Processa o texto inserindo todas as palavras na Trie
        """
        palavras = texto.split()
        for palavra in palavras:
            if formato == CONST_TOKENIZADOR.FORMATO_TEXTO.UTF8:
                pass
            elif formato == CONST_TOKENIZADOR.FORMATO_TEXTO.HEX:
                palavra = self._ferramentas.converter_texto_para_hex(palavra)
            else:
                raise ValueError
            self.__inserir_palavra(palavra)
        return self.__montar_lista_tokens(formato)

    
    def __inserir_palavra(self, palavra:str):
        """
        Insere uma palavra na Árvore Trie
        """
        no_atual = self.__arvore_trie
        
        for i, letra in enumerate(palavra):

            try:
                no_atual['fim'] +=1
            except KeyError:
                no_atual['fim'] =1                

            # Cria o nó e marca o token como fim se não existir
            if letra not in no_atual:
                no_atual[letra] = {}
                no_atual['fim'] =1                  
            
            #sempre que passa por uma token fim é incrementado
            if 'fim' in no_atual.keys():
                no_atual['fim'] +=1 
                 
            # Se for a última letra, marca como fim de palavra
            if i == len(palavra) - 1:
                try:
                    no_atual[letra]['fim'] += 1                    
                except KeyError:
                    no_atual[letra]['fim'] = 1
            
            #incrementa a árvore para o próximo nó
            no_atual = no_atual[letra]

    def __montar_lista_tokens(self, formato:str):
        """
        A partir do dicionário da Trie, retorna uma lista de tuplas (token, frequência)
        """
        tokens_encontrados = []
        pilha = [(self.__arvore_trie, "")]  # (nó_atual, palavra_parcial)
        
        while pilha:
            no_atual, token = pilha.pop()
            
            # Percorre todas as chaves do nó atual
            for chave, quantidade in no_atual.items():
                if chave == 'fim':
                    # Quando encontra 'fim', significa que uma palavra completa foi formada
                    tokens_encontrados.append(TokenObject(valor_token=token, quantidade=quantidade, formato=formato))
                else:
                    # Caso não encontre fim continua descendo na árvore e concatena o token com a chave
                    pilha.append((quantidade, token + chave))       
        return tokens_encontrados
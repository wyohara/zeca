# Emebeding

O embedding (ou "camada de incorporação", em português) é uma das principais técnicas e uma das mais fundamentais em redes neurais, especialmente quando trabalhamos com dados categóricos, texto ou itens discretos.Um embedding é o processo de representar vetorialmente um objeto (como uma palavra, um usuário, ou um item) em um espaço contínuo de baixa dimensionalidade.  
As Redes neurais não entendem palavras ou categorias apenas números. Poderiamos transformar categorias em números diretamente o **One-Hot Encoding**.  
- **One Hot**: Se temos 5 palavras: `["rei", "rainha", "homem", "mulher", "maçã"]`, poderíamos representar:
```"rei" = [1, 0, 0, 0, 0]
"rainha" = [0, 1, 0, 0, 0]
"homem" = [0, 0, 1, 0, 0]
"maçã" = [0, 0, 0, 0, 1]
```
- Porém teríamos problemas como:  
    - *Esparsidade*: Os vetores se tornam gigantes e a maioria dos valores zero.  
    - *Ausência de Semântica*: O modelo não sabe se "rei" e "rainha" são relacionados ou o contexto frase.  

- **Embedding**: Cada item do vetor passa a ter um vetor de números densos (diferentes de zeros) onde a posição no espaço carrega significado.
```
"rei" = [0.85, 0.23, -0.15, 0.55]
"rainha" = [0.90, 0.21, -0.10, 0.60]
"homem" = [0.70, -0.30, 0.45, -0.10]
"mulher" = [0.75, -0.28, 0.50, -0.05]
"maçã" = [-0.50, 0.80, 0.90, 0.33]
```
- Se calcular o cosseno entre os vetores, percebemos que rei é mais próximo de rainha que maçã

## Funcionamento prático
Em uma rede neural, a camada de embedding é basicamente uma tabela de lookup (consulta).
- Índice: Cada palavra (ou categoria) recebe um índice único. Ex: "rei" = 1.
- Matriz de Embedding: A rede cria uma matriz gigante onde cada linha é o vetor de embedding para um índice.
- Consulta: Quando a rede vê o índice "1", ela vai até a linha 1 da matriz, copia o vetor [0.85, 0.23, -0.15, 0.55] e usa isso como representação da palavra.

Durante o treinamento, esses números (os pesos da matriz de embedding) são ajustados pelo backpropagation (retropropagação) para melhorar a performance da tarefa. Assim, o embedding aprende a capturar as características latentes dos dados.
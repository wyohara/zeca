# Princípio de ia  
Antes de pensar em inteligência artificial é preiso compreender o que ela é, entender seus limites e características e é para isso que este capítulo serve. Por definição nossa espécie é *Homo Sapiens* ou"humano sábio", pois nossa **inteligência** foi o fator determinante para a nossa sobrevivência. Foi por meio da nossa **inteligência** que percebemos o meio, o compreendemos, prevemos as possibilidades e criamos formas de manipular o mundo. 

Assim se seguissemos esse paralelo, poderíamos pensar que Inteligência Artificial é a replicação das mesmas capacidades dos humanos de enxergar, prever e criar possibilidades. Porém, atualmente, abrange uma série de subcampos e objetivos distintos tais como aprendizado, raciocínio ou mesmo atividades específicas como traduzir, criar código, jogar xadrez entre outros.
 
## A visão tradicional da inteligência artifical  
A forma mais tradicional de enxergar a inteligência artificial é por meio da ***racionalidade*** e ***humanidade***. Essas duas vertentes debatem se a inteligência artificial deve ser fiel ao humano ou ser simplificado para fazer o correto de forma racional, podendo ter 4 vertentes:  

### 1. Agir como humano
Essa é a visão tradicional proposto por **Alan Turing (1950)**, ela foi proposta para preencher a ideia geral **"O humano pode pensar?"**. Nela o computador seria interrogado por meio de perguntas escritas e após responder o interrogador deveria dizer se foi respondido por uma pessoa ou computador. Para poder passar no teste o computador precisaria de alto dempenho em: 
- ***1 - Processamento da linguagem natural*** para poder se comunicar.
- ***2 - Raciocínio automatizado***, não necessariamente lógico, para responder e tirar conclusões
- ***3 - Armazenamento do conhecimento*** armazenar o que percebe e aprende em uma representação do conhecimento
- ***4 - Aprendizado de máquina*** para se adaptar aos padrões desconhecidos para generalizar e extrapolar.

Além das capacidades acima, a ciência moderna propôs a extrapolação para um ***Teste de Turing total***, onde o computador não se limita apenas a responder por texto, ele também percebe e interage com o ambiente, e a partir disso o interrogador define se as ações são de um humano ou máquina. Para essa atividade é preciso das capacidades:  
- ***5 - Visão Computacional***: Capacidade de perceber o mundo por outros meios além do texto
- ***6 - Robótica***: Para poder interagir fisicamente com o meio

Essas 6 capacidades compõem a maior parte dos campos da Inteligência artificial.  


### 2. Pensar como humano
É a visão tradicional que busca entender como os humanos pensam. Podemos generalizar as técnicas em três metodos:
 - ***1 - Introspecção***: Capturar os pensamentos enquanto ocorrem;
 - ***2 - Experimentos psicológicos***: Observar as pessoas em ação
 - ***3 - Imagem Cerebral***: Observar o cérebro em ação

Esta ciência é bem ampla e com muitas possibilidades, mas não é abordado aqui por precisar de equipamentos específicos e amostragem.  

Alguns livros interessantes para a análise:
- *WILSON, Robert A.; KEIL, Frank C. (ed.). **The MIT encyclopedia of the cognitive sciences**. Cambridge: MIT Press, 1999.*  
- *NEWELL, Allen; SHAW, J. C.; SIMON, Herbert A. **Report on a general problem-solving program**. Santa Monica: RAND Corporation, 1961.*  

### 3. Pensar racionalmente
O pensar racionalmente já é um conceito filosófico antigo, Aristósteles foi um dos primeiros a codificar o pensamento correto, usando raciocínios lógicos irrefutáveis encadeados - o ***silogismo***. Um exemplo cássico é o silogismo *'Sócrates é um homem e todos os homens são mortais e conclui que Sócrates é mortal.'*. A partir de então se iniciou o estudo do campo da ***lógica***.  
Até o século XIX se acreditou que a lógica poderia resolver qualquer problema solucionável. Prém existe uma limitação importante: Requer que o conhecimento do mundo esteja certo - condição raramente alcançada, tanto pela própria definição de certo, quanto por não conhecermos todas as regras e fatos possíveis.  
A falta da definição completa do certo é preenchida através da **probabilidade**, permitindo uma aproximação usando informações incertas, assim podemos criar um **pensamento racional ambrangente**. Apenas pensar racionalmente não torna o agente racional, para isso é preciso também definir uma ***ação racional a partir do pensamento racional***.  

### 4. Agir racionalmente
Aqui surge a definição de ***Agente***, que é todo aquele que age. Assim um computador que executa uma ação é um agente. Porém agir não é tudo que esperamos do computador, esperamos que ele seja autônomo, podendo agir dentro do que se espera ao longo do tempo - se tornando um ***Agente Autônomo***.  
Aqui ocorre a extrapolação, além de fazer inferências corretas, também age de forma correta. Um exemplo seria: *"O fogão esquentar dentro dos limites está tudo bem, mas aquecer além do limite o agente age acionando o alarme de incêndio"*.  

## Modelo padrão
Quando definimos uma tarefa definida para um agente autonomo, como jogar xadrez ou fazer um cálculo, podemos usar um **modelo padrão**, isto é, um modelo simples em que é especificado todo o objetivo para o computador. Porém, a medida que nos aproximamos do mundo real, é cada vez mais difícil especificar todos os objetivos ou atingir o objetivo desejado, ou a resposta se afasta do desejo de quem solicitou. Um exemplo: se quisermos um carro autônomo com máxima segurança precisamos lidar com motoristas imprudentes, asfalto ruim, desgaste de equipamentos entre outos, tornando arriscado o deslocamento, assim a solução mais lógica não sair.  
O problema entre alinhar o objetivo desejado e o objetivo mais lógico se  chama ***problema de alinhamento de valores*** e quanto mais inteligente um agentemais difícil é alinhar esses valores, pois as consequências de uma correção se torna incalculável, imagine corrigir a segurança do mesmo carro, uma alteração nas características  de segurança pode fazer ele aceitar atropelar uma pessoa se os riscos de dano forem menores que o calculado, mesmo que esse cálculo decorra de uma falha instrumental.  

## Fundamentos filosóficos da inteligência artificial  
Antes de fazer um apanhado dos pensamentos filosóficos sobre inteligência artificial, é preciso separar as regras do pensamento artificial e o sistema físico que o pensamento artificial opera.  
Quanto ao ***pensamento artificial*** as principais bases teóricas são:  
- Aristósteles (384–322 a.C.) foi o primeiro a formular o conjunto de regras que regem a racionalidade - a lógica. 
- René Descartes (1596–1650) fez a primeira discussão clara sobre a distinção entre mente e matéria. Ele criou o **dualismo ou espírito** que separa a inteligência do meio físico. O espírito é o que separa o livre-arbítrio de meras leis físicas. Se opondo ao dualismo temos a teoria do materialismo, onde diz que o cérebro opera somente por leis físicas e o livre-arbítrio é apenas a percepção das escolhas.
- Francis Bacon (1561–1626) em Novum Organum propôs o empirismo, onde propõe que todo conhecimento passou primeiro pelos sentidos.
- David Hume (1711–1776), em Tratado da Natureza Humana (Hume, 1739) propôs a indução que fala que as regras gerais são aprendidas por exposições repetidas
- Círculo de Viena (décadas de 1920 e 1930) com base no trabalho de Ludwig Wittgenstein (1889–1951) e Bertrand Russell (1872–1970) propôs o positivismo lógico, onde todo o conhecimento é feito de teorias lógicas conectadas.
- Rudolf Carnap (1891–1970) e Carl Hempel (1905–1997) propôs a Teoria da confirmação onde tentou analizar o conhecimento a partir da experiência. Para isso isso ele tentou quantificar quanta crença deve ser ver atribuído a uma sentença lógica com base nas outras observações. O livro de Carnap, A Estrutura Lógica do Mundo (1928), foi talvez a primeira teoria da mente como um processo computacional.

Ainda sobre as bases filosóficas, Aristósteles em *De Motu Animalium* Argumentou que a ação ocorre da relação lógica entre objetivos e conhecimentos previos de resultado de ações, sendo uma base para o ***agente inteligente***. Em *Ética a Nicômaco (Livro III. 3, 1112b)* Aristóteles propõe provavelmente o  que chamamos hoje de algoritmo:  

```Deliberamos não sobre os fins, mas sobre os meios. Pois um médico não delibera se deve curar, nem um orador se deve persuadir,... Eles assumem o fim e consideram como e por quais meios ele é atingido, e se parece ser produzido fácil e melhormente por eles; enquanto se é alcançado por apenas um meio, eles consideram como será alcançado por este e por quais meios isto será alcançado, até chegarem à causa primeira,... e o que é último na ordem da análise parece ser primeiro na ordem do devir. E se nos deparamos com uma impossibilidade, desistimos da busca, por exemplo, se precisamos de dinheiro e este não pode ser obtido; mas se uma coisa parece possível, tentamos fazê-la.```

Foi essa lógica usada em `NEWELL, Allen; SHAW, J. C.; SIMON, Herbert A. Report on a general problem-solving program. Santa Monica: RAND Corporation, 1961.`

- Ramon Llull (c. 1232–1315)  tentou implementar o prieiro mecanismo real baseado em lógica usando discos de papel em Ars Magna ou A Grande Arte (1305).
- Leonardo da Vinci (1452–1519) projetou, mas não construiu, uma calculadora mecânica.
- Wilhelm Schickard (1592–1635) construiu a primeira calculadora mecânica
- Gottfried Wilhelm Leibniz (1646–1716) tentou criar uma máquina que opera por conceito não números, mas era muito limitada
- Thomas Hobbes no livro Leviatã de 1651 propôs uma máquina pensante como um "animal artificial"













## Bibliografia  
- *RUSSELL, Stuart J.; NORVIG, Peter. **Artificial intelligence: a modern approach.** 4. ed. Global ed. London: Pearson, 2021.*

Trabalho Prático - Arquitetura e Organização de Computadores I
    Prof. Rodrigo Calvo

Alunos:
    Guilherme Jucoski da Silva - RA: 138642
    Ideraldo Luis Trentini Júnior - RA: 138318
    Matheus Henrique Borsato - RA: 138246


Para iniciar o simulador, é necessário executar o arquivo principal trabalho_simulador.py.
Este arquivo gerencia a entrada do usuário e coordena as interações entre os componentes da arquitetura simulada: 
a memória, o processador e os registradores, que em conjunto replicam o funcionamento de um computador de baixo nível, como o IAS.


A execução pode ser feita de duas formas:

Linha de Comando: Passando o nome do arquivo do programa como argumento. 

Para simular o selection_sort.txt:
`python trabalho_simulador.py selection_sort.txt`

Para simular o media_ponderada.txt:
`python trabalho_simulador.py media_ponderada.txt`

Para simular o teste.txt:
`python trabalho_simulador.py teste.txt`

Modo Interativo: Se nenhum arquivo for especificado, o programa solicitará o nome do arquivo de entrada.

--------------------------------------------------------------------------------------------------------------------------------------------------------------

Durante a simulação, um arquivo chamado simulador_memoria.txt é gerado e atualizado a cada instrução. 
Ele permite que o usuário visualize o estado da memória em tempo real, rastreando todas as modificações.

A simulação dos três programas incluídos demonstra diferentes aspectos da arquitetura:

selection_sort.txt: Demonstra a execução de um algoritmo de ordenação. É possível a visualização dos dados ordenados em "simulador_memoria.txt". Os dados
a serem ordenados estão entre 0x00 e 0x05.
media_ponderada.txt: Ilustra o uso de operações aritméticas, com o resultado final do cálculo sendo armazenado no endereço 0x10. Os valores a serem calculados
estão entre os endereços 0x00 e 0x03 e seus respectivos pesos em 0x08 a 0x0B.
teste.txt: Este arquivo não representa um algoritmo, mas sim um conjunto de testes para todas as instruções 
e possibilidades do simulador que não foram usadas nos outros programas. 

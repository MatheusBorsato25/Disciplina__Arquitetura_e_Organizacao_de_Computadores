
'''
    Trabalho Prático
    Arquitetura e Organização de Computadores I
    Prof. Rodrigo Calvo

    Guilherme Jucoski da Silva - RA: 138642
    Ideraldo Luis Trentini Júnior - RA: 138318
    Matheus Henrique Borsato - RA: 138246
'''

from processador import Processador
from sys import argv


def main() -> None:
    '''
    Função principal do programa.
    '''
    try:
        # Verifica se o formato da linha de comando está incorreto e exibe mensagens explicativas.
        if len(argv) > 2:
            print("\nUso incorreto.")
            print("Formato correto: python trabalho_simulador.py [arquivo_programa.txt]")
            print("Exemplo: python trabalho_simulador.py selection_sort.txt\n")
            return
        
        if len(argv) == 2:
            # Trata o caso do nome do arquivo ser passado na linha de comando.
            nome_arq = argv[1]
        else: # len(argv) == 1
            # Solicita ao usuário o nome do arquivo de entrada.
            nome_arq = input("\n Digite o nome do arquivo: ")
            
        with open(nome_arq, 'r') as arq: # Abre o arquivo em modo de leitura ('r').
            # Cria uma instância do Processador, carregando o programa do arquivo.       
            processador = Processador(arq)
            # Inicia a execução do programa.
            processador.executa_programa()
        print(f"\n{nome_arq} executado com sucesso!\n")
        
    except FileNotFoundError:
        # Captura e imprime um erro se o arquivo não for encontrado.
        print("\nErro: Arquivo não encontrado!\n")       
        
        
        
if __name__ == '__main__':
    main()
    
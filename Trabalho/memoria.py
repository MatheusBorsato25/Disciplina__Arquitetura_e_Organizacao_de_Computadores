
'''
    Trabalho Prático
    Arquitetura e Organização de Computadores I
    Prof. Rodrigo Calvo

    Guilherme Jucoski da Silva - RA: 138642
    Ideraldo Luis Trentini Júnior - RA: 138318
    Matheus Henrique Borsato - RA: 138246
'''

import io

# Classe Memória: Simula a memória RAM do computador.

class Memoria:
    
    lista: list[str|None] 
    
    # Construtor da Classe Memória.
    def __init__(self, tamanho: int = 1024) -> None:
        
        # Inicializa a lista de memória com 'None' em todas as posições.
        self.lista = [None] * tamanho
        
        
    def escreve_memoria(self, endereco: int, conteudo: str):
        '''
        Escreve *conteúdo* em um *endereço* (índice) específico da memória.
        '''
        # Verifica se o endereço está dentro dos limites válidos da memória.
        if endereco < 0 or endereco >= len(self.lista):
            raise ValueError(f"Endereço fora do limite: {endereco}")
        self.lista[endereco] = conteudo
        
        
    def le_memoria(self, endereco: int) -> str|None:
        '''
        Lê o conteúdo de um endereço específico da memória.
        Retorna o conteúdo da posição de memória ou None se estiver vazia.
        '''
        # Verifica se o endereço está dentro dos limites válidos da memória.
        if endereco < 0 or endereco >= len(self.lista):
            raise ValueError(f"Endereço fora do limite: {endereco}")
        return self.lista[endereco]
    
    
    def limpa_memoria(self):
        '''
        Limpa toda a memória, preenchendo-a com 'None'.
        '''
        self.lista = [None] * len(self.lista)
        
        
    def cria_arquivo_memoria(self):
        '''
        Cria um arquivo de texto 'simulador_memoria.txt' 
        que representa o estado atual da memória.
        '''
        # Abre o arquivo 'simulador_memoria.txt' em modo de escrita ('w').
        with open('simulador_memoria.txt', 'w') as arq:
            for i in range(len(self.lista)):
                posicao_memoria = f'0x{i:02X}'  # Formata o endereço da memória em hexadecimal (ex: 0x00, 0x0A).
                if self.lista[i]:
                    # Se houver conteúdo, adiciona um espaço e o conteúdo.
                    conteudo = ' ' + str(self.lista[i])
                else:
                    # Se não houver conteúdo, a string fica vazia.
                    conteudo = ''
            
                linha = posicao_memoria + conteudo # Linha a ser escrita: endereço + conteúdo
                # Adiciona uma quebra de linha para todas as linhas, exceto a última e escreve a linha em 'simulador_memoria.txt'
                if i < len(self.lista) - 1:
                    arq.write(linha + '\n')
                else:
                    arq.write(linha)
    
    
    def salva_memoria(self, arq: io.TextIOWrapper) -> int:
        '''
        Carrega dados e instruções de um arquivo de texto para a memória.
        Como parâmetro, tem-se *arq*, um descritor de arquivo aberto para leitura (io.TextIOWrapper).
        Retorna o endereço da primeira instrução a ser executada.
        '''
        # Salva os dados na memória
        dado = arq.readline().strip('\n') # Lê uma linha do arquivo e remove o '\n'
        while dado: # Loop enquanto houver dados para ler
            informacoes = dado.split() # Divide a linha em endereço e dado
            # Escreve o dado na memória no endereço especificado (convertido de hexadecimal para inteiro).
            self.escreve_memoria(int(informacoes[0], 16), informacoes[1])
            dado = arq.readline().strip('\n')
                
        # Salva o endereço da primeira instrução
        primeiro_endereco = arq.readline().strip('\n')
        # Converte o endereço da primeira instrução de hexadecimal para inteiro.
        primeiro_endereco_inteiro = int(primeiro_endereco, 16)
        # Variável auxiliar para percorrer os endereços das instruções.
        auxiliar_primeiro_endereco = primeiro_endereco_inteiro
        
        # Salva as instruções na memória
        instrucao = arq.readline().strip('\n') # Lê uma linha com uma instrução e remove o '\n'
        while instrucao: # Loop enquanto houver instruções para ler
            # Escreve a instrução na memória no endereço atual.
            self.escreve_memoria(auxiliar_primeiro_endereco, instrucao)
            auxiliar_primeiro_endereco += 1 # Incrementa o endereço para salvar a próxima instrução.
            instrucao = arq.readline().strip('\n')
            
        return primeiro_endereco_inteiro



'''
    Trabalho Prático
    Arquitetura e Organização de Computadores I
    Prof. Rodrigo Calvo

    Guilherme Jucoski da Silva - RA: 138642
    Ideraldo Luis Trentini Júnior - RA: 138318
    Matheus Henrique Borsato - RA: 138246
'''

from memoria import Memoria
from registradores import Registradores
import io
         
# Classe Processador: Simula a Unidade Central de Processamento (CPU).
class Processador:
    
    # Instância da classe Memoria.
    memoria: Memoria
    # Instância da classe Registradores.
    registradores: Registradores
    
    # Construtor da Classe Processador.
    def __init__(self, arq: io.TextIOWrapper) -> None:
        
        # Inicializa a memória.
        self.memoria = Memoria()
        # Salva o conteúdo de *arq* na memória e obtém o endereço da primeira instrução.
        primeiro_endereco = self.memoria.salva_memoria(arq)
        # Inicializa os registradores e fornece o primeiro endereço ao registrador PC.
        self.registradores = Registradores(primeiro_endereco)
    
                
    def gerar_opcode(self, instrucao: list[str]) -> str:
        '''
        Gera o código de operação (opcode) de *instrução*.
        Retorna o opcode correspondente como uma string binária.
        '''
        # Lógica para determinar o opcode com base na instrução.
        if instrucao[0] == "LOAD":
            if instrucao[1][:2] == "MQ":
                if len(instrucao) == 3: # LOAD MQ, M(X) - Carrega M(X) para MQ
                    op = '00001001'
                else: # LOAD MQ - Carrega MQ para AC
                    op = '00001010'
            elif instrucao[1][:2] == "M(": # LOAD M(X) - Carrega M(X) para AC
                op = '00000001'
            elif instrucao[1][:2] == "-M": # LOAD -M(X) - Carrega o negativo de M(X) para AC
                op = '00000010'
            elif instrucao[1][:2] == "|M": # LOAD |M(X)| - Carrega o valor absoluto de M(X) para AC
                op = '00000011'
            elif instrucao[1][:2] == "-|": # LOAD -|M(X)| - Carrega o negativo do valor absoluto de M(X) para AC
                op = '00000100'
                
        elif instrucao[0] == "STOR": # STOR M(X) - Armazena o conteúdo de AC em M(X)
            op = '00100001'

        elif instrucao[0] == "JUMP": # JUMP M(X) - Desvio incondicional para o endereço M(X)
            op = '00001101'
        
        # Desvio Condicional
        elif instrucao[0] == "JUMP+": # JUMP+ M(X) - Desvia para M(X) se AC >= 0
            op = '00001111'

        # Instruções Aritméticas:
        
        elif instrucao[0] == "ADD":
            if instrucao[1][0] == "M": # ADD M(X) - Adiciona M(X) ao AC
                op = '00000101'
            elif instrucao[1][0] == "|": # ADD |M(X)| - Adiciona o valor absoluto de M(X) ao AC
                op = '00000111'
            else: # ADD DADO (Endereçamento Imediato - ADD 5, por exemplo) - Instrução ilustrativa
                op = '11111010' 
        
        elif instrucao[0] == "SUB":
            if instrucao[1][0] == "M": # SUB M(X) - Subtrai M(X) do AC
                op = '00000110'
            elif instrucao[1][0] == "|": # SUB |M(X)| - Subtrai o valor absoluto de M(X) do AC
                op = '00001000'
            else: # SUB DADO (Endereçamento Imediato - SUB 5, por exemplo) - Instrução ilustrativa
                op = '11111001'
                
        elif instrucao[0] == "MUL": 
            if instrucao[1][0] == "M": # MUL M(X) - Multiplica MQ por M(X) e armazena o resultado em MQ
                op = '00001011'
            else: # MUL DADO (Endereçamento Imediato - MUL 5, por exemplo) - Instrução ilustrativa
                op = '11110100'
                    
        elif instrucao[0] == "DIV":
            if instrucao[1][0] == "M":  # DIV M(X) - Divide AC por M(X), quociente em AC, resto em R
                op = '00001100'
            else: # DIV DADO (Endereçamento Imediato - DIV 5, por exemplo) - Instrução ilustrativa
                op = '11110011'
            
        elif instrucao[0] == "LSH": # LSH (Logical Shift Left) - Deslocamento lógico à esquerda do AC
            op = '00010100'
            
        elif instrucao[0] == "RSH": # RSH (Logical Shift Right) - Deslocamento lógico à direita do AC
            op = '00010101'

        # Instruções Lógicas:
        
        elif instrucao[0] == "AND": # AND M(X) - AND (E) bit a bit - Compara os bits do AC com os de M(X) - Instrução ilustrativa 
            # O resultado de cada comparação é 1 apenas se os dois bits na mesma posição forem 1. É 0, caso contrário.
            op = '10000000'
        
        elif instrucao[0] == "OR": # OR M(X) - OR (OU) bit a bit - Compara os bits do AC com os de M(X) - Instrução ilustrativa
            # O resultado de cada comparação é 1 se um dos bits na mesma posição for 1. É 0, caso contrário.
            op = '11001100'
            
        elif instrucao[0] == "NOT": # NOT - NOT (NÃO) bit a bit - Inverte os bits do AC - Instrução ilustrativa
            op = '11111111'
            
        return op
    
    
    def executa_busca(self) -> None:
        '''
        Simula o ciclo de busca de uma instrução.
        '''
        # Obtém o endereço da próxima instrução do Program Counter (PC).
        endereco = self.registradores.get_registrador("PC")
        if isinstance(endereco, int): # Verifica se o endereço é um inteiro
            # Move o endereço do PC para o MAR.
            self.registradores.set_registrador("MAR", endereco)
            # Lê a instrução da memória no endereço especificado pelo MAR.
            instrucao = self.memoria.le_memoria(endereco)
            if isinstance(instrucao, str): # Verifica se a instrução lida é uma string.
                # Move a instrução lida para o MBR.
                self.registradores.set_registrador("MBR", instrucao)
                partes_instrucao = instrucao.split() # Divide a instrução em partes.
                opcode = self.gerar_opcode(partes_instrucao) # Gera o opcode a partir da instrução.
                self.registradores.set_registrador("IR", opcode) # Salva o opcode no IR.
                self.registradores.incrementa_pc() # Incrementa PC para a próxima instrução
         
        
    def execucao(self) -> None:
        '''
        Simula o ciclo de execução de uma instrução.
        '''
        instrucao = self.registradores.get_registrador("MBR") # Obtém a instrução completa do MBR.
        if isinstance(instrucao, str): # Verifica se a instrução lida é uma string.
            # Divide a instrução para obter os operandos e endereços de memória.
            partes_instrucao = instrucao.split() 
            opcode = self.registradores.get_registrador("IR") # Obtém o opcode salvo em IR
        
        # Executa a operação correspondente ao opcode.
        if opcode == '00001010':
            self.executaLoadMQ()
        elif opcode == '00001001':
            self.executaLoadMQMemoria(partes_instrucao[2][2:-1]) 
        elif opcode == '00000001':
            self.executaLoad(partes_instrucao[1][2:-1])
        elif opcode == '00000010':
            self.executaLoadNeg(partes_instrucao[1][3:-1])
        elif opcode == '00000011':
            self.executaLoadAbs(partes_instrucao[1][3:-2])
        elif opcode == '00000100':
            self.executaLoadNegAbs(partes_instrucao[1][4:-2])
        elif opcode == '00100001':
            self.executaStor(partes_instrucao[1][2:-1])
        elif opcode == '00001101':
            self.executaJump(partes_instrucao[1])
        elif opcode == '00001111':
            self.executaJumpCondicional(partes_instrucao[1])
        elif opcode == '00000101':
            self.executaAdd(partes_instrucao[1][2:-1])
        elif opcode == '11111010':
            self.executaAddImediato(partes_instrucao[1])
        elif opcode == '00000111':
            self.executaAddAbs(partes_instrucao[1][3:-2])
        elif opcode == '00000110':
            self.executaSub(partes_instrucao[1][2:-1])
        elif opcode == '11111001':
            self.executaSubImediato(partes_instrucao[1])
        elif opcode == '00001000':
            self.executaSubAbs(partes_instrucao[1][3:-2])
        elif opcode == '00001011':
            self.executaMul(partes_instrucao[1][2:-1])
        elif opcode == '11110100':
            self.executaMulImediato(partes_instrucao[1])
        elif opcode == '00001100':
            self.executaDiv(partes_instrucao[1][2:-1])
        elif opcode == '11110011':
            self.executaDivImediato(partes_instrucao[1])
        elif opcode == '00010100':
            self.executaLSH()
        elif opcode == '00010101':
            self.executaRSH()
        elif opcode == '10000000':
            self.executaAnd(partes_instrucao[1][2:-1])
        elif opcode == '11001100':
            self.executaOr(partes_instrucao[1][2:-1])
        elif opcode == '11111111':
            self.executaNot()
            
                    
    def busca_dado(self, endereco: str) -> int:
        '''
        Busca um dado na memória. Recebe o endereço do dado
        na memória (string hexadecimal). Retorna o dado lido da memória como um inteiro.
        '''
        endereco_memoria = int(endereco, 16) # Converte o endereço de hexadecimal para inteiro.
        self.registradores.set_registrador("MAR", endereco_memoria) # Move o endereço para o MAR.
        conteudo = self.memoria.le_memoria(endereco_memoria) # Lê o conteúdo da memória no endereço especificado.
        dado = -1
        if isinstance(conteudo, str): # Verifica se o dado lido é uma string.
            dado = int(conteudo) # Converte o dado para inteiro.
        return dado
            
            
    def executaLoadMQ(self) -> None:
        '''
        Executa a instrução LOAD MQ (carrega o conteúdo de MQ para AC).
        '''
        conteudo = self.registradores.get_registrador("MQ") # Obtém o conteúdo do registrador MQ.
        self.registradores.set_registrador("MBR", conteudo) # Move o conteúdo de MQ para o MBR.
        conteudo_mbr = self.registradores.get_registrador("MBR") # Obtém o conteúdo do MBR.
        self.registradores.set_registrador("AC", conteudo_mbr) # Move o conteúdo do MBR para o AC.
        # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
        self.analisa_resultado()


    def executaLoadMQMemoria(self, endereco: str) -> None:
        '''
        Executa a instrução LOAD MQ, M(X) (carrega o conteúdo de M(X) para MQ).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", dado) # Move o dado lido para o MBR.
        conteudo_mbr = self.registradores.get_registrador("MBR") # Obtém o conteúdo do MBR.
        self.registradores.set_registrador("MQ", conteudo_mbr) # Move o conteúdo do MBR para o MQ.
        
        
    def executaLoad(self, endereco: str) -> None:
        '''
        Executa a instrução LOAD M(X) (carrega o conteúdo de M(X) para AC).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.  
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", dado) # Move o dado lido para o MBR.
        conteudo_mbr = self.registradores.get_registrador("MBR") # Obtém o conteúdo do MBR.
        self.registradores.set_registrador("AC", conteudo_mbr) # Move o conteúdo do MBR para o AC.
        # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
        self.analisa_resultado()
        
        
    def executaLoadNeg(self, endereco: str) -> None:
        '''
        Executa a instrução LOAD -M(X) (carrega o negativo do conteúdo de M(X) para AC).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", -dado) # Move o negativo do dado lido para MBR.
        conteudo_mbr = self.registradores.get_registrador("MBR") # Obtém o conteúdo do MBR.
        self.registradores.set_registrador("AC", conteudo_mbr) # Move o conteúdo do MBR para o AC.
        # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
        self.analisa_resultado()
        
        
    def executaLoadAbs(self, endereco: str) -> None:
        '''
        Executa a instrução LOAD |M(X)| (carrega o valor absoluto do conteúdo de M(X) para AC).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.      
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", abs(dado)) # Move o valor absoluto do dado lido para MBR.
        conteudo_mbr = self.registradores.get_registrador("MBR") # Obtém o conteúdo do MBR.
        self.registradores.set_registrador("AC", conteudo_mbr) # Move o conteúdo do MBR para o AC.
        # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
        self.analisa_resultado()
        
        
    def executaLoadNegAbs(self, endereco: str) -> None:
        '''
        Executa a instrução LOAD -|M(X)| (carrega o negativo do valor absoluto de M(X) para AC).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.        
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", -abs(dado)) # Move o negativo do valor absoluto do dado lido para MBR.
        conteudo_mbr = self.registradores.get_registrador("MBR") # Obtém o conteúdo do MBR.
        self.registradores.set_registrador("AC", conteudo_mbr) # Move o conteúdo do MBR para o AC.
        # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
        self.analisa_resultado()
        
        
    def executaStor(self, endereco: str) -> None:
        '''
        Executa a instrução STOR M(X) (armazena o conteúdo de AC em M(X)).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.
        '''
        endereco_memoria = int(endereco, 16) # Converte o endereço de hexadecimal para inteiro.
        self.registradores.set_registrador("MAR", endereco_memoria) # Move o endereço para o MAR.
        conteudo = self.registradores.get_registrador("AC") # Obtém o conteúdo do AC.
        self.registradores.set_registrador("MBR", conteudo) # Move o conteúdo do AC para o MBR.
        # Recupera o endereço do MAR e o dado do MBR.
        endereco_mar = self.registradores.get_registrador("MAR")
        dado = self.registradores.get_registrador("MBR")
        # Verifica se ambos são inteiros antes de escrever na memória.
        if (isinstance(endereco_mar, int) and isinstance(dado, int)):
            # Escreve o dado (convertido para string) na memória.
            self.memoria.escreve_memoria(endereco_mar, str(dado))
        
        
    def executaJump(self, endereco: str) -> None:
        '''
        Executa a instrução JUMP M(X) (desvio incondicional para o endereço M(X)).
        X nesse caso é o *endereço* de destino, representado por uma string hexadecimal.
        '''
        endereco_memoria = int(endereco, 16) # Converte o endereço de destino de hexadecimal para inteiro.
        # Define o Program Counter (PC) para o novo endereço, efetivando o desvio.
        self.registradores.set_registrador("PC", endereco_memoria)
        
        
    def executaJumpCondicional(self, endereco: str) -> None:
        '''
        Executa a instrução JUMP+ M(X) (desvio condicional para M(X) se AC >= 0).
        X nesse caso é o *endereço* de destino, representado por uma string hexadecimal.
        '''
        endereco_memoria = int(endereco, 16) # Converte o endereço de destino de hexadecimal para inteiro.
        conteudo = self.registradores.get_registrador("AC") # Obtém o conteúdo do AC.
        if isinstance(conteudo, int): # Verifica se o conteúdo do AC é um inteiro.
            # Se o conteúdo do AC for maior ou igual a zero, efetua o desvio, atualizando o PC para o novo endereço.
            if conteudo >= 0:
                self.registradores.set_registrador("PC", endereco_memoria)
        
        
    def executaAdd(self, endereco: str) -> None:
        '''
        Executa a instrução ADD M(X) (adiciona o conteúdo de M(X) ao AC).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", dado) # Move o dado lido para o MBR.
        # Obtém o conteúdo do MBR e do AC.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_ac = self.registradores.get_registrador("AC")
        # Verifica se ambos são inteiros para realizar a soma.
        if isinstance(conteudo_ac, int) and isinstance(conteudo_mbr, int):
            soma = conteudo_ac + conteudo_mbr
            self.registradores.set_registrador("AC", soma) # Armazena o resultado da soma em AC.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
    
    
    def executaAddImediato(self, dado: str) -> None:
        '''
        Executa a instrução ADD *dado* (endereçamento imediato).
        '''
        dado_int = int(dado) # Converte o dado para inteiro.
        self.registradores.set_registrador("MBR", dado_int) # Move o dado para MBR.
        # Obtém o conteúdo do MBR e do AC.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_ac = self.registradores.get_registrador("AC")
        # Verifica se ambos são inteiros para realizar a soma.
        if isinstance(conteudo_ac, int) and isinstance(conteudo_mbr, int):
            soma = conteudo_ac + conteudo_mbr
            self.registradores.set_registrador("AC", soma) # Armazena o resultado da soma em AC.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
            
            
    def executaAddAbs(self, endereco: str) -> None:
        '''
        Executa a instrução ADD |M(X)| (adiciona o valor absoluto de M(X) ao AC).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", abs(dado)) # Move o valor absoluto do dado lido para MBR.
        # Obtém o conteúdo do MBR e do AC.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_ac = self.registradores.get_registrador("AC")
        # Verifica se ambos são inteiros para realizar a soma.
        if isinstance(conteudo_ac, int) and isinstance(conteudo_mbr, int):
            soma = conteudo_ac + conteudo_mbr
            self.registradores.set_registrador("AC", soma) # Armazena o resultado da soma em AC.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
    
    
    def executaSub(self, endereco: str) -> None:
        '''
        Executa a instrução SUB M(X) (subtrai o conteúdo de M(X) do AC).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", dado) # Move o dado lido para o MBR.
        # Obtém o conteúdo do MBR e do AC.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_ac = self.registradores.get_registrador("AC")
        # Verifica se ambos são inteiros para realizar a subtração.
        if isinstance(conteudo_ac, int) and isinstance(conteudo_mbr, int):
            subtracao = conteudo_ac - conteudo_mbr
            self.registradores.set_registrador("AC", subtracao) # Armazena o resultado da subtração em AC.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
    
    
    def executaSubImediato(self, dado: str) -> None:
        '''
        Executa a instrução SUB *dado* (endereçamento imediato).
        '''
        dado_int = int(dado) # Converte o dado para inteiro.
        self.registradores.set_registrador("MBR", dado_int) # Move o dado para MBR.
        # Obtém o conteúdo do MBR e do AC.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_ac = self.registradores.get_registrador("AC")
        # Verifica se ambos são inteiros para realizar a subtração.
        if isinstance(conteudo_ac, int) and isinstance(conteudo_mbr, int):
            subtracao = conteudo_ac - conteudo_mbr
            self.registradores.set_registrador("AC", subtracao) # Armazena o resultado da subtração em AC.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
            
            
    def executaSubAbs(self, endereco: str) -> None:
        '''
        Executa a instrução SUB |M(X)| (subtrai o valor absoluto de M(X) do AC).
        X nesse caso é o *endereço*, representado por uma string hexadecimal. 
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", abs(dado)) # Move o valor absoluto do dado lido para MBR.
        # Obtém o conteúdo do MBR e do AC.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_ac = self.registradores.get_registrador("AC")
        # Verifica se ambos são inteiros para realizar a subtração.
        if isinstance(conteudo_ac, int) and isinstance(conteudo_mbr, int):
            subtracao = conteudo_ac - conteudo_mbr
            self.registradores.set_registrador("AC", subtracao) # Armazena o resultado da subtração em AC.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
    
    
    def executaMul(self, endereco: str) -> None:
        '''
        Executa a instrução MUL M(X) (multiplica MQ por M(X) e armazena o resultado em MQ).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", dado) # Move o dado lido para o MBR.
        # Obtém o conteúdo do MBR e do MQ.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_mq = self.registradores.get_registrador("MQ")
        # Verifica se ambos são inteiros para realizar a multiplicação.
        if isinstance(conteudo_mq, int) and isinstance(conteudo_mbr, int):
            produto = conteudo_mq * conteudo_mbr
            self.registradores.set_registrador("MQ", produto) # Armazena o resultado da multiplicação em MQ.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
    
    
    def executaMulImediato(self, dado: str) -> None:
        '''
        Executa a instrução MUL *dado* (endereçamento imediato).
        '''
        dado_int = int(dado) # Converte o dado para inteiro.
        self.registradores.set_registrador("MBR", dado_int) # Move o dado para MBR.
        # Obtém o conteúdo do MBR e do MQ.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_mq = self.registradores.get_registrador("MQ")
        # Verifica se ambos são inteiros para realizar a multiplicação.
        if isinstance(conteudo_mq, int) and isinstance(conteudo_mbr, int):
            produto = conteudo_mq * conteudo_mbr
            self.registradores.set_registrador("MQ", produto) # Armazena o resultado da multiplicação em MQ.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
            
            
    def executaDiv(self, endereco: str) -> None:
        '''
        Executa a instrução DIV M(X) (divide AC por M(X), quociente em AC, resto em R).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", dado) # Move o dado lido para o MBR.
        # Obtém o conteúdo do MBR e do AC.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_ac = self.registradores.get_registrador("AC")
        # Verifica se ambos são inteiros para realizar a divisão.
        if isinstance(conteudo_ac, int) and isinstance(conteudo_mbr, int):
            if conteudo_mbr == 0:
                print("\nERRO: Divisão por Zero! Instrução não Executada!")
                return
            quociente = conteudo_ac // conteudo_mbr # Divisão inteira
            resto = conteudo_ac % conteudo_mbr # Cálculo do resto
            self.registradores.set_registrador("AC", quociente) # Armazena o quociente em AC.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
            # Analisa o resto da divisão e atualiza o registrador R.
            self.analisa_resto(resto)
    
    
    def executaDivImediato(self, dado: str) -> None:
        '''
        Executa a instrução DIV *dado* (endereçamento imediato).
        '''
        dado_int = int(dado) # Converte o dado para inteiro.
        self.registradores.set_registrador("MBR", dado_int) # Move o dado para MBR.
        # Obtém o conteúdo do MBR e do AC.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_ac = self.registradores.get_registrador("AC")
        # Verifica se ambos são inteiros para realizar a divisão.
        if isinstance(conteudo_ac, int) and isinstance(conteudo_mbr, int):
            if conteudo_mbr == 0:
                print("\nERRO: Divisão por Zero! Instrução não Executada!")
                return
            quociente = conteudo_ac // conteudo_mbr # Divisão inteira
            resto = conteudo_ac % conteudo_mbr # Cálculo do resto
            self.registradores.set_registrador("AC", quociente) # Armazena o quociente em AC.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
            # Analisa o resto da divisão e atualiza o registrador R.
            self.analisa_resto(resto)
            
            
    def executaLSH(self):
        '''
        Executa a instrução LSH (Logical Shift Left - Deslocamento Lógico à Esquerda).
        Desloca o conteúdo do AC um bit para a esquerda.
        '''
        conteudo = self.registradores.get_registrador("AC") # Obtém o conteúdo do AC.
        # Realiza o deslocamento lógico à esquerda (multiplica por 2).
        novo_conteudo = conteudo << 1 
        self.registradores.set_registrador("AC", novo_conteudo) # Armazena o novo conteúdo em AC.
        # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
        self.analisa_resultado()
    
    
    def executaRSH(self):
        '''
        Executa a instrução RSH (Logical Shift Right - Deslocamento Lógico à Direita).
        Desloca o conteúdo do AC um bit para a direita.
        '''
        conteudo = self.registradores.get_registrador("AC") # Obtém o conteúdo do AC.
        # Realiza o deslocamento lógico à direita (divide por 2).
        novo_conteudo = conteudo >> 1
        self.registradores.set_registrador("AC", novo_conteudo) # Armazena o novo conteúdo em AC.
        # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
        self.analisa_resultado()
        # Analisa o resto da divisão e atualiza o registrador R.
        possivel_resto = conteudo % 2
        self.analisa_resto(possivel_resto)
        
    
    def executaAnd(self, endereco: str) -> None:
        '''
        Executa a instrução AND M(X).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.
        
        Esta é uma operação lógica binária. Ela realiza um AND bit a bit
        entre o valor no Acumulador (AC) e o valor na memória M(X). O resultado é
        armazenado de volta no AC.
        
        Exemplo: AC = 13 (1101), M(X) = 10 (1010)
        1101 & 1010 = 1000 (Resultado = 8)
        O AC é atualizado para 8.  
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", dado) # Move o dado lido para o MBR.
        # Obtém o conteúdo do MBR e do AC.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_ac = self.registradores.get_registrador("AC")
        # Verifica se ambos são inteiros para realizar a operação lógica.
        if isinstance(conteudo_ac, int) and isinstance(conteudo_mbr, int):
            resultado_and = conteudo_ac & conteudo_mbr # AND bit a bit.
            self.registradores.set_registrador("AC", resultado_and) # Armazena o resultado da operação em AC.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
        
        
    def executaOr(self, endereco: str) -> None:
        '''
        Executa a instrução OR M(X).
        X nesse caso é o *endereço*, representado por uma string hexadecimal.
        
        Esta é uma operação lógica binária. Ela realiza um OR bit a bit
        entre o valor no Acumulador (AC) e o valor na memória M(X). O resultado é
        armazenado de volta no AC.
        
        Exemplo: AC = 12 (1100), M(X) = 10 (1010)
        1100 | 1010 = 1110 (Resultado = 14)
        O AC é atualizado para 14.  
        '''
        dado = self.busca_dado(endereco) # Busca o dado na memória no endereço especificado.
        self.registradores.set_registrador("MBR", dado) # Move o dado lido para o MBR.
        # Obtém o conteúdo do MBR e do AC.
        conteudo_mbr = self.registradores.get_registrador("MBR")
        conteudo_ac = self.registradores.get_registrador("AC")
        # Verifica se ambos são inteiros para realizar a operação lógica.
        if isinstance(conteudo_ac, int) and isinstance(conteudo_mbr, int):
            resultado_or = conteudo_ac | conteudo_mbr # OR bit a bit.
            self.registradores.set_registrador("AC", resultado_or) # Armazena o resultado da operação em AC.
            # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
            self.analisa_resultado()
            
    
    def executaNot(self) -> None:
        '''
        Executa a instrução NOT, uma operação lógica unária.
        Inverte todos os bits do valor no Acumulador (AC) e armazena o resultado de volta no AC.
        '''
        conteudo = self.registradores.get_registrador("AC") # Obtém o conteúdo do AC.
        # Realiza a inversão dos bits do conteudo de AC (Operação NOT).
        novo_conteudo = ~conteudo 
        self.registradores.set_registrador("AC", novo_conteudo) # Armazena o novo conteúdo em AC.
        # Analisa o resultado no Acumulador para atualizar os registradores C e Z.
        self.analisa_resultado()    
        
        
    def analisa_resultado(self):
        '''
        Analisa o resultado do Acumulador e atualiza os registradores C e Z.
        '''
        conteudo = self.registradores.get_registrador("AC") # Obtém o conteúdo atual do AC.
        self.registradores.set_carry(conteudo)
        self.registradores.set_z(conteudo)
        
        
    def analisa_resto(self, resto: int):
        '''
        Analisa o resto de uma operação de divisão e o armazena em R.
        '''
        self.registradores.set_registrador("R", resto)
    
    
    def executa_instrucao(self):
        '''
        Executa um único ciclo de instrução (busca e execução).
        '''
        self.executa_busca() # Realiza o ciclo de busca.
        print("\n-----CICLO DE BUSCA-----\n")
        self.registradores.imprime_registradores()
        self.execucao() # Realiza o ciclo de execução.
        print("\n-----CICLO DE EXECUÇÃO-----\n")
        self.registradores.imprime_registradores()
        
        
    def executa_programa(self):
        '''
        Executa o programa completo, instrução por instrução, até o final.
        '''
        print("\n-----INÍCIO DOS REGISTRADORES-----\n")
        self.registradores.imprime_registradores()
        # Obtém a primeira instrução a ser executada (apontada pelo PC).
        instrucao = self.memoria.le_memoria(self.registradores.get_registrador("PC"))
        numero_instrucao = 1 # Contador de instruções.
        while instrucao:
            # Pausa a execução e aguarda o usuário pressionar Enter.
            input("\nDigite Enter para continuar: ")
            print(f"\n{numero_instrucao}º Instrução: ")
            self.executa_instrucao() # Executa um ciclo completo de instrução.
            # Cria/atualiza o arquivo 'simulador_memoria.txt' com o estado atual da memória.
            self.memoria.cria_arquivo_memoria()
            # Obtém a próxima instrução a ser executada (o PC já foi incrementado).
            instrucao = self.memoria.le_memoria(self.registradores.get_registrador("PC"))
            numero_instrucao += 1 # Incrementa o contador de instruções.



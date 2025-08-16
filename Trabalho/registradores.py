
'''
    Trabalho Prático
    Arquitetura e Organização de Computadores I
    Prof. Rodrigo Calvo

    Guilherme Jucoski da Silva - RA: 138642
    Ideraldo Luis Trentini Júnior - RA: 138318
    Matheus Henrique Borsato - RA: 138246
'''

# Classe Registradores: Simula os registradores da CPU. 
            
class Registradores:
    
    # Dicionário para armazenar os registradores e seus valores.
    registradores: dict[str, int|str] 
    
    # Construtor da Classe Registradores.
    def __init__(self, primeiro_endereco: int):
         
        self.registradores = {} # Inicializa o dicionário
        # PC (Program Counter): Armazena o endereço da próxima instrução a ser executada.
        # É inicializado com o endereço da primeira instrução.
        self.registradores["PC"] = primeiro_endereco
        # MAR (Memory Address Register): Armazena o endereço de memória a ser acessado.
        self.registradores["MAR"] = ''
        # MBR (Memory Buffer Register): Armazena dados e instruções
        self.registradores["MBR"] = ''
        # IR (Instruction Register): Armazena o código de operação (opcode) da instrução atual.
        self.registradores["IR"] = ''
        # C (Carry Flag): Flag de carry (1 se houver carry, 2 se não houver - padrão).
        self.registradores["C"] = 2
        # Z (Zero Flag): Flag de zero (0 se o resultado for zero, 1 se positivo, -1 se negativo).
        self.registradores["Z"] = 0
        # AC (Acumulador): Registrador de propósito geral para operações aritméticas e lógicas.
        self.registradores["AC"] = 0
        # MQ (Multiplicador): Usado em operações de multiplicação.
        self.registradores["MQ"] = 1
        # R (Remainder Register): Armazena o resto de operações de divisão.
        self.registradores["R"] = 0
       
       
    def set_registrador(self, nome: str, valor: str|int):
        '''
        Define o *valor* (int ou str) de um registrador específico (*nome*).
        '''
        # Verifica se o nome do registrador é válido.
        if nome not in self.registradores:
            raise KeyError(f"Registrador inválido: {nome}")
        self.registradores[nome] = valor
        
        
    def get_registrador(self, nome: str) -> int|str:
        '''
        Recupera o valor de um registrador específico (*nome*).
        '''
        # Verifica se o nome do registrador é válido.
        if nome not in self.registradores:
            raise KeyError(f"Registrador inválido: {nome}")
        return self.registradores[nome]
    
    
    def incrementa_pc(self):
        '''
        Incrementa o Program Counter (PC) em 1.
        '''
        self.registradores["PC"] += 1
  

    def set_carry(self, resultado: int):
        '''
        Define a flag de Carry (C) com base em *resultado*.
        '''
        # Se o resultado exceder o limite de 2^40 - 1, define que houve Carry.
        if resultado > 2**40 - 1:
            self.registradores["C"] = 1
            print("\nCarry no Acumulador!")
        else:
            self.registradores["C"] = 2
        
        
    def set_z(self, resultado: int):
        '''
        Define a flag de Zero (Z) com base em *resultado*.
        '''
        if resultado < 0:
            self.registradores["Z"] = -1 # Resultado negativo
        elif resultado == 0:
            self.registradores["Z"] = 0 # Resultado nulo
        else:
            self.registradores["Z"] = 1 # Resultado positivo

    
    def imprime_registradores(self):
        '''
        Imprime o estado atual de todos os registradores.
        '''
        for elemento in self.registradores.keys():
            if self.registradores[elemento] != '':
                if elemento in ["PC", "MAR"]: # Formata a impressão para PC e MAR em hexadecimal.
                    print(f"{elemento}: 0x{self.registradores[elemento]:02X}")
                else: # Imprime os outros registradores com base em seus conteúdos.
                    print(elemento + ":", self.registradores[elemento])
            else: # Se o registrador estiver vazio, imprime apenas o nome.
                print(elemento + ":")
                
                
                
          
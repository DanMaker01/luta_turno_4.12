from database import Database

class Timeline:
    def __init__(self):
        self.estados_base = ["base_parado"] #inicialmente o player está parado
        self.estados_guarda = ["guarda_parado"] # inicialmente o player está parado
        self.movimentos_a_fazer = []
        self.movimento_classe = Database()
        # self.flag_adicionou_movimento = False

    def add_base_to_timeline(self, estado_objetivo):
        self.movimentos_a_fazer = [] #limpa a sequencia de movimentos a fazer
        estado_atual = self.estados_base[-1] # pega o estado atual
        
        menor_sequencia_ate_objetivo = self.movimento_classe.get_menor_sequencia(estado_atual, estado_objetivo)
        
        #verifica se você já está na posição inicial do movimento
        if estado_atual == menor_sequencia_ate_objetivo[0]:
            # retorna a menor_sequencia_ate_objetivo sem o primeiro item
            self.movimentos_a_fazer= menor_sequencia_ate_objetivo[1:]
        else:
            self.movimentos_a_fazer = menor_sequencia_ate_objetivo

    def add_guarda_to_timeline(self, estado_objetivo):
        self.movimentos_a_fazer = []
        #IMPLEMENTAR @@@

    #implementar: talvez precise adicionar um terceiro caso, se não for base nem guarda??
    def add_movimento_to_timeline(self, estado_objetivo):
        #se for movimento de base:
        print(estado_objetivo)

        if self.movimento_classe.MOVEMENTS[estado_objetivo][0] == 0:
            self.add_base_to_timeline( estado_objetivo)
            # self.flag_adicionou_movimento = True
        else:#senão é movimento de guarda
            self.add_guarda_to_timeline(estado_objetivo)
            # self.flag_adicionou_movimento = True
        
    def avancar_movimentos(self):
        # ???? explicar melhor
        pass


    def executar_movimentos(self): # transfere movimento a fazer para timeline.estados_base 
        if self.movimentos_a_fazer:
            proximo_estado = self.movimentos_a_fazer.pop(0)
            #implementar: mudar sprite do player
            self.estados_base.append(proximo_estado)
        else:
            # se não houver movimentos a fazer, adiciona-se repetidamente o ultimo estado
            self.estados_base.append(self.estados_base[-1])
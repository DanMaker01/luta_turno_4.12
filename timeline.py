from movements import Movement

class Timeline:
    def __init__(self):
        self.estados_base = ["base_parado"]
        self.estados_guarda = ["guarda_parado"]
        self.movimentos_a_fazer = []
        self.movimento_classe = Movement()
        

    def add_base_to_timeline(self, estado_objetivo):
        self.movimentos_a_fazer = []
        estado_atual = self.estados_base[-1]
        
        menor_sequencia_ate_objetivo = self.movimento_classe.get_menor_sequencia(estado_atual, estado_objetivo)
        
        #verifica se você já está na posição inicial do movimento
        if estado_atual == menor_sequencia_ate_objetivo[0]:
            # retorna a menor_sequencia_ate_objetivo sem o primeiro item
            self.movimentos_a_fazer= menor_sequencia_ate_objetivo[1:]
        else:
            self.movimentos_a_fazer = menor_sequencia_ate_objetivo

    def add_guarda_to_timeline(self, estado_objetivo):
        self.movimentos_a_fazer = []

    def add_movimento_to_timeline(self, estado_objetivo):
        #se dor movimento de base:
        if self.movimento_classe.MOVEMENTS[estado_objetivo][0] == 0:
            self.add_base_to_timeline( estado_objetivo)
        else:#senão é movimento de guarda
            self.add_guarda_to_timeline(estado_objetivo)

    def avancar_movimentos(self):
        #implementar
        pass

    def executar_movimentos(self):
        if self.movimentos_a_fazer:
            proximo_estado = self.movimentos_a_fazer.pop(0)
            self.estados_base.append(proximo_estado)
        else:
            pass
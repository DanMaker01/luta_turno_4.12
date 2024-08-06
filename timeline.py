from database import Database

class Timeline:
    def __init__(self):
        self.estados_base = ["base_parado"] #inicialmente o player está parado
        self.estados_guarda = ["guarda_parado"] # inicialmente o player está parado
        self.movimentos_a_fazer = []
        self.database = Database()
        # self.flag_adicionou_movimento = False

    def add_base_to_timeline(self, estado_objetivo):
        self.movimentos_a_fazer = [] #limpa a sequencia de movimentos a fazer
        estado_atual = self.estados_base[-1] # pega o estado atual
        
        menor_sequencia_ate_objetivo = self.database.get_menor_sequencia(estado_atual, estado_objetivo)
        
        #verifica se você já está na posição inicial do movimento
        if estado_atual == menor_sequencia_ate_objetivo[0]:
            # retorna a menor_sequencia_ate_objetivo sem o primeiro item
            self.movimentos_a_fazer= menor_sequencia_ate_objetivo[1:]
        else:
            self.movimentos_a_fazer = menor_sequencia_ate_objetivo

    def add_guarda_to_timeline(self, estado_objetivo):
        self.movimentos_a_fazer = []
        #IMPLEMENTAR @@@
        estado_atual = self.estados_guarda[-1]
        menor_sequencia_ate_objetivo = self.database.get_menor_sequencia_guarda(estado_atual, estado_objetivo)
        # menor_sequencia_ate_objetivo = self.database.get_menor_sequencia(estado_atual, estado_objetivo)
        # self.movimentos_a_fazer = menor_sequencia_ate_objetivo




    #implementar: talvez precise adicionar um terceiro caso, se não for base nem guarda??
    def add_movimento_to_timeline(self, movimento):
        ultima_base = self.estados_base[-1]
        # ultima_guarda = self.estados_guarda[-1]

        print("movimento:", movimento)
        # se a string começa com "ataque":
        if movimento.startswith("ataque"):
            print("ataque:")
            # se tiver na base de chute sai chute
            # se tiver com guarda ou defesa sai soco
            if ultima_base == "base_chute":
                if movimento == "ataque_leve":
                    # print("chute leve!")
                    self.add_guarda_to_timeline("chute_frente")
                else:
                    # print("chute pesado!")
                    self.add_guarda_to_timeline("chute_tras")
            else:
                print("soco!")
                if movimento == "ataque_leve":
                    # print("soco leve!")
                    self.add_guarda_to_timeline("soco_frente")
                else:
                    # print("soco pesado!")
                    self.add_guarda_to_timeline("soco_tras")
        elif movimento.startswith("base"):
            print("base!")
            self.add_base_to_timeline(movimento)
        elif movimento.startswith("mover"):
            print("mover!")
        print("")


        # if(estado_objetivo == "mover_avancar" or estado_objetivo == "mover_recuar"):
        #     print("movimento!")
        #     if( estado_objetivo == "mover_avancar"):


        # elif self.database.MOVEMENTS[estado_objetivo][0] == 0:
        #     print("base!")
        #     self.add_base_to_timeline( estado_objetivo)
        #     # self.flag_adicionou_movimento = True
        # else:#senão é movimento de guarda
        #     print("guarda!")
        #     self.add_guarda_to_timeline(estado_objetivo)
        #     # self.flag_adicionou_movimento = True
        
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
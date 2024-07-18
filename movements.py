



class Movement:
    ESTADOS_BASE = ["base_parado","base_agachado", "base_zenkutsu",  "base_cavaleiro","base_kokutsu", "base_chute","chute_frente","chute_lateral"]
    #ESTADOS_GUARDA = ["guarda_parado", "guarda_guarda", "soco_frente", "soco_tras","def_baixo", "def_alto"]

    MATRIZ_TRANSICAO_BASE = [
        [0,2,0,0,0,0,0,0],
        [0,0,3,2,2,3,0,0],
        [0,1,0,3,1,3,0,0],
        [0,1,2,0,2,3,0,0],
        [0,2,1,3,0,2,0,0],
        [0,1,2,3,2,0,1,2],
        [0,0,0,0,0,1,0,0],
        [0,0,0,0,0,1,0,0]
    ]

    
    
    MOVEMENTS = {
        "base_parado": [0, 0, 0, []],
        "base_zenkutsu": [0],
        "base_kokutsu": [0],
        "base_cavaleiro": [0],
        "base_chute": [0],
        "guarda_parado": [1, 0, 0, []],
        "soco_frente": [1, 10, 3, ["base", "tronco", "braco"]],
        "soco_tras": [1, 17, 4, ["base", "tronco", "braco"]],
        "defesa_baixo": [3, -10, 1, ["tronco", "braco"]],
        "defesa_alta": [3, -10, 2, ["tronco", "braco"]],
        "chute_frente": [3, 22, 3, ["tronco", "base"]],
        "chute_tras": [3, 20, 3, ["tronco", "base"]],
        "mover_avancar": [3, 0, 3, ["base"]],
        "mover_recuar": [3, 0, 3, ["base"]],
        "strafe_cima": [3, 0, 3, ["base"]],
        "strafe_baixo": [3, 0, 3, ["base"]],
    }


    def __init__(self):
        pass


    def add_estado_n_vezes(self, sequencia, estado , n):
        for _ in range(n): #adicionar estado inicial n vezes
                sequencia.append(estado)
        return sequencia

    def verifica_distancia(self, estado_inicial, estado_final):
        indice_estado_inicial = self.ESTADOS_BASE.index(estado_inicial)
        indice_estado_final = self.ESTADOS_BASE.index(estado_final)
        return self.MATRIZ_TRANSICAO_BASE[indice_estado_inicial][indice_estado_final]
    
    def get_menor_sequencia(self, estado_inicial, estado_final):
        sequencia = []
        distancia_inicial_final = self.verifica_distancia(estado_inicial, estado_final)
        indice_estado_inicial = self.ESTADOS_BASE.index(estado_inicial)
        indice_estado_final = self.ESTADOS_BASE.index(estado_final)

        if (distancia_inicial_final > 0): #dist > 0, transição direta.
            sequencia = self.add_estado_n_vezes(sequencia, estado_inicial, distancia_inicial_final)
            sequencia.append(estado_final)
            return sequencia
        else: #dist = 0, transição indireta
            menor_distancia_total = 999
            sequencia_b = []
            parcial_utilizado = ""
            # para cada valor não nulo na linha do estado_inicial
            for i in range(len(self.MATRIZ_TRANSICAO_BASE[indice_estado_inicial])):
                distancia_inicial_parcial = self.verifica_distancia(estado_inicial, self.ESTADOS_BASE[i])
                if (distancia_inicial_parcial > 0): # se dist não nula, verifica a dist parcial->final
                    distancia_parcial_final = self.verifica_distancia(self.ESTADOS_BASE[i], estado_final)
                    distancia_total_candidata = distancia_inicial_parcial+distancia_parcial_final
                    if(distancia_total_candidata < menor_distancia_total):
                        menor_distancia_total = distancia_total_candidata
                        parcial_utilizado = self.ESTADOS_BASE[i]
                        sequencia_b = self.get_menor_sequencia(self.ESTADOS_BASE[i], estado_final)
                    
                else:
                    pass
                pass
            sequencia = self.add_estado_n_vezes(sequencia, estado_inicial, self.verifica_distancia(estado_inicial, parcial_utilizado))
            sequencia = sequencia + sequencia_b

            return sequencia

                

            
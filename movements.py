



class Movement:
    ESTADOS_BASE = ["parado","agachado", "zenkutsu",  "cavaleiro","kokutsu", "chute","chute_frente","chute_lateral"]
    #ESTADOS_GUARDA = ["parado", "guarda", "soco_frente", "soco_tras","def_baixo", "def_alto"]

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

    def __init__(self):
        pass


    def add_estado_n_vezes(self, sequencia, estado , n):
        for _ in range(n): #adicionar estado inicial n vezes
                sequencia.append(estado)
        return sequencia

    def verifica_distancia(self, estado_inicial, estado_final):
        return Movement.MATRIZ_TRANSICAO_BASE[estado_inicial][estado_final]
    
    def get_menor_sequencia(self, estado_inicial, estado_final):
        sequencia = []
        distancia_inicial_final = self.verifica_distancia(estado_inicial, estado_final)
        
        if (distancia_inicial_final > 0): #dist > 0, transição direta.
            sequencia = self.add_estado_n_vezes(sequencia, estado_inicial, distancia_inicial_final)
            sequencia.append(estado_final)
            return sequencia
        else: #dist = 0, transição indireta
            menor_distancia_parcial_final = 999
            sequencia_b = []
            for estado_parcial in self.ESTADOS_BASE:
                distancia_inicial_parcial = self.verifica_distancia(estado_inicial, estado_parcial)
                if (distancia_inicial_parcial > 0):
                    distancia_parcial_final = self.verifica_distancia(estado_parcial, estado_final)
                    if(distancia_parcial_final < menor_distancia_parcial_final):
                        sequencia_b = []
                        menor_distancia_parcial_final = distancia_parcial_final
                        sequencia_b = self.add_lei_n_vezes(sequencia, estado_inicial, distancia_inicial_parcial)
                        sequencia_b.append(estado_parcial)
# CONTINUAR
                    
                    

                

            
    MOVEMENTS = {
        "base_parado": [0, 0, 0, []],
        "guarda_parado": [1, 0, 0, []],
        "inter": [1, 0, 0, []],
        "base_zenkutsu": [2, 0, 1, ["base"]],
        "base_kokutsu": [1, 0, 3, ["base"]],
        "base_cavaleiro": [2, 0, 2, ["base"]],
        "base_chute": [3, 0, 2, ["base"]],
        "ataque_leve": [2, 5, 3, ["braco"]],
        "ataque_forte": [3, 10, 4, ["braco"]],
        "soco_frente": [2, 10, 3, ["base", "tronco", "braco"]],
        "soco_tras": [4, 17, 4, ["base", "tronco", "braco"]],
        "chute_frente": [3, 22, 3, ["tronco", "base"]],
        "chute_tras": [3, 20, 3, ["tronco", "base"]],
        "defesa_baixo": [3, -10, 1, ["tronco", "braco"]],
        "defesa_alta": [3, -10, 2, ["tronco", "braco"]],
        "mover_avancar": [3, 0, 3, ["base"]],
        "mover_recuar": [3, 0, 3, ["base"]],
        "strafe_cima": [3, 0, 3, ["base"]],
        "strafe_baixo": [3, 0, 3, ["base"]],
        "rikite": [1, 0, 2, ["braco"]]
    }

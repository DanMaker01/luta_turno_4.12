



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

    
    def get_menor_sequencia(self, estado_inicial, estado_final):
        sequencia = []
        linha = self.ESTADOS_BASE.index(estado_inicial)
        coluna = self.ESTADOS_BASE.index(estado_final)
        n = self.MATRIZ_TRANSICAO_BASE[linha][coluna]
        menor_n = 999

        if  n > 0: # se houver transicao direta
            sequencia = self.add_estado_n_vezes(sequencia, estado_inicial, n)
            sequencia.append(estado_final)
            return sequencia
        else: #senao, abrir possibilidades recursivamente e testar se há transicao direta de segundo nivel
            print("transicao indireta")
            for estado in self.ESTADOS_BASE:
                 seq2 = self.get_menor_sequencia(estado, estado_final)
                 if len(seq2) < menor_n:
                    menor_n = len(seq2)
                    sequencia = seq2#
            


            return sequencia
        

            
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
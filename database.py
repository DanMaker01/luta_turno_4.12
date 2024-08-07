

class Database:
    ESTADOS_BASE = ["base_parada",
                    "base_agachado", 
                    "base_zenkutsu",  
                    "base_cavaleiro",
                    "base_kokutsu", 
                    "base_chute",
                    "chute_frente",
                    "chute_lateral"]
    
    BASE_CENTRO_COLUNA = [127,127,127,127,64,127,85,64]
    
    ESTADOS_GUARDA = ["guarda_parada", 
                      "guarda_guarda", 
                      "soco_frente", 
                      "soco_tras",
                      "guarda_defesa_baixa", 
                      "guarda_defesa_alta"]


    MATRIZ_TRANSICAO_BASE = [ #8x8 (numeros de estados base)
        [0,2,0,0,0,0,0,0],
        [0,0,3,2,2,3,0,0],
        [0,1,0,3,1,3,0,0],
        [0,1,2,0,2,3,0,0],
        [0,2,1,3,0,2,0,0],
        [0,1,2,3,2,0,1,2],
        [0,0,0,0,0,1,0,0],
        [0,0,0,0,0,1,0,0]
    ]
    MATRIZ_TRANSICAO_GUARDA = [ #9x9
        [0,1,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,0],
        [0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0],
        [0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0]
    ]
    
    MOVEMENTS_COMANDS = { #implementar: acertar o formato padrão
        "base_parada" : ['z','z'],
        "base_zenkutsu" : ['z','right'],
        "base_kokutsu" : ['z','left'],
        "base_chute" : ['z','up'],
        "base_cavaleiro" : ['z','down'],

        "guarda_parada" : ['a','a'],
        "ataque_leve" : ['a','right'],
        "ataque_pesado" : ['a','left'],
        "guarda_defesa_alta" : ['a','up'],
        "guarda_defesa_baixa" : ['a','down'],

        "mover_esquerda" : ['left'],
        "mover_direita" : ['right'],
        "mover_strafe_cima" : ['up'],
        "mover_strafe_baixo" : ['down'],

        "mover_direita2" : ['right','right'],
        "mover_esquerda2": ['left','left'],
        "mover_esquerda_direita" : ['left','right'],
        "mover_direita_esquerda" : ['right','left'],
    }

    def check_movements(self, sequence):
        for movement, seq in self.MOVEMENTS_COMANDS.items():
            if sequence == seq:
                return movement
        return None

    def __init__(self):
        pass


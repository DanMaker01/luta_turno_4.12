
class Database:
    TEMPO = 6 # a cada 5 frames atualiza-se o jogo
    # controlar o tempo de atualização do jogo
    # tempo de atualização

    # BASE_CENTRO_COLUNA = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]

    ESTADOS_BASE = ["base_parado",
                    "base_agachado", 
                    "base_zenkutsu",  
                    "base_cavaleiro",
                    "base_kokutsu", 
                    "base_chute",
                    "chute_frente",
                    "chute_lateral"]
    
    MATRIZ_TRANSICAO_BASE = [ #8x8 (numeros de estados base)
        [0,4,0,0,0,0,0,0], 
        [3,0,6,4,4,6,0,0],
        [3,2,0,0,0,0,0,0],
        [3,2,0,0,0,0,0,0],
        [3,4,0,0,0,0,0,0],
        [3,2,4,6,4,0,2,4],
        [3,0,0,0,0,2,0,0],
        [3,0,0,0,0,2,0,0]
    ]

    
    ESTADOS_GUARDA = ["guarda_parado", 
                      "guarda_guarda", 
                      "soco_frente", 
                      "soco_tras",
                      "guarda_defesa_baixo", 
                      "guarda_defesa_alto"]

    MATRIZ_TRANSICAO_GUARDA = [ #6x6 
        [0,3,0,0,0,0],
        [3,0,2,4,6,6],
        [3,2,0,0,0,0],
        [3,2,0,0,0,0],
        [3,2,0,0,0,0],
        [3,2,0,0,0,0]
    ]
    
    MOVEMENTS_COMANDS = { # é necessario ordenar por tamanho de sequencia, decrescente
        # tamanho 4
        "postura_g_b": ['a','a','z'],
        "postura_b_g": ['z','z','a'],

        # tamanho 2
        "postura_para": ['z','a'],
        "postura_para2": ['a','z'],

        "base_agachado" :     ['z','z'],
        "base_zenkutsu" :   ['z','right'],
        "base_kokutsu" :    ['z','left'],
        "base_chute" :      ['z','up'],
        "base_cavaleiro" :  ['z','down'],

        "guarda_guarda" :       ['a','a'],
        "guarda_defesa_alto" :  ['a','up'],
        "guarda_defesa_baixo" : ['a','down'],

        
        "ataque_leve" :     ['a','right'],
        "ataque_pesado" :   ['a','left'],

        "mover_direita2" :          ['right','right'],
        "mover_esquerda2":          ['left','left'],
        "mover_esquerda_direita" :  ['left','right'],
        "mover_direita_esquerda" :  ['right','left'],

        #tamanho 1
        "mover_esquerda" :      ['left'],
        "mover_direita" :       ['right'],
        "mover_strafe_cima" :   ['up'],
        "mover_strafe_baixo" :  ['down'],


    }

    def check_movements(self, sequence):
        for movement, seq in self.MOVEMENTS_COMANDS.items():
            if sequence == seq:
                return movement
        return None

    def __init__(self):
        pass


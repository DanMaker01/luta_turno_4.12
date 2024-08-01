import numpy as np
from movements import Database
class Player:
    def __init__(self, sprites_base, sprites_guarda, pos, estado_inicial):
        self.sprites_base = sprites_base #dicionario
        self.sprites_guarda = sprites_guarda # implementar @@@@
        
        self.pos = pos
        
        self.estado = estado_inicial
        pass

    def draw(self, screen):
        #editar: desenhar base; desenhar guarda na posição em relação à base
        
        screen.blit(self.sprites_base[self.estado[0]], self.pos)



        altura_sprite = self.sprites_base[self.estado[0]].get_height()
        # implementar: a posição varia de acordo com a base.
        screen.blit(self.sprites_guarda[self.estado[1]], self.pos+np.array([0, -altura_sprite]))
        
        


    def trocar_estado(self, estado_novo):
        self.estado = estado_novo


    def update(self):
    
        pass
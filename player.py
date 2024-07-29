class Player:
    def __init__(self, image, pos, estado_inicial):
        self.image = image
        self.pos = pos
        self.estado = estado_inicial

    def draw(self, screen):
        #editar: desenhar base; desenhar guarda na posição em relação à base
        screen.blit(self.image, self.pos)
        


    def trocar_estado(self, estado_novo):
        self.estado = estado_novo


    # def update(self):
    #     self.estado[0] = self.estado[0]
    #     self.estado[1] = self.estado[1]
    #     pass
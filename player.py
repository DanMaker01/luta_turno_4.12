class Player:
    def __init__(self, image, pos, estado_inicial):
        self.image = image
        self.pos = pos
        self.estado = estado_inicial

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    def update(self):
        pass
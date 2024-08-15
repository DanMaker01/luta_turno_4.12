import pygame
import database

class ResourceLoader:

    #init

    def __init__(self):
        self.database = database.Database()
        
        self.bg = ['bg',self.load_image("bg.png")]
        
        self.bases = []
        for base in self.database.ESTADOS_BASE:
            self.bases.append([base,self.load_image(base+".png")])
        
        self.guardas= []
        for guarda in self.database.ESTADOS_GUARDA:
            self.guardas.append([guarda,self.load_image(guarda+".png")])
        
        print("recursos carregados")

        pygame.mixer.init()

    @staticmethod
    def load_image(nome,path="recursos/"):
        return pygame.image.load(path+nome)

    @staticmethod
    def load_sound(nome,path="recursos/"):
        return pygame.mixer.Sound(path+nome)

    @staticmethod
    def scale_image(image, scale):
        width, height = image.get_size()
        new_size = (int(width * scale), int(height * scale))
        return pygame.transform.scale(image, new_size)

    def get_image(self, nome):
        return self.objs
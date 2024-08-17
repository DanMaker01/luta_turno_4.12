import pygame
import database

class ResourceLoader:

    #init

    def __init__(self):
        self.database = database.Database()
        
        self.bg = ['bg',self.load_image("bg.png")]
        
        self.bases = []
        for base in self.database.ESTADOS_BASE:
            self.bases.append([base,self.scale_image(self.load_image(base+".png"),0.5)])
        
        self.guardas= []
        for guarda in self.database.ESTADOS_GUARDA:
            self.guardas.append([guarda,self.scale_image(self.load_image(guarda+".png"),0.5)])
        
        # print("recursos carregados")

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

    def get_bg_img(self):
        return self.bg
    def get_base_img(self, nome):
        return self.bases[self.database.ESTADOS_BASE.index(nome)][1]
    def get_guarda_img(self,nome):
        return self.guardas[self.database.ESTADOS_GUARDA.index(nome)][1]
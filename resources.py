import pygame
class ResourceLoader:
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

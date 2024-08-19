import pygame
import database
from input import KeySequenceDetector
from timeline import Timeline
from resources import ResourceLoader
from game_logic import GameLogic
from renderer import Renderer
import os

# Define a posição da janela (x, y)
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,32"
class Game:
    def __init__(self, width=640, height=480):

        
        pygame.init()
        pygame.display.set_caption("Jogo luta em turno")
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont(None, 20)

        self.database = database.Database()

        self.movimentos_possiveis = self.database.MOVEMENTS_COMANDS.values()
        

        self.detector = KeySequenceDetector(self.movimentos_possiveis)
        self.timeline = Timeline()
        self.recursos = ResourceLoader()

        self.logic = GameLogic(self.timeline, self.database)
        self.renderer = Renderer(self.screen, self.font, self.recursos, self.timeline, self.database, self.detector, width, height)
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.detector.handle_keydown(event.key)

    def run(self):
        while self.running:
            self.handle_events()
            comando, tempo_entre_comandos = self.detector.check_sequences()
            if comando:  # se a sequência for detectada
                self.timeline.pilha_add(comando)
            self.logic.update()
            self.renderer.draw()
            self.clock.tick(60)  # Verifica a cada frame (60 vezes por segundo)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

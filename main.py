import pygame
import database
from input import KeySequenceDetector
from timeline import Timeline
from resources import ResourceLoader
from game_logic import GameLogic
from renderer import Renderer
from event_handler import EventHandler

class Game:
    def __init__(self, width=640, height=480):
        pygame.init()
        pygame.display.set_caption("Jogo luta em turno")
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((width, height))
        self.font = pygame.font.SysFont(None, 20)

        self.predefined_sequences = [
            # 3 teclas
            ['a', 'a', 'a'],

            # 2 teclas
            ['a', 'a'],
            ['a', 'left'],
            ['a', 'right'],
            ['a', 'up'],
            ['a', 'down'],

            ['z', 'z'],
            ['z', 'left'],
            ['z', 'right'],
            ['z', 'up'],
            ['z', 'down'],

            ['left', 'left'],
            ['right', 'right'],
            ['left', 'right'],
            ['right', 'left'],
            
            # 1 tecla
            ['left'],
            ['right'],
            ['up'],
            ['down'],
        ]

        self.detector = KeySequenceDetector(self.predefined_sequences)
        self.timeline = Timeline()
        self.database = database.Database()
        self.recursos = ResourceLoader()

        self.event_handler = EventHandler(self.detector)
        self.logic = GameLogic(self.timeline)
        self.renderer = Renderer(self.screen, self.font, self.recursos, self.timeline, self.database,width,height)
        self.clock = pygame.time.Clock()

    def run(self):
        while self.event_handler.running:
            self.event_handler.handle_events()
            comando, b = self.detector.check_sequences()
            if comando:  # se a sequência for detectada
                self.timeline.pilha_add(comando)
            self.logic.update()
            self.renderer.draw()
            self.clock.tick(60)  # Verifica a cada frame (60 vezes por segundo)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

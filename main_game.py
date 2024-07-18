import pygame
import sys
from player import Player
from movements import Movement
from timeline import Timeline
from resources import ResourceLoader
from input_manager import InputManager

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Luta_turno")

class Game:
    def __init__(self):
        self.running = True
        self.loader = ResourceLoader()
        self.player_image = self.loader.scale_image(self.loader.load_image('player.png'), 0.2)
        self.background_image = self.loader.scale_image(self.loader.load_image('background.png'), 1)
        
        pygame.mixer.init()
        self.move_sound = self.loader.load_sound('beep.mp3')
        self.player = Player(self.player_image, [0, HEIGHT - self.player_image.get_height()], [Movement.MOVEMENTS["guarda_parado"], Movement.MOVEMENTS["base_parado"]])
        self.clock = pygame.time.Clock()

        self.t = 0
        self.intervalo_turno = 40
        self.turno = 0
        self.timeline = Timeline()

        self.input_manager = InputManager()

        pygame.font.init()
        self.font = pygame.font.SysFont(None, 20)
        self.movimentos = Movement()
        # a = self.movimentos.get_menor_sequencia("chute_frente", "zenkutsu")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.input_manager.handle_keydown(event.key)

            self.update()
            self.player.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def avancar_tempo(self):
        self.t += 1
        pass

    def avancar_turno(self):
        self.timeline.executar_movimentos()
        self.turno += 1

    def update(self):
        self.avancar_tempo()
        self.input_manager.check_sequences(self.timeline)
        self.input_manager.buffer_update()
        if self.t % self.intervalo_turno == 0:
            self.avancar_turno()

    def draw(self):
        screen.blit(self.background_image, (0, 0))
        self.player.draw(screen)
        self.draw_last_elements()
        pygame.display.flip()

    def draw_last_elements(self):
        last_elements = self.input_manager.buffer[-3:]
        for i, element in enumerate(last_elements):
            text_surface = self.font.render(str(element), True, (255, 255, 255))
            screen.blit(text_surface, (10, 50 + i * 30))

        # Display current turn
        turn_text = self.font.render(f"Turno: {self.turno}", True, (255, 255, 255))
        screen.blit(turn_text, (10, 10))

        # Display timeline.estados_base
        movimentos_text = self.font.render(f"Movimentos: {self.timeline.estados_base}", True, (255, 255, 255))
        screen.blit(movimentos_text, (5, 50))

        #display timeline.movimentos_a_fazer
        movimentos_a_fazer_text = self.font.render(f"Movimentos a fazer: {self.timeline.movimentos_a_fazer}", True, (255, 255, 255))
        screen.blit(movimentos_a_fazer_text, (5, 100))

if __name__ == "__main__":
    game = Game()
    game.run()

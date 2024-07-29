# # # # # # # # # # # # # # # # # # # # # # # # # 
# Luta Turno
# https://github.com/danmaker01/luta_turno
# danmaker01
# 2024
# # # # # # # # # # # # # # # # # # # # # # # # # 
# Jogo de luta em turno ABS
# O objetivo é passar a sensação do ritmo de uma luta
# com movimentação, ataque e defesa, antecipação e gingado.


import pygame
import sys
from player import Player
from movements import Movement
from timeline import Timeline
from resources import ResourceLoader
from input_manager import InputManager

WIDTH, HEIGHT = 1240, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Luta_turno")

class Game:
    def __init__(self):
        self.running = True
        #database
        self.movimentos = Movement() #editar: Movement vai virar Base de Dados
        #resources
        self.loader = ResourceLoader()
        ##som
        self.move_sound = self.loader.load_sound('beep.mp3')
        ##sprites
        self.sprites_base = []
        self.sprites_guarda = []
        for i in self.movimentos.ESTADOS_BASE:
            self.sprites_base.append(self.loader.load_image(i+".png"))
        
        self.background_image = self.loader.scale_image(self.loader.load_image('background.png'), 1)
        #to-do: deletar player_image
        self.player_image = self.loader.scale_image(self.loader.load_image('player.png'), 0.2)
        
        #objetos
        #implementar: na hora de criar o Player, passar imagem da base e da guarda ao invés de imagem_player
        self.player = Player(self.player_image, 
                             [0, HEIGHT - self.player_image.get_height()], 
                             [Movement.MOVEMENTS["guarda_parado"], Movement.MOVEMENTS["base_parado"]])
        
        
        #tempo
        self.clock = pygame.time.Clock()
        self.t = 0
        self.intervalo_turno = 40
        self.turno = 0
        self.timeline = Timeline()

        #input
        self.input_manager = InputManager()

        #hud
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 20)
        # a = self.movimentos.get_menor_sequencia("chute_frente", "zenkutsu")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.input_manager.handle_keydown(event.key)

            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def avancar_tempo(self):
        self.t += 1
        pass

    def avancar_turno(self):

        self.timeline.executar_movimentos()
        self.player.trocar_estado([self.timeline.estados_base[-1], self.timeline.estados_guarda[-1]])
        self.turno += 1

    def update(self):
        self.avancar_tempo()
        self.input_manager.check_sequences(self.timeline) #aqui adiciona-se na timeline
        self.input_manager.buffer_update() #nao mexer
        if self.t % self.intervalo_turno == 0:
            self.avancar_turno()
        
        # self.player.update()

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
        movimentos_text = self.font.render(f"Timeline_base: {self.timeline.estados_base}", True, (255, 255, 255))
        screen.blit(movimentos_text, (5, 50))

        #display timeline.movimentos_a_fazer
        movimentos_a_fazer_text = self.font.render(f"Movimentos a fazer: {self.timeline.movimentos_a_fazer}", True, (255, 255, 255))
        screen.blit(movimentos_a_fazer_text, (5, 100))

        #mostrar player.base_atual
        base_text = self.font.render(f"Estado atual: {self.player.estado}", True, (255, 255, 255))
        screen.blit(base_text, (5, 150))

if __name__ == "__main__":
    game = Game()
    game.run()

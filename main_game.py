
import pygame
import sys
from player import Player
from database import Database
from timeline import Timeline
from resources import ResourceLoader
from input_manager import InputManager

screen = pygame.display.set_mode((Database.WIDTH, Database.HEIGHT))
pygame.display.set_caption("Luta_turno")

class Game:
    def __init__(self):
        self.running = True
        #database
        self.movimentos = Database() #editar: Database vai virar Base de Dados
        #resources
        self.loader = ResourceLoader()
        ##som
        self.move_sound = self.loader.load_sound('beep.mp3')
        ##sprites
        self.background_image = self.loader.scale_image(self.loader.load_image('background.png'), 1)
        
        self.sprites_base = {}
        self.sprites_guarda = {}
        for nome_i in self.movimentos.ESTADOS_BASE:
            self.sprites_base[nome_i] = self.loader.scale_image(self.loader.load_image(nome_i+".png"),0.5)
        for nome_i in self.movimentos.ESTADOS_GUARDA:
            self.sprites_guarda[nome_i] = self.loader.scale_image(self.loader.load_image(nome_i+".png"),0.5)

        # #to-do: deletar player_image
        # self.player_image = self.loader.scale_image(self.loader.load_image('player.png'), 1)
        
        #objetos
        #implementar: na hora de criar o Player, passar imagem da base e da guarda ao invés de imagem_player
        self.player = Player(self.sprites_base,
                             self.sprites_guarda, 
                             [0, Database.HEIGHT - self.sprites_base[Database.ESTADOS_BASE[0]].get_height()], #altura de refernecia fixa
                             [Database.ESTADOS_BASE[0], Database.ESTADOS_GUARDA[0]])
        
        
        #tempo
        self.clock = pygame.time.Clock()
        self.t = 0
        self.intervalo_turno = 20
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
        #teste
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
        self.draw_hud()
        pygame.display.flip()

    def draw_hud(self):
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

        # Display timeline.estados_guarda
        guarda_text = self.font.render(f"Timeline_guarda: {self.timeline.estados_guarda}", True, (255, 255, 255))
        screen.blit(guarda_text, (5, 70))

        # Display timeline.movimentos_a_fazer
        movimentos_a_fazer_text = self.font.render(f"Movimentos a fazer: {self.timeline.movimentos_a_fazer}", True, (255, 255, 255))
        screen.blit(movimentos_a_fazer_text, (5, 100))

        # Display player.base_atual
        base_text = self.font.render(f"Estado atual: {self.player.estado}", True, (255, 255, 255))
        screen.blit(base_text, (5, 150))

if __name__ == "__main__":
    game = Game()
    game.run()

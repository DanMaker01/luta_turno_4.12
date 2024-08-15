import pygame
import database
from input import KeySequenceDetector
from timeline import Timeline
from resources import ResourceLoader

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
            ['a','up'],
            ['a','down'],

            ['z','z'],
            ['z','left'],
            ['z','right'],
            ['z','up'],
            ['z','down'],

            ['left', 'left'],
            ['right','right'],
            ['left', 'right'],
            ['right','left'],
            
            # 1 tecla
            ['left'],
            ['right'],
            ['up'],
            ['down'],
            # Adicione mais sequências conforme necessário
        ]
        self.detector = KeySequenceDetector(self.predefined_sequences)
        self.running = True
        self.timeline = Timeline()
        self.clock = pygame.time.Clock()
        self.database = database.Database()
        self.t = 0
        self.recursos = ResourceLoader()
        
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.detector.handle_keydown(event.key)

    
    def update(self):
        self.timeline.update()
        self.t+=1
        if self.t % 100 == 0: #tempo de um turno in_game
            self.timeline.addTimeline()
        
        
    def desenhar_base(self,nome_base,x,y):
        imagem = self.recursos.get_base(nome_base)
        self.screen.blit(imagem, (x, y+imagem.get_height()))
    def desenhar_guarda(self,nome_guarda,x,y):
        base_atual = self.timeline.get_ultima_base()
        
        
        # if base_atual == "base_chute":
        #     y = y+
        
        imagem = self.recursos.get_guarda(nome_guarda)
        
        self.screen.blit(imagem, (x-1, y))

    def draw(self):
        self.screen.fill((127, 127, 127))  # Preenche a tela com a cor preta
        margem_x = 10
        margem_y = 10
        espacamento_linha = 20
        # Texto estático
        texto_estatico = "A: Guarda, Z: Base, Setas: Movimento"
        label_estatico = self.font.render(texto_estatico, True, (255, 255, 255))
        self.screen.blit(label_estatico, (margem_x, margem_y))  # Posição no topo da tela

        # Render self.linha_guarda[-1]
        guarda_atual_text = self.timeline.linha_guarda[-1]
        label_linha_guarda = self.font.render(f"Guarda Atual: {guarda_atual_text,self.database.ESTADOS_GUARDA.index(guarda_atual_text)}", True, (255, 255, 255))
        self.screen.blit(label_linha_guarda, (margem_x, margem_y+espacamento_linha))  # Posicione conforme necessário

        # Render self.linha_base[-1]
        base_atual_text = self.timeline.linha_base[-1]
        label_linha_base = self.font.render(f"Base Atual: {base_atual_text,self.database.ESTADOS_BASE.index(base_atual_text)}", True, (255, 255, 255))
        self.screen.blit(label_linha_base, (margem_x, margem_y+2*espacamento_linha))  # Posicione conforme necessário
        
        # Render sequencia_guarda em coluna
        movimentos_guarda = self.timeline.sequencia_guarda
        for i, movimento in enumerate(movimentos_guarda):
            label_movimento = self.font.render(f"Guarda seq {i+1}: {movimento}", True, (255, 255, 255))
            self.screen.blit(label_movimento, (margem_x, margem_y+100 + i * espacamento_linha))  # Desenha a 200 pixels à direita da coluna de base

        # Render sequencia_base em coluna
        movimentos_base = self.timeline.sequencia_base
        for i, movimento in enumerate(movimentos_base):
            label_movimento = self.font.render(f"Base seq {i+1}: {movimento}", True, (255, 255, 255))
            self.screen.blit(label_movimento, (margem_x+200, margem_y+100 + i * espacamento_linha))  # 40 é o espaçamento vertical após o texto estático


        guarda_atual = self.timeline.get_ultima_guarda()
        base_atual = self.timeline.get_ultima_base()

        #render base e guarda
        pos_x = 0
        pos_y = 0
        self.desenhar_guarda(guarda_atual, pos_x, pos_y)
        self.desenhar_base(base_atual, pos_x,pos_y)


        pygame.display.flip()



    def run(self):
        while self.running:
            self.handle_events() 
            comando, b = self.detector.check_sequences()
            if comando: # se a sequência for detectada
                self.timeline.pilha_add(comando)
            self.update()
            self.draw()
            self.clock.tick(60)  # Verifica a cada frame (60 vezes por segundo)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

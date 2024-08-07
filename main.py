import pygame

from input import KeySequenceDetector
from timeline import Timeline

class Game:
    def __init__(self, width=640, height=480):
        pygame.init()
        pygame.display.set_caption("Jogo luta em turno")
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
        self.timeline = Timeline()
        self.running = True
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.detector.handle_keydown(event.key)

    def update(self):
        self.timeline.update()
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))  # Preenche a tela com a cor preta
        movimentos_text = ', '.join(self.timeline.pilha_movimentos_a_fazer)
        label = self.font.render(f"Movimentos: {movimentos_text}", True, (255, 255, 255))
        self.screen.blit(label, (20, 20))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            comando, b = self.detector.check_sequences()
            if comando:
                self.timeline.pilha_add(comando)
            self.update()
            self.draw()
            self.clock.tick(60)  # Verifica a cada frame (60 vezes por segundo)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

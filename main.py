import pygame
import time
import input

pygame.init()

# Defina a tela
screen = pygame.display.set_mode((640, 480))


def main():
    # Defina as sequências predefinidas
    predefined_sequences = [
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

    detector = input.KeySequenceDetector(predefined_sequences)
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                detector.handle_keydown(event.key)

        detector.check_sequences()
        clock.tick(60)  # Verifica a cada frame (60 vezes por segundo)

    pygame.quit()

if __name__ == "__main__":
    main()

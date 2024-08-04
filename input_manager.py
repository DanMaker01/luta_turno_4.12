import pygame
from database import Database

class InputManager:
    def __init__(self):
        self.buffer = []
        self.buffer_timeout = 0
        self.buffer_timeout_max = 30

        self.predefined_sequences = [
            ["Base", "baixo"],
            ["Base", "cima"],
            ["Base", "direita"],
            ["Base", "esquerda"],
            ["Guarda", "baixo"],
            ["Guarda", "cima"],
            ["Guarda", "esquerda"],
            ["Guarda", "direita"],
            ["baixo"],
            ["cima"],
            ["esquerda"],
            ["direita"],
        ]

    def handle_keydown(self, key):
        key_map = {
            pygame.K_a: "Guarda",
            pygame.K_z: "Base",
            pygame.K_UP: "cima",
            pygame.K_DOWN: "baixo",
            pygame.K_LEFT: "esquerda",
            pygame.K_RIGHT: "direita"
        }
        if key in key_map:
            self.buffer.append(key_map[key])
            self.buffer_timeout = self.buffer_timeout_max

    def limpar_buffer(self):
        self.buffer = []

    def sequence_to_move(self, sequence):
        mapping = {
            "Base": {
                "cima": "base_chute",
                "baixo": "base_cavaleiro",
                "esquerda": "base_kokutsu",
                "direita": "base_zenkutsu",
            },
            "Guarda": {
                "cima": "defesa_alta",
                "baixo": "defesa_baixo",
                "direita": "ataque_leve",
                "esquerda": "ataque_forte"
            },
            "cima": "strafe_cima",
            "baixo": "strafe_baixo",
            "direita": "mover_avancar",
            "esquerda": "mover_recuar"
        }

        if sequence[0] in mapping and isinstance(mapping[sequence[0]], dict):
            return mapping[sequence[0]].get(sequence[1])
        return mapping.get(sequence[0])

    # Check if the buffer contains a predefined sequence
    def check_sequences(self, timeline):
        """
        Check if the buffer contains any predefined sequences.
        """
        buffer_length = len(self.buffer)
        for sequence in self.predefined_sequences:
            sequence_length = len(sequence)  # Get the length of the sequence
            for i in range(buffer_length - sequence_length + 1):  # Check every possible sequence in the buffer
                if self.buffer[i:i + sequence_length] == sequence:
                    # If a sequence is found, add the corresponding movement to the timeline
                    timeline.add_movimento_to_timeline(self.sequence_to_move(sequence))
                    self.limpar_buffer()
                    return

    def buffer_update(self):
        if self.buffer:
            self.buffer_timeout -= 1
        if self.buffer_timeout <= 0:
            self.limpar_buffer()

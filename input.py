import time
import pygame

class KeySequenceDetector:
    def __init__(self, predefined_sequences, key_interval_max=0.250):
        self.predefined_sequences = predefined_sequences
        self.keys_pressed = []
        self.key_times = []
        self.key_interval_max = key_interval_max  # intervalo máximo de tempo em segundos
        self.last_key_time = None
        self.move_buffer = []  # Buffer de movimentos detectados

    def get_keys_pressed(self):
        return self.keys_pressed

    def get_move_buffer(self):
        return self.move_buffer

    def handle_keydown(self, key):
        current_time = time.time()
        key_name = pygame.key.name(key)
        
        self.keys_pressed.append(key_name)
        self.key_times.append(current_time)
        self.last_key_time = current_time

    def check_sequences(self):
        if not self.last_key_time:
            return None, None  # Retorna None se nenhuma sequência for detectada
        
        current_time = time.time()
        if (current_time - self.last_key_time) >= self.key_interval_max:
            buffer_length = len(self.keys_pressed)
            for sequence in self.predefined_sequences:
                sequence_index = self.find_sequence_in_buffer(sequence, buffer_length)
                if sequence_index is not None:
                    sequencia, intervalos = self.handle_sequence_detected(sequence, sequence_index)
                    return sequencia, intervalos

            # Remove a tecla mais antiga se não encontrar uma sequência e o tempo exceder o limite
            self.keys_pressed.pop(0)
            self.key_times.pop(0)
            return None, None

        return None, None

    def find_sequence_in_buffer(self, sequence, buffer_length):
        sequence_length = len(sequence)
        if buffer_length >= sequence_length:
            for i in range(buffer_length - sequence_length + 1):
                key_intervals = [
                    self.key_times[i + j] - self.key_times[i + j - 1]
                    for j in range(1, sequence_length)
                ]
                if all(interval <= self.key_interval_max for interval in key_intervals):
                    if self.keys_pressed[i:i + sequence_length] == sequence:
                        return i
        return None

    def handle_sequence_detected(self, sequence, start_index):
        self.move_buffer.append(sequence)  # Adiciona a sequência detectada no buffer de movimentos

        # Remove as teclas correspondentes à sequência detectada
        for _ in range(len(sequence)):
            self.keys_pressed.pop(start_index)
            self.key_times.pop(start_index)

        # Recalcula o tempo da última tecla se ainda houver teclas no buffer
        if self.keys_pressed:
            self.last_key_time = self.key_times[-1]
        else:
            self.last_key_time = None

        # Calcula os intervalos de tempo para feedback
        key_intervals = [
            self.key_times[i] - self.key_times[i - 1]
            for i in range(1, len(self.key_times))
        ]
        intervalos = [round(interval, 3) for interval in key_intervals]

        return sequence, intervalos

    def reset(self):
        self.keys_pressed = []
        self.key_times = []
        self.last_key_time = None
        self.move_buffer = []

import time
import pygame

class KeySequenceDetector:
    def __init__(self, predefined_sequences, key_interval_max=0.150):
        self.predefined_sequences = predefined_sequences
        self.keys_pressed = []
        self.key_times = []
        self.key_interval_max = key_interval_max  # intervalo máximo de tempo em segundos
        self.last_key_time = None

    def handle_keydown(self, key):
        current_time = time.time()
        key_name = pygame.key.name(key)
        
        self.keys_pressed.append(key_name)
        self.key_times.append(current_time)
        self.last_key_time = current_time

    def check_sequences(self):
        if not self.last_key_time:
            return None, None
        
        current_time = time.time()
        if (current_time - self.last_key_time) >= self.key_interval_max:
            # Verifique as sequências antes de resetar
            buffer_length = len(self.keys_pressed)
            for sequence in self.predefined_sequences:
                if self.is_sequence(sequence, buffer_length):
                    sequencia, intervalos = self.handle_sequence_detected(sequence)
                    return sequencia, intervalos
            # Reset se nenhuma sequência for detectada
            self.reset()
            return None, None
        return None, None
        

    def is_sequence(self, sequence, buffer_length):
        sequence_length = len(sequence)
        if buffer_length >= sequence_length:
            # Verifica sequência regular
            key_intervals = [self.key_times[i] - self.key_times[i-1] for i in range(1, sequence_length)]
            if all(interval <= self.key_interval_max for interval in key_intervals):
                if self.keys_pressed[-sequence_length:] == sequence:
                    return True
        return False

    def handle_sequence_detected(self, sequence):
        # print(f"Sequência detectada: {sequence}")
        key_intervals = [self.key_times[i] - self.key_times[i-1] for i in range(1, len(self.key_times))]
        intervalos = [round(interval, 3) for interval in key_intervals]
        # print(f"Intervalos de tempo: {intervalos} segundos")
        self.reset()
        return sequence, intervalos

    def reset(self):
        self.keys_pressed = []
        self.key_times = []
        self.last_key_time = None

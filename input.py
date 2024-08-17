import time
import pygame


# IMPLEMENTAR: 
# sistema de detectar sequencias melhor.
# como está atualmente: a cada frame o buffer de input é lido, se houver itens, verifica se há alguma sequencia, se houver, add ela na pilha de comandos. 
# como deve ser: ao apertar uma tecla inicia-se uma contagem, adiciona-se a tecla no buffer e verifica se há uma sequencia válida. após o contador o buffer zera.

class KeySequenceDetector:
    def __init__(self, predefined_sequences, key_interval_max=0.175):
        self.predefined_sequences = predefined_sequences
        self.keys_pressed = []
        self.key_times = []
        self.key_interval_max = key_interval_max  # intervalo máximo de tempo em segundos
        self.last_key_time = None

    def get_keys_pressed(self):
        return self.keys_pressed

    def handle_keydown(self, key):
        current_time = time.time()
        key_name = pygame.key.name(key)
        
        self.keys_pressed.append(key_name)
        self.key_times.append(current_time)
        self.last_key_time = current_time

    def check_sequences(self):
        if not self.last_key_time: # Verifique se a lista de teclas pressionadas ainda é vazia
            return None, None # Retorna None se nenhuma sequência for detectada
        
        current_time = time.time() # Obtenha o tempo atual
        if (current_time - self.last_key_time) >= self.key_interval_max: # Verifique se o intervalo de tempo ultrapassou o limite
            # Verifique as sequências antes de resetar 
            buffer_length = len(self.keys_pressed) # Tamanho da lista de teclas pressionadas
            for sequence in self.predefined_sequences: # Percorra as sequências predefinidas
                if self.is_sequence(sequence, buffer_length): # Verifique se a sequência atual corresponde a uma sequência predefinida
                    sequencia, intervalos = self.handle_sequence_detected(sequence) # Sequência detectada
                    return sequencia, intervalos# Retorna a sequência e os intervalos de tempo
            # Reset se nenhuma sequência for detectada
            self.reset()# Reseta a lista de teclas pressionadas
            # print("resetou após tempo sem apertar nada...")
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

    def handle_sequence_detected(self, sequence): #
        # print(f"Sequência detectada: {sequence}")
        key_intervals = [self.key_times[i] - self.key_times[i-1] for i in range(1, len(self.key_times))] # Calcula os intervalos de tempo
        intervalos = [round(interval, 3) for interval in key_intervals] # Arredonda os intervalos de tempo
        # print(f"Intervalos de tempo: {intervalos} segundos")
        self.reset()
        print("reset pelo handle_sequence_detected")
        return sequence, intervalos

    def reset(self):
        self.keys_pressed = []
        self.key_times = []
        self.last_key_time = None

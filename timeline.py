from movements import Movement

class Timeline:
    def __init__(self):
        self.movimentos = []
        

    def add_movimento_to_timeline(self, nome_movimento):
        tempo_in = Movement.MOVEMENTS[nome_movimento][0]
        tempo_out = Movement.MOVEMENTS[nome_movimento][2]

        for _ in range(tempo_in):
            self.movimentos.append("pre")
        
        self.movimentos.append(nome_movimento)

        for _ in range(tempo_out):
            self.movimentos.append("pós")

    def executar_movimentos(self):
        if self.movimentos:
            movimento_executado = self.movimentos.pop(0)
            print(movimento_executado)
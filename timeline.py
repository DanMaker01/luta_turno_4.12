import database
import input
import dijkstra

class Timeline:

    def __init__(self):
        self.database = database.Database()
        self.linha_tempo = [0]
        self.linha_posicao = [10]
        self.linha_guarda = ["guarda_parada"]
        self.linha_base = ["base_parada"]

        self.sequencia_guarda = []
        self.sequencia_base = []
        self.sequencia_movimento = []

        self.pilha_movimentos_a_fazer = []

    def pilha_add(self, movimento):
        self.pilha_movimentos_a_fazer.append(movimento)
    def pilha_pop(self):
        if len(self.pilha_movimentos_a_fazer) > 0:
            return self.pilha_movimentos_a_fazer.pop()
        else:
            return None

    def criar_proxima_cena(self):
        cena = []
        #na verdade tem que add o primeiro item de cada sequencia
        # cena.append(self.linha_tempo[-1])
        # cena.append(self.linha_posicao[-1])
        # cena.append(self.linha_guarda[-1])
        # cena.append(self.linha_base[-1])
        return cena

    def gerar_sequencia_base(self, base_final):
        indice_base_inicial = self.database.ESTADOS_BASE.index(self.linha_base[-1])
        indice_base_final = self.database.ESTADOS_BASE.index(base_final)
        menor_sequencia = dijkstra.dijkstra_path(self.database.ESTADOS_BASE,indice_base_inicial,indice_base_final )
        return menor_sequencia
    
    def gerar_sequencia_guarda(self,base_final):
        indice_base_inicial = self.database.ESTADOS_GUARDA.index(self.linha_guarda[-1])
        indice_base_final = self.database.ESTADOS_GUARDA.index(base_final)
        menor_sequencia = dijkstra.dijkstra_path(self.database.ESTADOS_GUARDA,indice_base_inicial,indice_base_final )
        return menor_sequencia

    def executar_movimento(self):
        movimento_a_executar = self.pilha_pop()
        if movimento_a_executar:
            string_movimento = self.database.check_movements(movimento_a_executar)
            print("string_movimento:",string_movimento)
            tipo = self.selecionar_tipo_movimento(string_movimento)
            if(tipo == "base"):
                print("é base!")
                menor_sequencia = self.gerar_sequencia_base(string_movimento)
                pass
            elif (tipo == "guarda"):
                print("é guarda")
                menor_sequencia = self.gerar_sequencia_guarda(string_movimento)
                pass
            elif tipo == "ataque":
                #verifica se está na base de chute, se tiver sai chute.
                pass
            elif tipo == "mover":
                print("é movimento")
        else:
            pass

    def selecionar_tipo_movimento(self,string_movimento):
        
        if string_movimento.startswith("base"):
            return "base"
        if string_movimento.startswith("guarda"):
            return "guarda"
        if string_movimento.startswith("ataque"):
            return "ataque"
        if string_movimento.startswith("mover"):
            return "mover"



    def update(self):
        self.executar_movimento()

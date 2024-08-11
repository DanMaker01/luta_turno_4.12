import database
import input
import dijkstra

class Timeline:
    def __init__(self):
        self.database = database.Database()
        self.linha_tempo = [0]
        self.linha_posicao = [10] # por que 10?
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

    # def criar_proxima_cena(self):
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
        menor_sequencia = dijkstra.dijkstra_path(self.database.MATRIZ_TRANSICAO_BASE,indice_base_inicial,indice_base_final )
        return menor_sequencia
    def gerar_sequencia_guarda(self,base_final):
        indice_base_inicial = self.database.ESTADOS_GUARDA.index(self.linha_guarda[-1])
        indice_base_final = self.database.ESTADOS_GUARDA.index(base_final)
        menor_sequencia = dijkstra.dijkstra_path(self.database.MATRIZ_TRANSICAO_GUARDA,indice_base_inicial,indice_base_final )
        return menor_sequencia

    def definir_sequencia_base(self, string_movimento):
        menor_sequencia = self.gerar_sequencia_base(string_movimento) #gera a menor sequencia
        self.sequencia_base =  menor_sequencia[1] # aloca a sequencia gerada no self.sequencia_base 
    def definir_sequencia_guarda(self, string_movimento):
        menor_sequencia = self.gerar_sequencia_guarda(string_movimento) #gera a menor sequencia
        self.sequencia_guarda = menor_sequencia[1] # aloca a sequencia gerada no self.sequencia_guarda
    
    def definir_sequencia_ataque(self, string_movimento):
        base_atual = self.linha_base[-1]
        # print("base:", base_atual)

        if(base_atual == "base_chute"): # se estiver na base de chute, sai chute.
            if string_movimento == "ataque_leve":
                string_movimento = "chute_frente"
            else:           #então é ataque_forte
                string_movimento = "chute_lateral"
            
            self.definir_sequencia_base(string_movimento) #base
        else: #então é soco
            if string_movimento == "ataque_leve":
                string_movimento = "soco_frente"
            else:           #então é ataque forte
                string_movimento = "soco_tras"
           
            self.definir_sequencia_guarda(string_movimento) #guarda
        pass

    # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = 
    # FUNÇÔES RELEVANTES    
    # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = 
    def gerar_sequencia_de_movimento(self):
        movimento_a_executar = self.pilha_pop()
        if movimento_a_executar:
            string_movimento = self.database.check_movements(movimento_a_executar)
            print("string_movimento:",string_movimento)
            tipo = self.selecionar_tipo_movimento(string_movimento)
            if tipo == "ataque": #chute ou soco
                self.definir_sequencia_ataque(string_movimento)
                pass
            elif(tipo == "base"):
                self.definir_sequencia_base(string_movimento)
                pass
            elif (tipo == "guarda"): #defesa
                self.definir_sequencia_guarda(string_movimento)
                pass
            elif tipo == "mover":
                print("é movimento")
        else:
            pass # não ha movimentos no buffer

    def selecionar_tipo_movimento(self,string_movimento):
        
        if string_movimento.startswith("base"):
            return "base"
        if string_movimento.startswith("guarda"):
            return "guarda"
        if string_movimento.startswith("ataque"):
            return "ataque"
        if string_movimento.startswith("mover"):
            return "mover"

    def aplicar_base(self):
        self.linha_base.append(self.sequencia_base.pop(0))
    def aplicar_guarda(self):
        self.linha_guarda.append(self.sequencia_guarda.pop(0))

    def executar_movimentos(self):
        if len(self.sequencia_base) > 0:
            print("aplicar base")
            # self.aplicar_base()
            a = self.sequencia_base.pop(0)
            self.linha_base.append(self.database.ESTADOS_BASE[a])
            print(self.database.ESTADOS_GUARDA[a])
        if len(self.sequencia_guarda) > 0:
            print("aplicar guarda", self.sequencia_guarda)
            a = self.sequencia_guarda.pop(0)
            self.linha_guarda.append(self.database.ESTADOS_GUARDA[a])
            print(self.database.ESTADOS_GUARDA[a])
            # self.aplicar_guarda()


    def update(self):
        self.gerar_sequencia_de_movimento()
        self.executar_movimentos()




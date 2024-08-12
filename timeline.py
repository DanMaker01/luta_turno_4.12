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

        self.sequencia_posicao = []

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
        cena.append(self.linha_tempo[-1] + 1)
        cena.append(self.sequencia_posicao.pop(0)) # CORRGIR @@@@@@@@@@@@@
        cena.append(self.sequencia_guarda.pop(0))
        cena.append(self.sequencia_base.pop(0))

        return cena
    
    def addTimeline(self):
        cena = self.criar_proxima_cena()
        print("cena",cena)
        self.linha_tempo.append(cena[0])
        self.linha_posicao.append(cena[1])
        self.linha_guarda.append(cena[2])
        self.linha_base.append(cena[3])

        #printar cena


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
        # print("menor_sequencia:",menor_sequencia)
        self.sequencia_base =  menor_sequencia[1] # aloca a sequencia gerada no self.sequencia_base 
    def definir_sequencia_guarda(self, string_movimento):
        menor_sequencia = self.gerar_sequencia_guarda(string_movimento) #gera a menor sequencia
        self.sequencia_guarda = menor_sequencia[1] # aloca a sequencia gerada no self.sequencia_guarda
    
    #vai ser editada, pois dependendo da base, o movimento vai ser diferente, etc, tem movimento que tem recoil
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
            else:           #então é ataque_forte
                string_movimento = "soco_tras"
           
            self.definir_sequencia_guarda(string_movimento) #guarda
        pass

    # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = 
    # FUNÇÔES RELEVANTES    
    # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = 
    def selecionar_tipo_do_movimento_e_alocar_sequencia(self):
        movimento_a_executar = self.pilha_pop()
        if movimento_a_executar:
            string_movimento = self.database.check_movements(movimento_a_executar)
            print("string_movimento:",string_movimento)
            tipo = self.selecionar_tipo_movimento(string_movimento)
            # print("tipo",tipo)
            if tipo == "ataque": #chute ou soco
                self.definir_sequencia_ataque(string_movimento)
                print("sequencia_guarda:",self.sequencia_guarda)
                print("sequencia_base:",self.sequencia_base)
                pass
            elif (tipo == "guarda"): #defesa
                self.definir_sequencia_guarda(string_movimento)
                print("sequencia_guarda:",self.sequencia_guarda)
                
                pass
            elif (tipo == "base"):
                self.definir_sequencia_base(string_movimento)
                print("sequencia_base:",self.sequencia_base)
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
            a = self.sequencia_base.pop(0)
            self.linha_base.append(self.database.ESTADOS_BASE[a])
            print(self.database.ESTADOS_BASE[a])
        if len(self.sequencia_guarda) > 0:
            a = self.sequencia_guarda.pop(0)
            self.linha_guarda.append(self.database.ESTADOS_GUARDA[a])
            print(self.database.ESTADOS_GUARDA[a])
            

    def update(self):
        self.selecionar_tipo_do_movimento_e_alocar_sequencia()
        # self.executar_movimentos()
        pass




import database
# import input
import dijkstra

class Timeline:
    def __init__(self):
        self.database = database.Database()
        self.linha_tempo = [0] 
        self.linha_posicao = [1] #posicao inicial
        self.linha_guarda = ["guarda_parado"]
        self.linha_base = ["base_parado"]

        self.contagem_cena = 1

        self.sequencia_guarda = []
        self.sequencia_base = []
        self.sequencia_movimento = []

        self.sequencia_posicao = []

        self.pilha_movimentos_a_fazer = []

    def get_ultima_base(self):
        return self.linha_base[-1]
    def get_ultima_guarda(self):
        return self.linha_guarda[-1]
    def get_ultima_posicao(self):
        return self.linha_posicao[-1]

    def pilha_add(self, movimento):
        self.pilha_movimentos_a_fazer.append(movimento)
    def pilha_pop(self):
        if len(self.pilha_movimentos_a_fazer) > 0:
            return self.pilha_movimentos_a_fazer.pop()
        else:
            return None

    def criar_proxima_cena(self):
        cena = []

        #tempo
        cena.append(self.contagem_cena)
        self.contagem_cena+=1
        
        #posicao
        if len(self.sequencia_posicao) > 0:
            novo_movimento = self.sequencia_posicao.pop(0)
            cena.append(novo_movimento) # CORRGIR @@@@@@@@@@@@@
        else:
            cena.append(self.linha_posicao[-1])
        
        #guarda
        if len(self.sequencia_guarda) > 0:
            # nova_guarda = 
            cena.append(self.sequencia_guarda.pop(0))
        else:
            cena.append(self.linha_guarda[-1])
        
        #base
        if len(self.sequencia_base) > 0:
            cena.append(self.sequencia_base.pop(0))
        else:
            cena.append(self.linha_base[-1])
            
        return cena
    def get_cena(self, indice):
        tamanho_timeline = len(self.linha_tempo)
        if(indice > tamanho_timeline):
            return None
        else:
            cena = []
            cena.append(self.linha_tempo[indice])
            cena.append(self.linha_posicao[indice])
            cena.append(self.linha_guarda[indice])
            cena.append(self.linha_base[indice])
            return cena
    def aplicar_cena_na_timeline(self, cena):
        self.linha_tempo.append(cena[0])
        self.linha_posicao.append(cena[1])
        self.linha_guarda.append(cena[2])
        self.linha_base.append(cena[3])
    def verificar_efeitos_da_acao(self):
        ultima_cena = self.get_cena(-1)
        ultima_postura = [ultima_cena[2],ultima_cena[3]]

        penultima_cena = self.get_cena(-2)
        penultima_postura = [penultima_cena[2],penultima_cena[3]]

        if ultima_postura != penultima_postura:
            # print("se moveu!!")
            pass

    
    def addTimeline(self):
        cena = self.criar_proxima_cena()
        
        self.aplicar_cena_na_timeline(cena)
        self.verificar_efeitos_da_acao()

    def gerar_sequencia_base(self, base_final):
        indice_base_inicial = self.database.ESTADOS_BASE.index(self.linha_base[-1])
        indice_base_final = self.database.ESTADOS_BASE.index(base_final)
        menor_sequencia = dijkstra.dijkstra_path(self.database.MATRIZ_TRANSICAO_BASE,indice_base_inicial,indice_base_final )
        return menor_sequencia
    def gerar_sequencia_guarda(self,base_final):
        indice_guarda_inicial = self.database.ESTADOS_GUARDA.index(self.linha_guarda[-1])
        indice_guarda_final = self.database.ESTADOS_GUARDA.index(base_final)
        menor_sequencia = dijkstra.dijkstra_path(self.database.MATRIZ_TRANSICAO_GUARDA,indice_guarda_inicial,indice_guarda_final )
        return menor_sequencia

    def adicionar_pausas_na_sequencia(self, matriz_transicao, sequencia):
        sequencia_com_pausas = []
        for i in range(len(sequencia)-1):
            if matriz_transicao == self.database.MATRIZ_TRANSICAO_BASE:

                indice_estado_inicial = self.database.ESTADOS_BASE.index(sequencia[i])
                indice_estado_final = self.database.ESTADOS_BASE.index(sequencia[i+1])
                distancia = matriz_transicao[indice_estado_inicial][indice_estado_final]
                for n in range(distancia):
                    sequencia_com_pausas.append(sequencia[i])
            else:
                indice_lei_inicial = self.database.ESTADOS_GUARDA.index(sequencia[i])
                indice_lei_final = self.database.ESTADOS_GUARDA.index(sequencia[i+1])
                distancia = matriz_transicao[indice_lei_inicial][indice_lei_final]
                for n in range(distancia):
                    sequencia_com_pausas.append(sequencia[i])

        sequencia_com_pausas.append(sequencia[-1])
            
        return sequencia_com_pausas

    def definir_sequencia_completa_base(self, string_movimento):
        indices_menor_sequencia = self.gerar_sequencia_base(string_movimento)[1] #gera a menor sequencia
        menor_sequencia = [(self.database.ESTADOS_BASE[indice]) for indice in indices_menor_sequencia]
        menor_sequencia_com_pausas = self.adicionar_pausas_na_sequencia(self.database.MATRIZ_TRANSICAO_BASE,menor_sequencia)
        # menor_sequencia_com_pausas_e_rikite = self.adicionar_rikite_na_sequencia(menor_sequencia_com_pausas) # implementar@@@@
        self.aplicar_sequencia_base(menor_sequencia_com_pausas) # aloca a sequencia gerada no self.sequencia_base 
    def definir_sequencia_completa_guarda(self, string_movimento):
        indices_menor_sequencia = (self.gerar_sequencia_guarda(string_movimento))[1] #gera a menor sequencia
        menor_sequencia = [(self.database.ESTADOS_GUARDA[indice]) for indice in indices_menor_sequencia]
        menor_sequencia_com_pausas = self.adicionar_pausas_na_sequencia(self.database.MATRIZ_TRANSICAO_GUARDA,menor_sequencia)
        self.aplicar_sequencia_guarda(menor_sequencia_com_pausas)
        
    def aplicar_sequencia_guarda(self,menor_sequencia):
        self.sequencia_guarda = menor_sequencia # aloca a sequencia gerada no self.sequencia_guarda
    def aplicar_sequencia_base(self,menor_sequencia):
        self.sequencia_base = menor_sequencia # aloca a sequencia gerada no self.sequencia_base

    #vai ser editada, pois dependendo da base, o movimento vai ser diferente, etc, tem movimento que tem recoil
    def definir_sequencia_ataque(self, string_movimento):
        base_atual = self.linha_base[-1]
        # print("base:", base_atual)
        
        if(base_atual == "base_chute"): # se estiver na base de chute, sai chute.
            if string_movimento == "ataque_leve":
                string_movimento = "chute_frente"
            else:           #então é ataque_forte
                string_movimento = "chute_lateral"
            
            self.definir_sequencia_completa_base(string_movimento) #base
        else: #então é soco
            if string_movimento == "ataque_leve":
                string_movimento = "soco_frente"
            else:           #então é ataque_forte
                string_movimento = "soco_tras"
           
            self.definir_sequencia_completa_guarda(string_movimento) #guarda
        pass

    # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = 
    # FUNÇÔES RELEVANTES    
    # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = 
    def selecionar_tipo_do_movimento_e_alocar_sequencia(self): #implementar, pra ter CANCEL, a cada comando deve-se criar uma sequencia baseado no ultimo estado que você está
        movimento_a_executar = self.pilha_pop()
        if movimento_a_executar:
            string_movimento = self.database.check_movements(movimento_a_executar)
            print("string_movimento:",string_movimento)
            tipo = self.selecionar_tipo_movimento(string_movimento)
            # print("tipo",tipo)
            if tipo == "ataque": #chute ou soco
                self.definir_sequencia_ataque(string_movimento)
                # print("sequencia_guarda:",self.sequencia_guarda)
                # print("sequencia_base:",self.sequencia_base)
                pass
            elif (tipo == "guarda"): #defesa
                self.definir_sequencia_completa_guarda(string_movimento)
                # print("sequencia_guarda:",self.sequencia_guarda)
                
                pass
            elif (tipo == "base"):
                self.definir_sequencia_completa_base(string_movimento)
                # print("sequencia_base:",self.sequencia_base)
                pass
            elif tipo == "mover":
                print("apertou \"movimento\", falta implementar @@@@@@@@")
        else:
            pass # não ha movimentos no buffer

    def selecionar_tipo_movimento(self,string_movimento):
        if string_movimento:

            if string_movimento.startswith("base"):
                return "base"
            if string_movimento.startswith("guarda"):
                return "guarda"
            if string_movimento.startswith("ataque"):
                return "ataque"
            if string_movimento.startswith("mover"):
                return "mover" 
        else:
            pass # 
    def update(self):
        self.selecionar_tipo_do_movimento_e_alocar_sequencia()
        # self.executar_movimentos()
        pass




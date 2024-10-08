import database
# import input
import dijkstra
import numpy as np

class Timeline:
    def __init__(self):
        self.database = database.Database()
        self.linha_tempo = [0] 
        self.linha_posicao = [1] #posicao inicial
        self.linha_guarda = ["guarda_parado"]
        self.linha_base = ["base_parado"]

        self.contagem_cenas = 0

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
        self.contagem_cenas+=1
        cena.append(self.contagem_cenas)
        
        #se há algo na sequencia de posicao
        if len(self.sequencia_posicao) > 0:
            mudanca_posicao = self.sequencia_posicao.pop(0) #retira a proxima acao da sequencia e 
            posicao_final = mudanca_posicao + self.linha_posicao[-1] #aplica a mudança na posicao atual 
            cena.append(self.limitar_a_posicao(posicao_final)) #limita para o personagem não sair da tela
        else:
            cena.append(self.linha_posicao[-1])
        
        #se há algo na sequencia de guarda
        if len(self.sequencia_guarda) > 0:
            # nova_guarda = 
            cena.append(self.sequencia_guarda.pop(0))
        else:
            cena.append(self.linha_guarda[-1])
        
        #se existe algo na sequencia de base
        if len(self.sequencia_base) > 0:
            cena.append(self.sequencia_base.pop(0))
        else:
            cena.append(self.linha_base[-1])
            
        return cena
    def get_cena(self, indice): #implementar
        tamanho_timeline = len(self.linha_tempo)
        if(indice > tamanho_timeline):
            return None #está tentando pegar um tempo que nao existe ainda
        else:
            cena = []
            cena.append(self.linha_tempo[indice])
            cena.append(np.around(self.linha_posicao[indice],8)) #está arredondado em 4 digitos apos virgula, espero que dê bom
            cena.append(self.linha_guarda[indice])
            cena.append(self.linha_base[indice])
            return cena
    def aplicar_cena_na_timeline(self, cena):
        self.linha_tempo.append(cena[0])
        self.linha_posicao.append(cena[1])
        self.linha_guarda.append(cena[2])
        self.linha_base.append(cena[3])
   
    def limitar_a_posicao(self, posicao):
        max = 4
        min = 0
        if posicao <= min:
            posicao = min
        if posicao >= max:
            posicao = max
        return posicao
    def verificar_efeitos_da_acao(self): #implementar
        #pegar ultima e penultima cenas
        ultima_cena = self.get_cena(-1)
        ultimo_estado_player = [ultima_cena[1],ultima_cena[2],ultima_cena[3]]
        penultima_cena = self.get_cena(-2)
        penultimo_estado_player = [penultima_cena[1], penultima_cena[2],penultima_cena[3]]

        if ultimo_estado_player != penultimo_estado_player:# moveu!!
            # print(penultima_cena)
            print(penultima_cena)
            # mini_linha_base = 
            #calcular dano tbm, dano = fator_dano*delta_posicao
            #bonus no dano se for em uma base
            pass

        #
    
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

    def gerar_sequencia_completa_base(self, string_movimento): #modularizar mais, implementar
        indices_menor_sequencia = self.gerar_sequencia_base(string_movimento)[1] #gera a menor sequencia
        menor_sequencia = [(self.database.ESTADOS_BASE[indice]) for indice in indices_menor_sequencia]
        menor_sequencia_com_pausas = self.adicionar_pausas_na_sequencia(self.database.MATRIZ_TRANSICAO_BASE,menor_sequencia)
        # menor_sequencia_com_pausas_e_rikite = self.adicionar_rikite_na_sequencia(menor_sequencia_com_pausas) # implementar@@@@
        return menor_sequencia_com_pausas # aloca a sequencia gerada no self.sequencia_base 
    def gerar_sequencia_completa_guarda(self, string_movimento): #modulzarizar mais, implementar
        indices_menor_sequencia = (self.gerar_sequencia_guarda(string_movimento))[1] #gera a menor sequencia
        menor_sequencia = [(self.database.ESTADOS_GUARDA[indice]) for indice in indices_menor_sequencia]
        menor_sequencia_com_pausas = self.adicionar_pausas_na_sequencia(self.database.MATRIZ_TRANSICAO_GUARDA,menor_sequencia)
        return menor_sequencia_com_pausas
    
    #vai ser editada, pois dependendo da base, o movimento vai ser diferente, etc, tem movimento que tem recoil
    def definir_sequencia_ataque(self, string_movimento):
        base_atual = self.linha_base[-1]
        
        if(base_atual == "base_chute"): # se estiver na base de chute, sai chute.
            if string_movimento == "ataque_leve":
                string_movimento = "chute_frente"
            else:           #então é ataque_forte
                string_movimento = "chute_lateral"
            
            self.sequencia_base = self.gerar_sequencia_completa_base(string_movimento) #base
        else: #então é soco
            if string_movimento == "ataque_leve":
                string_movimento = "soco_frente"
            else:           #então é ataque_forte
                string_movimento = "soco_tras"
           
            self.sequencia_guarda = self.gerar_sequencia_completa_guarda(string_movimento) #guarda
        pass

    def definir_sequencia_movimento(self, string_movimento): #implementar, fazer funções de gerar a sequencia mais modulares.
        vel_passo = [0,3,2,1,0] #soma 11
        vel_passo2 = [0,3,3,2,1,0] #soma 11
        vel_ameaça = [0,3,1,0,-3,-1,0] #soma 0

        #dependendo da base:
        base_atual = self.linha_base[-1]
        if base_atual == "base_agachado":   
            vel_passo = [i/2 for i in vel_passo]
            vel_passo2 = [0 for i in vel_passo2] #nao da pra correr agachado
        
        #criar sequencia e colocar ela disponível para a cena pegar a sequencia
        if string_movimento == "mover_esquerda":
            for i in vel_passo:
                self.sequencia_posicao.append(-i/13)
        if string_movimento == "mover_direita":
            for i in vel_passo:
                self.sequencia_posicao.append(i/13)
        if string_movimento == "mover_direita2":
            for i in vel_passo2:
                self.sequencia_posicao.append(i/7)
        if string_movimento == "mover_esquerda2":
            for i in vel_passo2:
                self.sequencia_posicao.append(-i/7)
        if string_movimento == "mover_direita_esquerda":
            for i in vel_ameaça:
                self.sequencia_posicao.append(i/8)
        if string_movimento == "mover_esquerda_direita":
            for i in vel_ameaça:
                self.sequencia_posicao.append(-i/8)
        #implementar
        if string_movimento == "mover_strafe_cima":
            print("mover strafe cima, implementar!")
        if string_movimento == "mover_strafe_baixo":
            print("mover strafe baixo, implementar!")
        
        pass #gerou a sequencia e colocou ela na timeline correspondente

    def definir_sequencia_postura(self, string_movimento):
        print("postura:",string_movimento)
        if string_movimento == "postura_g_b":
            self.sequencia_guarda = self.gerar_sequencia_completa_guarda("guarda_guarda")
            self.sequencia_guarda.insert(0, self.sequencia_guarda[0]) #adiciona um delay no começo
            self.sequencia_base = self.gerar_sequencia_completa_base("base_agachado")
            
        if string_movimento == "postura_b_g":
            self.sequencia_base = self.gerar_sequencia_completa_base("base_agachado")
            self.sequencia_base.insert(0,self.sequencia_base[0]) #adicionar um delay no começo
            self.sequencia_guarda = self.gerar_sequencia_completa_guarda("guarda_guarda")
        
        if string_movimento in ["postura_para","postura_para2"]:
            self.sequencia_base = self.gerar_sequencia_completa_base("base_parado")
            # self.sequencia_base.insert(0,self.sequencia_base[0]) #adicionar um delay no começo
            # self.sequencia_base.insert(0,self.sequencia_base[0]) #adicionar um delay no começo
            self.sequencia_guarda = self.gerar_sequencia_completa_guarda("guarda_parado")
            # self.sequencia_guarda.insert(0, self.sequencia_guarda[0]) #adiciona um delay no começo
            # self.sequencia_guarda.insert(0, self.sequencia_guarda[0]) #adiciona um delay no começo
        pass
        

    # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = 
    # FUNÇÔES MAIS GERAIS
    # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = # = 
    def selecionar_tipo_do_movimento_e_alocar_sequencia(self): #implementar, pra ter CANCEL, a cada comando deve-se criar uma sequencia baseado no ultimo estado que você está
        movimento_a_executar = self.pilha_pop()
        if movimento_a_executar:
            string_movimento = self.database.check_movements(movimento_a_executar)
            print("string_movimento:",string_movimento)
            
            if string_movimento.startswith("postura"):
                print("postura!!!")
                self.definir_sequencia_postura(string_movimento) #ao inves de definir, apenas gerar
            elif string_movimento.startswith("ataque"): #chute ou soco
                self.definir_sequencia_ataque(string_movimento) #ao invés de definir, apenas gerar
            elif string_movimento.startswith("guarda"): #defesa
                self.sequencia_guarda = self.gerar_sequencia_completa_guarda(string_movimento) #ok
            elif string_movimento.startswith("base"):
                self.sequencia_base = self.gerar_sequencia_completa_base(string_movimento) #ok
            elif string_movimento.startswith("mover"):
                self.definir_sequencia_movimento(string_movimento) #ao inves de definir, apenas gerar
        else:
            pass # não ha movimentos no buffer

    def update(self):
        self.selecionar_tipo_do_movimento_e_alocar_sequencia()
        # self.executar_movimentos()
        pass





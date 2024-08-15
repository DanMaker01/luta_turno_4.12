

import pygame

class Renderer:
    def __init__(self, screen, font, recursos, timeline, database, larg, alt):
        self.screen = screen
        self.font = font
        self.recursos = recursos
        self.timeline = timeline
        self.database = database
        self.cor_neutra = (100,100,100)
        self.alt = alt
        self.lar = larg

    # def desenhar_obj(self, objeto, x, y):
    #     if 

    def desenhar_bg(self):
        imagem = self.recursos.get_bg_img()
        self.screen.blit(imagem, (0, 0))

    def desenhar_hud(self):
        margem_x = 10
        margem_y = 10
        espacamento_linha = 20
        
        # Texto estático
        texto_estatico = "A: Guarda, Z: Base, Setas: Movimento"
        label_estatico = self.font.render(texto_estatico, True, (255, 255, 255))
        self.screen.blit(label_estatico, (margem_x, margem_y))

        # Renderizar guarda atual
        guarda_atual_text = self.timeline.get_ultima_guarda()
        label_linha_guarda = self.font.render(f"Guarda Atual: {guarda_atual_text,self.database.ESTADOS_GUARDA.index(guarda_atual_text)}", True, (255, 255, 255))
        self.screen.blit(label_linha_guarda, (margem_x, margem_y + espacamento_linha))

        # Renderizar base atual
        base_atual_text = self.timeline.get_ultima_base()
        label_linha_base = self.font.render(f"Base Atual: {base_atual_text,self.database.ESTADOS_BASE.index(base_atual_text)}", True, (255, 255, 255))
        self.screen.blit(label_linha_base, (margem_x, margem_y + 2 * espacamento_linha))
        
        # Renderizar sequencia_guarda em coluna
        movimentos_guarda = self.timeline.sequencia_guarda
        for i, movimento in enumerate(movimentos_guarda):
            label_movimento = self.font.render(f"Guarda seq {i + 1}: {movimento}", True, (255, 255, 255))
            self.screen.blit(label_movimento, (margem_x, margem_y + 100 + i * espacamento_linha))

        # Renderizar sequencia_base em coluna
        movimentos_base = self.timeline.sequencia_base
        for i, movimento in enumerate(movimentos_base):
            label_movimento = self.font.render(f"Base seq {i + 1}: {movimento}", True, (255, 255, 255))
            self.screen.blit(label_movimento, (margem_x + 200, margem_y + 100 + i * espacamento_linha))


    def desenhar_base(self, nome_base, x, y):
        imagem = self.recursos.get_base_img(nome_base)
        self.screen.blit(imagem, (x, y))

    def desenhar_guarda(self, nome_guarda, x, y):        
        imagem = self.recursos.get_guarda_img(nome_guarda)
        self.screen.blit(imagem, (x, y))


    def desenhar_jogador(self):
        guarda_atual = self.timeline.get_ultima_guarda()
        base_atual = self.timeline.get_ultima_base()
        posicao_atual = self.timeline.get_ultima_posicao()

        largura_img = self.recursos.get_guarda_img(guarda_atual).get_width()
        
        pos_x = posicao_atual*largura_img
        pos_y = self.alt-largura_img
        
        var_x = 0
        var_y = -largura_img
        if base_atual != "base_parado" and base_atual != "base_chute":
            var_y = -(3/4)*largura_img
        if base_atual == "base_kokutsu":
            var_x = -largura_img*(17/64)
        
        pos_x_guarda = pos_x + var_x
        pos_y_guarda = pos_y + var_y

        # print(pos_x, pos_y,var_x,var_y)
        # print(var_x, var_y)
        self.desenhar_guarda(guarda_atual, pos_x_guarda, pos_y_guarda)
        self.desenhar_base(base_atual, pos_x, pos_y)


    def draw(self):
        self.screen.fill(self.cor_neutra)  # Preenche a tela com a cor cinza
        
        # Renderizar img da base e guarda
        self.desenhar_jogador()
        
        self.desenhar_hud()
        pygame.display.flip()
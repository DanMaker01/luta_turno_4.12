# IMPLEMENTAR
# para cada sprite base deve haver um ponto pivo nos pés e um na coluna
# para cada sprite guarda deve haver um ponto pivo na coluna

import pygame


class BackgroundRenderer:
    def __init__(self, screen, recursos):
        self.screen = screen
        self.recursos = recursos

    def desenhar_bg(self):
        imagem = self.recursos.get_bg_img()[1]
        self.screen.blit(imagem, (0, 0))

class HUDRenderer:
    def __init__(self, screen, font, timeline, database, input):
        self.screen = screen
        self.font = font
        self.font_color = (20, 20, 20)
        self.timeline = timeline
        self.database = database
        self.input = input
        self.margem_x = 10
        self.margem_y = 10
        self.espacamento_linha = 20

    def desenhar_hud(self):
        # Texto estático
        self._desenhar_texto_estatico()
        # Renderizar guarda e base atual
        self._desenhar_guarda_atual()
        self._desenhar_base_atual()
        # Renderizar buffer de teclas apertadas
        self._desenhar_buffer_teclas()
        # Renderizar sequências de guarda e base
        self._desenhar_sequencias_guarda()
        self._desenhar_sequencias_base()

    def _desenhar_texto_estatico(self):
        texto_estatico = "A: Guarda, Z: Base, Setas: Movimento"
        label_estatico = self.font.render(texto_estatico, True, self.font_color)
        self.screen.blit(label_estatico, (self.margem_x, self.margem_y))

    def _desenhar_guarda_atual(self):
        guarda_atual_text = self.timeline.get_ultima_guarda()
        label_linha_guarda = self.font.render(
            f"Guarda Atual: {guarda_atual_text, self.database.ESTADOS_GUARDA.index(guarda_atual_text)}",
            True, self.font_color
        )
        self.screen.blit(label_linha_guarda, (self.margem_x, self.margem_y + self.espacamento_linha))

    def _desenhar_base_atual(self):
        base_atual_text = self.timeline.get_ultima_base()
        label_linha_base = self.font.render(
            f"Base Atual: {base_atual_text, self.database.ESTADOS_BASE.index(base_atual_text)}",
            True, self.font_color
        )
        self.screen.blit(label_linha_base, (self.margem_x, self.margem_y + 2 * self.espacamento_linha))

    def _desenhar_buffer_teclas(self):
        label_buffer = self.font.render(f"Buffer: {self.input.get_keys_pressed()}", True, self.font_color)
        self.screen.blit(label_buffer, (self.margem_x, self.margem_y + 3 * self.espacamento_linha))

    def _desenhar_sequencias_guarda(self):
        movimentos_guarda = self.timeline.sequencia_guarda
        for i, movimento in enumerate(movimentos_guarda):
            label_movimento = self.font.render(f"{i + 1}: {movimento}", True, self.font_color)
            self.screen.blit(label_movimento, (self.margem_x, self.margem_y + 100 + i * self.espacamento_linha))

    def _desenhar_sequencias_base(self):
        movimentos_base = self.timeline.sequencia_base
        for i, movimento in enumerate(movimentos_base):
            label_movimento = self.font.render(f"{i + 1}: {movimento}", True, self.font_color)
            self.screen.blit(label_movimento, (self.margem_x + 200, self.margem_y + 100 + i * self.espacamento_linha))

class PlayerRenderer:
    def __init__(self, screen, recursos, timeline, larg, alt):
        self.screen = screen
        self.recursos = recursos
        self.timeline = timeline
        self.largura = larg
        self.altura = alt

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
        altura_img = self.recursos.get_guarda_img(guarda_atual).get_height()

        pos_x = posicao_atual * largura_img
        pos_y = self.altura - altura_img

        var_x, var_y = self._calcular_variacoes(guarda_atual, base_atual, largura_img, altura_img)

        pos_x_guarda = pos_x + var_x
        pos_y_guarda = pos_y + var_y

        self.desenhar_guarda(guarda_atual, pos_x_guarda, pos_y_guarda)
        self.desenhar_base(base_atual, pos_x, pos_y)

    def _calcular_variacoes(self, guarda_atual, base_atual, largura_img, altura_img):
        var_x = 0#-largura_img * (1 / 256)
        var_y = -altura_img + (1 / 8) * altura_img

        if base_atual not in ["base_parado", "base_chute"]:
            var_y = -(3 / 4) * altura_img
        
        if base_atual == "base_agachado":
            var_x += largura_img * (0 / 256)
        if base_atual == "base_parado":
            var_x = -largura_img * (2 / 256)
        if base_atual == "base_kokutsu":
            var_x = -largura_img * (67 / 256)
        if base_atual == "base_zenkutsu":
            var_x = largura_img * (0 / 64)
        if base_atual == "base_cavaleiro":
            var_x = largura_img * (0)
        if base_atual == "base_chute":
            var_x = largura_img * (0 / 64)
        
        if base_atual == "chute_frente":
            var_x += -largura_img * (11 / 64)
        if base_atual == "chute_lateral":
            var_x += -largura_img * (65 / 256)

        if guarda_atual in ["guarda_defesa_alto", "guarda_defesa_baixo"]:
            var_x += largura_img * (1 / 64)
        if guarda_atual == "soco_tras":
            var_x += largura_img * (1 / 64)
            var_y += altura_img * (1 / 32)

        return var_x, var_y

class Renderer:
    def __init__(self, screen, font, recursos, timeline, database, input, larg, alt):
        self.bg_renderer = BackgroundRenderer(screen, recursos)
        self.hud_renderer = HUDRenderer(screen, font, timeline, database, input)
        self.player_renderer = PlayerRenderer(screen, recursos, timeline, larg, alt)
        self.screen = screen
        self.cor_neutra = (100, 100, 100)

    def draw(self):
        self.screen.fill(self.cor_neutra)  # Preenche a tela com a cor cinza
        self.bg_renderer.desenhar_bg()  # Renderizar o fundo
        self.player_renderer.desenhar_jogador()  # Renderizar o jogador
        self.hud_renderer.desenhar_hud()  # Renderizar o HUD
        pygame.display.flip()

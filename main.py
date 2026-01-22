import pygame 
from pygame.locals import *
import sys
import json
import numpy as np
import math
from primitive import Primitive
from open_scene import OpenScene
import transform
import random

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1280, 768
        self.colors = None
        self.clock = pygame.time.Clock()
        self.angle = 0.0
        self.pos_x = 0.0

        self.entities = []
        types = ["stone", "paper", "scissors"]
        for _ in range(10): # Criar 10 objetos iniciais
            self.entities.append({
                "type": random.choice(types),
                "x": random.randint(100, 1100),
                "y": random.randint(100, 600),
                "dx": random.uniform(-3, 3), # Velocidade horizontal
                "dy": random.uniform(-3, 3), # Velocidade vertical
                "angle": 0.0,
                "timer": random.randint(30, 90) # Tempo para mudar de direção
            })

    def on_init(self):
        pygame.init()
        self.load_colors()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.drawer = Primitive(self._display_surf)

        opening = OpenScene(self._display_surf)
        self._display_surf.fill((0, 0, 0)) 
        pygame.display.flip()
        
        opening.draw_logo()
        pygame.display.flip()
        
        # Espera 3 segundos
        pygame.time.delay(3000)

        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):        
        # Incrementa o ângulo para rotação contínua
        self.angle += 0.05 
        # Oscila a posição X para um movimento de vai e vem
        self.pos_x = 300 * math.sin(self.angle)

        for ent in self.entities:
            # Movimentação contínua
            ent["x"] += ent["dx"]
            ent["y"] += ent["dy"]
            ent["angle"] += 0.05
            
            # Rebater nas bordas (Sistema de Coordenadas de Dispositivo)
            if ent["x"] < 50 or ent["x"] > 1230:
                ent["dx"] *= -1
            if ent["y"] < 50 or ent["y"] > 718:
                ent["dy"] *= -1

            # Mudar direção aleatoriamente após um tempo
            ent["timer"] -= 1
            if ent["timer"] <= 0:
                ent["dx"] = random.uniform(-3, 3)
                ent["dy"] = random.uniform(-3, 3)
                ent["timer"] = random.randint(60, 180) # Reinicia o cronômetro

    def on_render(self):
        """self._display_surf.fill((0, 0, 0))
    
        # Modelos de pontos centralizados na origem (0,0)
        models = {
            "scissors": [(0, -20), (20, 20), (-20, 20)], # Triângulo [cite: 6]
            "paper": [(-20, -20), (20, -20), (20, 20), (-20, 20)], # Quadrado 
            "stone": [(10, -17), (20, 0), (10, 17), (-10, 17), (-20, 0), (-10, -17)] # Hexágono (Círculo simplificado)
        }

        for ent in self.entities:
            # Criar matriz de transformação para cada objeto [cite: 11, 24]
            m = transform.cria_transformacao()
            m = transform.multiplica_matrizes(transform.rotacao(ent["angle"]), m)
            m = transform.multiplica_matrizes(transform.translacao(ent["x"], ent["y"]), m)
            
            # Aplicar transformação
            pts_originais = models[ent["type"]]
            pts_transformados = transform.aplica_transformacao(m, pts_originais)
            pts_int = [(int(p[0]), int(p[1])) for p in pts_transformados]
            
            # Definir cor baseada no tipo
            color = self.colors["red"] if ent["type"] == "scissors" else \
                    self.colors["white"] if ent["type"] == "paper" else self.colors["light_gray"]
            
            # Preenchimento obrigatório por Scanline 
            self.drawer.scanline_fill(pts_int, color)
            # Contorno [cite: 22]
            self.drawer.draw_polygon(pts_transformados, self.colors["black"])

        pygame.display.flip()"""
        
        self._display_surf.fill((0, 0, 0))
        
        # Definições de Janela (Mundo) e Viewport (Tela) 
        mundo = (0, 0, 1280, 768)
        # Minimapa no canto superior esquerdo (10, 10) com 200px de largura
        viewport_mini = (10, 10, 210, 130) 
        
        # Criar matriz de mapeamento Janela-Viewport
        m_viewport = transform.janela_viewport(mundo, viewport_mini)

        models = {
            "scissors": [(0, -20), (20, 20), (-20, 20)],
            "paper": [(-20, -20), (20, -20), (20, 20), (-20, 20)],
            "stone": [(10, -17), (20, 0), (10, 17), (-10, 17), (-20, 0), (-10, -17)]
        }

        # Loop de desenho
        for ent in self.entities:
            # CENA PRINCIPAL
            m = transform.cria_transformacao()
            m = transform.multiplica_matrizes(transform.rotacao(ent["angle"]), m)
            m = transform.multiplica_matrizes(transform.translacao(ent["x"], ent["y"]), m)
            
            pts_trans = transform.aplica_transformacao(m, models[ent["type"]])
            color = self.colors["red"] if ent["type"] == "scissors" else \
                    self.colors["white"] if ent["type"] == "paper" else self.colors["light_gray"]
            
            # Desenha no mundo real
            pts_int = [(int(p[0]), int(p[1])) for p in pts_trans]
            self.drawer.scanline_fill(pts_int, color)
            self.drawer.draw_polygon(pts_trans, self.colors["black"])

            # MINIMAPA (VIEWPORT)
            # Aplica a transformação de viewport sobre os pontos já transformados do mundo
            pts_mini = transform.aplica_transformacao(m_viewport, pts_trans)
            pts_mini_int = [(int(p[0]), int(p[1])) for p in pts_mini]
            
            # Desenha no minimapa
            self.drawer.scanline_fill(pts_mini_int, color)

        # Desenhar borda do minimapa
        self.drawer.draw_rectangle(10, 10, 200, 120, self.colors["white"])

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        pygame.display.set_caption("Simulação")
        self.clock.tick(60)

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def load_colors(self):
        with open('colors.json', 'r') as f:
            self.colors = json.load(f)

if __name__ == "__main__" : 
    theApp = App()
    theApp.on_execute()
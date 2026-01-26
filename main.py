import pygame 
from pygame.locals import *
import sys
import json
import numpy as np
import math
from primitive import Primitive
from open_scene import OpenScene
from transform import Transform
import random
from entity import Entity
from menu import Menu

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1280, 768
        self.colors = None
        self.clock = pygame.time.Clock()
        self.entities = []
        self.state = "OPENING" 
        self.menu = None

    def on_init(self):
        pygame.init()
        self.load_colors()

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.drawer = Primitive(self._display_surf)

        # Instancia o menu
        self.menu = Menu(self._display_surf, self.colors)

        opening = OpenScene(self._display_surf, self.colors)
        self._display_surf.fill(self.colors["black"]) 
        
        opening.draw_logo()
        pygame.display.flip()

        pygame.time.delay(3000)
        self.state = "MENU"

        for _ in range(10):
            self.entities.append(
                Entity("scissors", 
                random.randint(100, 1100), 
                random.randint(100, 600), 
                self.colors)
            )
            self.entities.append(
                Entity("paper", 
                random.randint(100, 1100), 
                random.randint(100, 600), 
                self.colors)
            )
            self.entities.append(
                Entity("stone", 
                random.randint(100, 1100), 
                random.randint(100, 600), 
                self.colors)
            )

        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        
        if self.state == "MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menu.navigate(-1)
                elif event.key == pygame.K_DOWN:
                    self.menu.navigate(1)
                elif event.key == pygame.K_SPACE:
                    selection = self.menu.get_selection()
                    if selection == "Iniciar":
                        self.state = "SIMULATION"
                    elif selection == "Sair":
                        self._running = False

    def on_loop(self):   
        if self.state == "SIMULATION":
            for entity in self.entities:
                entity.update(self.weight, self.height, self.entities)
        
    def on_render(self):
        if self.state == "MENU":
            self.menu.draw() 
            pygame.display.flip()
        elif self.state == "SIMULATION":
            # 1. Limpa a tela principal 
            self._display_surf.fill(self.colors["black"])
            
            # 2. Desenha entidades na cena principal 
            for ent in self.entities:
                ent.draw(self.drawer)

            # CONFIGURAÇÃO DA VIEWPORT (MINIMAPA) 
            # Limites da Viewport: xmin, ymin, xmax, ymax 
            v_xmin, v_ymin, v_xmax, v_ymax = 10, 10, 210, 130
            world_window = (0, 0, self.weight, self.height)

            # 3. "Limpa" a área do minimapa 
            pygame.draw.rect(self._display_surf, self.colors["black"], (v_xmin, v_ymin, 200, 120))
            self.drawer.draw_rectangle(v_xmin, v_ymin, 200, 120, self.colors["white"])

            # 4. Matriz de mapeamento Mundo -> Viewport
            m_viewport = Transform.window_viewport(world_window, (v_xmin, v_ymin, v_xmax, v_ymax))

            for ent in self.entities:
                # Pega os pontos transformados da entidade no mundo
                m_ent = Transform.create_transformation()
                m_ent = Transform.multiply_matrices(Transform.rotation(ent.angle), m_ent)
                m_ent = Transform.multiply_matrices(Transform.translation(ent.x, ent.y), m_ent)
                pts_mundo = Transform.apply_transformation(m_ent, ent.model)
                
                # Mapeia os pontos do mundo para a Viewport 
                pts_mini = Transform.apply_transformation(m_viewport, pts_mundo)

                # 5. APLICAÇÃO DO RECORTE (Cohen-Sutherland) 
                # Itera sobre cada aresta do polígono
                for i in range(len(pts_mini)):
                    p0 = pts_mini[i]
                    p1 = pts_mini[(i + 1) % len(pts_mini)] # Próximo ponto (fecha o polígono)
                    
                    visivel, nx0, ny0, nx1, ny1 = Transform.cohen_sutherland(
                        p0[0], p0[1], p1[0], p1[1], 
                        v_xmin, v_ymin, v_xmax, v_ymax
                    )
                    
                    # Se a linha for visível (total ou parcialmente), desenha o segmento recortado
                    if visivel:
                        self.drawer.draw_line_bress(int(nx0), int(ny0), int(nx1), int(ny1), ent.color)

            pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        pygame.display.set_caption("Pedra Papel Tesoura")
        self.clock.tick(60)

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def load_colors(self):
        try:
            with open('colors.json', 'r') as f:
                self.colors = json.load(f)
        except:
            self.colors = {
                "black": (0, 0, 0),
                "white": (255, 255, 255),
                "offset_black": (3, 3, 3),
                "dark_gray": (33, 33, 33),
                "medium_gray": (100, 100, 100),
                "light_gray": (200, 200, 200),
                "silver": (192, 192, 192),
                "charcoal": (54, 69, 79),
                "red": (255, 0, 0),
                "crimson": (220, 20, 60),
                "maroon": (128, 0, 0),
                "coral": (255, 127, 80),
                "green": (0, 255, 0),
                "emerald": (80, 200, 120),
                "forest_green": (34, 139, 34),
                "lime": (191, 255, 0),
                "blue": (0, 0, 255),
                "sapphire": (15, 82, 186),
                "azure_mist": (240, 255, 255),
                "sky_blue": (135, 206, 235),
                "deep_ocean": (0, 75, 120),
                "navy_blue": (0, 0, 128),
                "steel_blue": (70, 130, 180),
                "cyan": (0, 255, 255),
                "yellow": (255, 255, 0),
                "gold": (255, 215, 0),
                "amber": (255, 191, 0),
                "orange": (255, 165, 0),
                "magenta": (255, 0, 255),
                "purple": (128, 0, 128),
                "violet": (238, 130, 238),
                "indigo": (75, 0, 130),
                "brown": (139, 69, 19),
                "chocolate": (210, 105, 30),
                "sand": (194, 178, 128)
            }

if __name__ == "__main__" : 
    theApp = App()
    theApp.on_execute()
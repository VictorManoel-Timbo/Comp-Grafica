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
        self.textures = None
        self.clock = pygame.time.Clock()
        self.entities = []
        self.state = "OPENING" 
        self.menu = None

    def on_init(self):
        pygame.init()
        self.load_colors()
        self.load_textures()

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.drawer = Primitive(self._display_surf)

        self.menu = Menu(self._display_surf, self.colors, self.textures)

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
            self._display_surf.fill(self.colors["black"])
            
            for ent in self.entities:
                ent.draw(self.drawer)

            self.draw_minimap()

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

    def draw_minimap(self):
        v_xmin, v_ymin, v_xmax, v_ymax = 10, 10, 210, 130
        world_window = (0, 0, self.weight, self.height)

        pygame.draw.rect(self._display_surf, self.colors["black"], (v_xmin, v_ymin, 200, 120))
        self.drawer.draw_rectangle(v_xmin, v_ymin, 200, 120, self.colors["white"])

        m_viewport = Transform.window_viewport(world_window, (v_xmin, v_ymin, v_xmax, v_ymax))

        for ent in self.entities:
            m_ent = Transform.create_transformation()
            m_ent = Transform.multiply_matrices(Transform.rotation(ent.angle), m_ent)
            m_ent = Transform.multiply_matrices(Transform.translation(ent.x, ent.y), m_ent)
            pts_mundo = Transform.apply_transformation(m_ent, ent.model)
            
            pts_mini = Transform.apply_transformation(m_viewport, pts_mundo)

            self.render_clipped_entity(pts_mini, ent.color, (v_xmin, v_ymin, v_xmax, v_ymax))

    def render_clipped_entity(self, points, color, viewport_limits):
        v_xmin, v_ymin, v_xmax, v_ymax = viewport_limits
        
        for i in range(len(points)):
            p0 = points[i]
            p1 = points[(i + 1) % len(points)] 
            
            visivel, nx0, ny0, nx1, ny1 = Transform.cohen_sutherland(
                p0[0], p0[1], p1[0], p1[1], 
                v_xmin, v_ymin, v_xmax, v_ymax
            )
            
            if visivel:
                self.drawer.draw_line_bress(int(nx0), int(ny0), int(nx1), int(ny1), color)

    def load_textures(self):
        try:
            with open('textures.json', 'r') as f:
                self.textures = json.load(f)
        except:
            self.textures = {
                "table": "img/table.png",
                "stone": "img/stone.png",
                "paper": "img/paper.jpg"
            }

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
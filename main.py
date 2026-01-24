import pygame 
from pygame.locals import *
import sys
import json
import numpy as np
from primitive import Primitive
from open_scene import OpenScene
import transform
import random
from entity import Entity

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 1280, 768
        self.colors = None
        self.clock = pygame.time.Clock()
        self.entities = []

    def on_init(self):
        pygame.init()
        self.load_colors()

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.drawer = Primitive(self._display_surf)

        opening = OpenScene(self._display_surf, self.colors)
        self._display_surf.fill(self.colors["gold"]) 
        
        opening.draw_logo()
        pygame.display.flip()

        for _ in range(20):
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

        
        pygame.time.delay(3000)
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):   
        for entity in self.entities:
            entity.update(self.weight, self.height, self.entities)
    def on_render(self):
        self._display_surf.fill(self.colors["gold"])
        mundo = (0, 0, self.weight, self.height)

        viewport_mini = (10, 10, 210, 130) 
        m_viewport = transform.janela_viewport(mundo, viewport_mini)

        for entity in self.entities:
            entity.draw(self.drawer, m_viewport)

        # Borda do minimapa
        self.drawer.draw_rectangle(10, 10, 200, 120, self.colors["white"])
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
import pygame 
from pygame.locals import *
import sys
import json
import numpy as np
from primitive import Primitive
from open_scene import OpenScene
from transform import Transform
import random
from entity import Entity
from menu import Menu
from mixer import Mixer

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
        self.pause_options = ["Continuar", "Reiniciar", "Sair"]
        self.pause_index = 0

    def on_init(self):
        pygame.init()
        self.load_colors()

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.load_textures()

        self.drawer = Primitive(self._display_surf)
        self.menu = Menu(self._display_surf, self.colors, self.textures)

        opening = OpenScene(self._display_surf, self.colors)
        self._display_surf.fill(self.colors["black"]) 
        
        opening.draw_logo()
        pygame.display.flip()

        pygame.time.delay(3000)
        self.state = "MENU"

        self.reset_simulation()
        self._running = True
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self._toggle_pause()

        if self.state == "MENU":
            self._handle_menu_events(event)

        elif self.state == "PAUSED":
            self._handle_pause_events(event)

    def on_loop(self):   
        if self.state == "SIMULATION":
            for entity in self.entities:
                entity.update(self.weight, self.height, self.entities)
            
            if self.check_victory():
                self.state = "PAUSED" 
        
    def on_render(self):
        if self.state == "MENU":
            self.menu.draw() 
            pygame.display.flip()

        elif self.state == "SIMULATION" or self.state == "PAUSED":
            self._display_surf.fill(self.colors["black"])
            
            for ent in self.entities:
                ent.draw(self.drawer)

            self.draw_minimap()

            if self.state == "PAUSED":
                self._render_pause_overlay()

            pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        
        pygame.display.set_caption("Pedra Papel Tesoura")
        self.clock.tick(60)
        mixer = Mixer()
        simulation_loaded = False
        mixer.load_music("music/8b0rws1ViH.mp3")
        while( self._running ):
            if self.state == "SIMULATION" and not simulation_loaded:
                simulation_loaded = True
                mixer.stop_music()
                mixer.load_music("music/PJb7DdPD00.mp3")
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def reset_simulation(self):
        self.entities = []
        for _ in range(15):
            self.entities.append(Entity("scissors", random.randint(100, 1100), random.randint(100, 600), self.colors))
            self.entities.append(Entity("paper", random.randint(100, 1100), random.randint(100, 600), self.colors))
            self.entities.append(Entity("stone", random.randint(100, 1100), random.randint(100, 600), self.colors))
    
    def check_victory(self):
        if not self.entities:
            return False
        
        first_type = self.entities[0].type
        for ent in self.entities:
            if ent.type != first_type:
                return False 
        
        return True 

    def _render_pause_overlay(self):
        overlay = pygame.Surface(self.size) 
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self._display_surf.blit(overlay, (0, 0))

        font = pygame.font.SysFont("Arial", 30, bold=True)

        if self.check_victory():
            winner = self.entities[0].type.upper()
            text = font.render(f"{winner} VENCEU!!! [Espaço para Sair]", True, self.colors["gold"])
            rect = text.get_rect(center=(self.weight // 2, self.height // 2))
            self._display_surf.blit(text, rect)
        else:
            for i, opt in enumerate(self.pause_options):
                color = self.colors["sapphire"] if i == self.pause_index else self.colors["charcoal"]
                bx, by = self.weight//2 - 100, self.height//2 - 50 + (i * 70)
                self.drawer.draw_rectangle(bx, by, 200, 50, self.colors["white"], color)
                
                btn_txt = font.render(opt, True, self.colors["white"])
                self._display_surf.blit(btn_txt, btn_txt.get_rect(center=(bx+100, by+25)))
    
    def draw_minimap(self):
        # VIEWPORT 1
        v1_limits = (10, 10, 210, 130)
        world_v1 = (0, 0, self.weight, self.height)
        
        # VIEWPORT 2
        v2_limits = (1070, 10, 1270, 130)
        zoom_size = 100 
        cx, cy = self.weight // 2, self.height // 2
        world_v2 = (cx - zoom_size//2, cy - zoom_size//2, cx + zoom_size//2, cy + zoom_size//2)

        m_v1 = Transform.window_viewport(world_v1, v1_limits)
        m_v2 = Transform.window_viewport(world_v2, v2_limits)

        # fundos e molduras
        for v_limits in [v1_limits, v2_limits]:
            vx0, vy0, vx1, vy1 = v_limits
            pygame.draw.rect(self._display_surf, self.colors["black"], (vx0, vy0, 200, 120))
            self.drawer.draw_rectangle(vx0, vy0, 200, 120, self.colors["white"])

        # Renderização das Entidades
        for ent in self.entities:
            m_ent = Transform.create_transformation()
            m_ent = Transform.multiply_matrices(Transform.rotation(ent.angle), m_ent)
            m_ent = Transform.multiply_matrices(Transform.translation(ent.x, ent.y), m_ent)
            pts_world = Transform.apply_transformation(m_ent, ent.model)
            
            uvs_orig = self.drawer._generate_uvs(ent.model)
            tex = self.textures.get(ent.type)

            for m_view, v_limits in [(m_v1, v1_limits), (m_v2, v2_limits)]:
                pts_view = Transform.apply_transformation(m_view, pts_world)
                
                vertices = []
                for i in range(len(pts_view)):
                    vertices.append((pts_view[i][0], pts_view[i][1], uvs_orig[i][0], uvs_orig[i][1]))

                pts_clipped = Transform.sutherland_hodgman(vertices, v_limits[0], v_limits[1], v_limits[2], v_limits[3])

                if len(pts_clipped) >= 3:
                    f_pts = [(v[0], v[1]) for v in pts_clipped]
                    f_uvs = [(v[2], v[3]) for v in pts_clipped]
                    
                    self.drawer.draw_polygon(f_pts, color=self.colors["white"], uvs=f_uvs, texture=tex)

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
    
    def _toggle_pause(self):
        if self.state == "SIMULATION":
            self.state = "PAUSED"
            self.pause_index = 0
        elif self.state == "PAUSED" and not self.check_victory():
            self.state = "SIMULATION"

    def _handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu.navigate(-1)
            elif event.key == pygame.K_DOWN:
                self.menu.navigate(1)
            elif event.key == pygame.K_SPACE:
                selection = self.menu.get_selection()
                if selection == "Iniciar":
                    self.reset_simulation()
                    self.state = "SIMULATION"
                elif selection == "Sair":
                    self._running = False

    def _handle_pause_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.check_victory():
                self._running = False

            if event.key == pygame.K_UP:
                self.pause_index = (self.pause_index - 1) % len(self.pause_options)
            elif event.key == pygame.K_DOWN:
                self.pause_index = (self.pause_index + 1) % len(self.pause_options)
            elif event.key == pygame.K_SPACE:
                sel = self.pause_options[self.pause_index]
                if sel == "Continuar": self.state = "SIMULATION"
                elif sel == "Reiniciar":
                    self.reset_simulation()
                    self.state = "SIMULATION"
                elif sel == "Sair": self.state = "MENU"
    
    def load_textures(self):
        paths = {
            "table": "img/table.png",
            "stone": "img/stone.png",
            "paper": "img/paper.jpg",
            "scissor": "img/scissor.png"
        }
        
        self.textures = {}
        for name, path in paths.items():
            try:
                surf = pygame.image.load(path).convert()
                self.textures[name] = surf
            except:
                fallback = pygame.Surface((64, 64))
                fallback.fill(self.colors["orange"]) 
                self.textures[name] = fallback

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
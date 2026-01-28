import pygame
import math
from primitive import Primitive
from transform import Transform

class Menu:
    def __init__(self, surface, colors,  textures):
        self.surface = surface
        self.drawer = Primitive(self.surface)
        self.colors = colors
        self.textures = textures
        self.selected_index = 0  
        self.options = ["Iniciar", "Sair"]
        self.button_width = 200
        self.button_height = 50
        self.center_x = self.surface.get_width() // 2
        self.start_y = 450
        self.angle = 0
        self.paper = [(-20, -20), (20, -20), (20, 20), (-20, 20)]
        self.scissors = [(-1, 5), (-10, 5), (-10, 15),(-1,20),(-10,20),(-10,40),(0,20),(10,40),(10,20),(1,20),(10,15),(10,5),(1,5),(0,20)]
        self.stone = [(10, -17), (20, 0), (10, 17), (-10, 17), (-20, 0), (-10, -17)]

        self.star = self.create_star_points(0, 0, 30, 15)

        self.uvs_stone = self.drawer._generate_uvs(self.stone)
        self.uvs_paper = self.drawer._generate_uvs(self.paper)
        self.uvs_scissors = self.drawer._generate_uvs(self.scissors)

        self.background_cache = self._create_gradient_background()

    def draw(self):
        self.surface.blit(self.background_cache, (0, 0))
        self.angle += 0.02

        # ESTRELA 
        m_star = Transform.create_transformation()
        m_star = Transform.multiply_matrices(Transform.scale(4, 4), m_star)
        m_star = Transform.multiply_matrices(Transform.translation(640, 384), m_star)
        
        star_transformed = Transform.apply_transformation(m_star, self.star)

        brightness_color = self.colors["white"]       # Pontos de luz
        base_color = self.colors["gold"]         # Cor principal
        shadow_color = self.colors["orange"]      # Profundidade

        # Definição das 10 cores para os vértices da estrela
        cores_estrela = [
            brightness_color, shadow_color,  # Ponta 1, Vale 1
            base_color,   shadow_color,  # Ponta 2, Vale 2
            brightness_color, shadow_color,  # Ponta 3, Vale 3
            base_color,   shadow_color,  # Ponta 4, Vale 4
            brightness_color, shadow_color   # Ponta 5, Vale 5
        ]

        self.drawer.scanline_fill_gradient(star_transformed, cores_estrela)
        self.drawer.draw_polygon(star_transformed, self.colors["white"])

        background_shapes = [
            # Lado Esquerdo
            (self.stone, (200, 200), None, 1, self.uvs_stone, self.textures["stone"]),
            (self.paper, (200, 550), None, -1, self.uvs_paper, self.textures["paper"]),
            
            # Lado Direito
            (self.scissors, (1080, 200), self.colors["red"], 1, self.uvs_scissors, self.textures["scissor"]),
            (self.stone, (1080, 550), None, -1, self.uvs_stone, self.textures["stone"]),
            
            # Centro (Topo e Baixo)
            (self.paper, (640, 100), None, 1, self.uvs_paper, self.textures["paper"]),
            (self.scissors, (640, 700), self.colors["red"], -1, self.uvs_scissors, self.textures["scissor"])
        ]

        for model_points, pos, fill_color, direction, uvs, tex in background_shapes:
            m = Transform.create_transformation()
            m = Transform.multiply_matrices(Transform.scale(4, 4), m)
            m = Transform.multiply_matrices(Transform.rotation(self.angle * direction), m)
            m = Transform.multiply_matrices(Transform.translation(pos[0], pos[1]), m)
            
            transformed_pts = Transform.apply_transformation(m, model_points)
            self.drawer.draw_polygon(transformed_pts, self.colors["black"], fill_color, uvs, tex)
            
        self._draw_ui()


    def _draw_ui(self):
        pygame.font.init()
        font_title = pygame.font.SysFont("Arial", 60, bold=True)
        font_button = pygame.font.SysFont("Arial", 30, bold=True)

        title_parts = ["PEDRA", "PAPEL", "TESOURA"]
        for i, word in enumerate(title_parts):
            text_surf = font_title.render(word, True, self.colors["amber"])
            text_rect = text_surf.get_rect(center=(self.center_x, 100 + i * 80))
            self.surface.blit(text_surf, text_rect)

        # Desenho dos Botões
        for i, option in enumerate(self.options):
            rect_x = self.center_x - self.button_width // 2
            rect_y = self.start_y + i * (self.button_height + 20)
            
            # Cor de destaque
            color_bg = self.colors["sapphire"] if i == self.selected_index else self.colors["charcoal"]
            
            self.drawer.draw_rectangle(rect_x, rect_y, self.button_width, self.button_height, self.colors["silver"], color_bg)
            
            btn_text = font_button.render(option, True, self.colors["black"])
            btn_rect = btn_text.get_rect(center=(self.center_x, rect_y + self.button_height // 2))
            self.surface.blit(btn_text, btn_rect)

    def _create_gradient_background(self):
        bg = pygame.Surface((self.surface.get_width(), self.surface.get_height()))
        drawer_bg = Primitive(bg) 
        
        width, height = bg.get_width(), bg.get_height()
        pontos = [(0, 0), (width, 0), (width, height), (0, height)]
        
        # Cores do degradê
        soft_color = self.colors["sky_blue"]
        hard_color = self.colors["navy_blue"]
        colors = [soft_color, soft_color, hard_color, hard_color]
        
        drawer_bg.scanline_fill_gradient(pontos, colors)
        return bg

    def navigate(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.options)

    def get_selection(self):
        return self.options[self.selected_index]
    
    def create_star_points(self, cx, cy, out_radius, in_radius):
        num_points = 5
        points = []

        total_vertices = num_points * 2
        
        for i in range(total_vertices):
            r = out_radius if i % 2 == 0 else in_radius
            
            # Calcula o ângulo de cada vértice (em radianos)
            angle = (math.pi * i / num_points) - (math.pi / 2)
            
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append((x, y))
            
        return points
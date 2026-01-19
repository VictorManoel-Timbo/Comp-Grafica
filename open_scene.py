import pygame
import json
from primitive import Primitive

class OpenScene:
    def __init__(self, surface):
        self.surface = surface
        self.drawer = Primitive(self.surface)
        with open('colors.json', 'r') as f:
            self.fill_colors = json.load(f)

    def boundary_fill(self, x, y, color_fill, color_boundary):
        width, height = self.surface.get_width(), self.surface.get_height()
        target = tuple(color_fill)
        boundary = tuple(color_boundary)
        
        start_pixel = self.surface.get_at((int(x), int(y)))[:3]
        if start_pixel == boundary or start_pixel == target:
            return

        stack = [(int(x), int(y))]
        while stack:
            curr_x, curr_y = stack.pop()
            if not (0 <= curr_x < width and 0 <= curr_y < height):
                continue
            
            pixel_color = self.surface.get_at((curr_x, curr_y))[:3]
            if pixel_color != boundary and pixel_color != target:
                self.surface.set_at((curr_x, curr_y), target)
                stack.append((curr_x + 1, curr_y))
                stack.append((curr_x - 1, curr_y))
                stack.append((curr_x, curr_y + 1))
                stack.append((curr_x, curr_y - 1))

    def draw_logo(self):
        cx, cy = 640, 384
        
        # --- DESENHO DOS CONTORNOS ---
        pts_caminho = [(cx-50, cy+150), (cx+50, cy+150), (cx+120, cy+300), (cx-120, cy+300)]
        self.drawer.draw_polygon(pts_caminho, self.fill_colors["offset_black"])
        
        self.drawer.draw_rectangle(cx-150, cy-100, 300, 250, self.fill_colors["offset_black"])
        
        self.drawer.draw_triangle(cx-170, cy-100, cx+170, cy-100, cx, cy-250, self.fill_colors["offset_black"])
        
        pts_alca = [(cx+150, cy-50), (cx+250, cy-50), (cx+250, cy+100), (cx+150, cy+100), (cx+150, cy+60), (cx+200, cy+60), (cx+200, cy-10), (cx+150, cy-10)]
        self.drawer.draw_polygon(pts_alca, self.fill_colors["offset_black"])

        # --- PREENCHIMENTO ---
        # Sementes ajustadas (1 pixel de margem para não tocar o contorno)
        self.boundary_fill(cx, cy, self.fill_colors["red"], self.fill_colors["offset_black"])         # Caneca
        self.boundary_fill(cx, cy-150, self.fill_colors["green"], self.fill_colors["offset_black"])  # Telhado
        self.boundary_fill(cx, cy+200, self.fill_colors["blue"], self.fill_colors["offset_black"]) # Caminho
        self.boundary_fill(cx+220, cy, self.fill_colors["red"], self.fill_colors["offset_black"])    # Alças
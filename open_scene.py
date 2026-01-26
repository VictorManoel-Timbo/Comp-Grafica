import pygame
import json
from primitive import Primitive

class OpenScene:
    def __init__(self, surface, colors):
        self.surface = surface
        self.drawer = Primitive(self.surface)
        self.colors = colors

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
        off_y = -70  # Ajuste vertical
        
        b_color = tuple(self.colors["offset_black"])
        c_fill = tuple(self.colors["azure_mist"])
        d_fill = tuple(self.colors["sky_blue"])
        e_fill = tuple(self.colors["deep_ocean"])

        # Pontos principais da coroa 
        p_norte, p_sul = (cx, cy - 62 + off_y), (cx, cy + 62 + off_y)
        p_leste, p_oeste = (cx + 125, cy + off_y), (cx - 125, cy + off_y)
        p_ne, p_se = (cx + 82, cy - 45 + off_y), (cx + 82, cy + 45 + off_y)
        p_so, p_no = (cx - 82, cy + 45 + off_y), (cx - 82, cy - 45 + off_y)
        
        # Pontas e base 
        p_ponta_oso = (cx - 142, cy + 62 + off_y) 
        p_ponta_sos = (cx - 61, cy + 122 + off_y)
        p_ponta_sse = (cx + 61, cy + 122 + off_y)
        p_ponta_sel = (cx + 142, cy + 62 + off_y)
        p_culatra = (cx, cy + 200 + off_y)

        oct_pts = [p_norte, p_ne, p_leste, p_se, p_sul, p_so, p_oeste, p_no]

        self.drawer.draw_circunference_bress(cx, cy + off_y + 50, 180, b_color)
        self.drawer.draw_circunference_bress(cx, cy + off_y + 50, 160, b_color)

        self.boundary_fill(cx + 165, cy + off_y + 40, tuple(self.colors["gold"]), b_color) # anel
        self.boundary_fill(cx, cy + off_y + 40, tuple(self.colors["steel_blue"]), b_color)

        # coroa
        self.drawer.draw_polygon(oct_pts, b_color)

        # triângulos da base da coroa
        self.drawer.draw_triangle(p_oeste[0], p_oeste[1], p_so[0], p_so[1], p_ponta_oso[0], p_ponta_oso[1], b_color)
        self.drawer.draw_triangle(p_so[0], p_so[1], p_sul[0], p_sul[1], p_ponta_sos[0], p_ponta_sos[1], b_color)
        self.drawer.draw_triangle(p_sul[0], p_sul[1], p_se[0], p_se[1], p_ponta_sse[0], p_ponta_sse[1], b_color)
        self.drawer.draw_triangle(p_se[0], p_se[1], p_leste[0], p_leste[1], p_ponta_sel[0], p_ponta_sel[1], b_color)

        # ponta do diamante
        self.drawer.draw_triangle(p_ponta_oso[0], p_ponta_oso[1], p_ponta_sos[0], p_ponta_sos[1], p_culatra[0], p_culatra[1], b_color)
        self.drawer.draw_triangle(p_ponta_sos[0], p_ponta_sos[1], p_ponta_sse[0], p_ponta_sse[1], p_culatra[0], p_culatra[1], b_color)
        self.drawer.draw_triangle(p_ponta_sse[0], p_ponta_sse[1], p_ponta_sel[0], p_ponta_sel[1], p_culatra[0], p_culatra[1], b_color)

        pygame.display.flip()

        # Preenchimentos 
        self.boundary_fill(cx, cy + off_y, c_fill, b_color) # coroa

        # base da coroa
        self.boundary_fill(cx - 115, cy + 52 + off_y, d_fill, b_color)
        self.boundary_fill(cx - 47, cy + 77 + off_y, d_fill, b_color)
        self.boundary_fill(cx + 47, cy + 77 + off_y, d_fill, b_color)
        self.boundary_fill(cx + 115, cy + 52 + off_y, d_fill, b_color)
        self.boundary_fill(cx - 92, cy + 75 + off_y, d_fill, b_color)
        self.boundary_fill(cx, cy + 100 + off_y, d_fill, b_color)
        self.boundary_fill(cx + 92, cy + 75 + off_y, d_fill, b_color)

        # ponta
        self.boundary_fill(cx - 65, cy + 125 + off_y, e_fill, b_color)
        self.boundary_fill(cx, cy + 150 + off_y, e_fill, b_color)
        self.boundary_fill(cx + 65, cy + 125 + off_y, e_fill, b_color)

        # Texto 
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 18, bold=True)
        
        text_surface = font.render("PARCELADOS PICTURY", True, tuple(self.colors["dark_gray"])) 
        text_rect = text_surface.get_rect(center=(cx, cy + off_y))
        
        self.surface.blit(text_surface, text_rect)
        
        pygame.display.flip()
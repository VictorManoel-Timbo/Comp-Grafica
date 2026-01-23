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
        off_y = -140 # ajuste de vertical (Mudar posteriormente)
        
        b_color = tuple(self.colors["offset_black"])
        c_fill = tuple(self.colors["azure_mist"])
        d_fill = tuple(self.colors["sky_blue"])
        e_fill = tuple(self.colors["deep_ocean"])

        p_norte, p_sul = (cx, cy - 125 + off_y), (cx, cy + 125 + off_y)
        p_leste, p_oeste = (cx + 250, cy + off_y), (cx - 250, cy + off_y)
        p_ne, p_se = (cx + 165, cy - 90 + off_y), (cx + 165, cy + 90 + off_y)
        p_so, p_no = (cx - 165, cy + 90 + off_y), (cx - 165, cy - 90 + off_y)
        
        p_ponta_oso = (cx - 285, cy + 125 + off_y) 
        p_ponta_sos = (cx - 122, cy + 245 + off_y)
        p_ponta_sse = (cx + 122, cy + 245 + off_y)
        p_ponta_sel = (cx + 285, cy + 125 + off_y)
        p_culatra = (cx, cy + 400 + off_y)

        oct_pts = [p_norte, p_ne, p_leste, p_se, p_sul, p_so, p_oeste, p_no]

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

        self.boundary_fill(cx, cy + off_y, c_fill, b_color) # coroa

        self.boundary_fill(cx - 230, cy + 105 + off_y, d_fill, b_color)
        self.boundary_fill(cx - 95, cy + 155 + off_y, d_fill, b_color)
        self.boundary_fill(cx + 95, cy + 155 + off_y, d_fill, b_color)
        self.boundary_fill(cx + 230, cy + 105 + off_y, d_fill, b_color)
        self.boundary_fill(cx - 185, cy + 150 + off_y, d_fill, b_color)
        self.boundary_fill(cx, cy + 200 + off_y, d_fill, b_color)
        self.boundary_fill(cx + 185, cy + 150 + off_y, d_fill, b_color)

        self.boundary_fill(cx - 130, cy + 250 + off_y, e_fill, b_color)
        self.boundary_fill(cx, cy + 300 + off_y, e_fill, b_color)
        self.boundary_fill(cx + 130, cy + 250 + off_y, e_fill, b_color)

        pygame.font.init()
        font = pygame.font.SysFont("Arial", 36, bold=True)
        
        text_surface = font.render("PARCELADOS PICTURY", True, tuple(self.colors["dark_gray"])) 
        text_rect = text_surface.get_rect(center=(cx, cy + off_y))
        
        self.surface.blit(text_surface, text_rect)
        
        pygame.display.flip()
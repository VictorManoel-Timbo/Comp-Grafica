import pygame
import numpy as np
import math

class Primitive: 
    def __init__(self, surface):
        self.surface = surface

    def setPixel(self, x, y, color):
        if 0 <= x < self.surface.get_width() and 0 <= y < self.surface.get_height():
            self.surface.set_at((int(x), int(y)), color)

    def draw_line_bress(self, x0, y0, x1, y1, color=(255, 255, 255)):
        step = abs(y1 - y0) > abs(x1 - x0)
        if step:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = x1 - x0
        dy = y1 - y0

        ystep = 1
        if dy < 0:
            ystep = -1
            dy = -dy

        # Bresenham clássico
        d = 2 * dy - dx
        incE = 2 * dy
        incNE = 2 * (dy - dx)

        x = x0
        y = y0

        while x <= x1:
            if step:
                self.setPixel(y, x, color)
            else:
                self.setPixel(x, y, color)

            if d <= 0:
                d += incE
            else:
                d += incNE
                y += ystep

            x += 1

    def _symmetry_circle(self, xc, yc, x, y, color):
        self.setPixel(xc + x, yc - y, color) # 1 Octante
        self.setPixel(xc + y, yc - x, color) # 2 Octante
        self.setPixel(xc + y, yc + x, color) # 3 Octante
        self.setPixel(xc + x, yc + y, color) # 4 Octante

        self.setPixel(xc - x, yc + y, color) # 5 Octante
        self.setPixel(xc - y, yc + x, color) # 6 Octante
        self.setPixel(xc - y, yc - x, color) # 7 Octante
        self.setPixel(xc - x, yc - y, color) # 8 Octante

    def draw_circunference_bress(self, xc, yc, radius, color=(255, 255, 255), color_fill=None, texture=None):
        if color_fill is not None or texture is not None:
            points = []
            for i in range(0, 360, 5):
                rad = math.radians(i)
                points.append((xc + radius * math.cos(rad), yc + radius * math.sin(rad)))

            if texture:
                uvs = self._generate_uvs(points)
                self.scaline_texture(points, uvs, texture)

            elif color_fill:
                self.scanline_fill([(int(p[0]), int(p[1])) for p in points], color_fill)

        x = 0
        y = radius
        d = 1 - radius

        self._symmetry_circle(xc, yc, x, y, color)

        while (y > x):
            if (d < 0):
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x+=1
            self._symmetry_circle(xc, yc, x, y, color)

    def _ellipse_points(self, xc, yc, x, y, color):
        self.setPixel(xc + x, yc + y, color)
        self.setPixel(xc - x, yc + y, color)
        self.setPixel(xc + x, yc - y, color)
        self.setPixel(xc - x, yc - y, color)

    def draw_elipse(self, xc, yc, a, b, color=(255, 255, 255), color_fill=None, texture=None):
        if color_fill is not None or texture is not None:
            points = []
            for i in range(0, 360, 5):
                rad = math.radians(i)
                points.append((xc + a * math.cos(rad), yc + b * math.sin(rad)))
            
            if texture:
                uvs = self._generate_uvs(points)
                self.scaline_texture(points, uvs, texture)
            
            elif color_fill:
                self.scanline_fill([(int(p[0]), int(p[1])) for p in points], color_fill)

        x = 0
        y = b

        d1 = b * b - a * a * b + 0.25 * a * a
        self._ellipse_points(xc, yc, x, y, color)

        # Região 1
        while (b * b * x) <= (a * a * y):
            if d1 < 0:
                d1 += b * b * (2 * x + 3)
                x += 1
            else:
                d1 += b * b * (2 * x + 3) + a * a * (-2 * y + 2)
                x += 1
                y -= 1
            self._ellipse_points(xc, yc, x, y, color)

        # Região 2
        d2 = (b * b * (x + 0.5) * (x + 0.5) + a * a * (y - 1) * (y - 1) - a * a * b * b)

        while y > 0:
            if d2 > 0:
                d2 += a * a * (-2 * y + 3)
                y -= 1
            else:
                d2 += b * b * (2 * x + 2) + a * a * (-2 * y + 3)
                x += 1
                y -= 1
            self._ellipse_points(xc, yc, x, y, color)
    
    def draw_rectangle(self, x, y, width, height, color=(255, 255, 255), color_fill=None, texture=None):
        points = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        self.draw_polygon(points, color, color_fill, texture)

    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color=(255, 255, 255), color_fill=None, texture=None):
        points = [(x0, y0), (x1, y1), (x2, y2)]
        self.draw_polygon(points, color, color_fill, texture)

    def draw_polygon(self, points, color=(255, 255, 255), color_fill=None, uvs=None, texture=None):
        if texture is not None:
            use_uvs = uvs if uvs is not None else self._generate_uvs(points)
            self.scaline_texture(points, use_uvs, texture)

        elif color_fill is not None:
            pts_int = [(int(p[0]), int(p[1])) for p in points]
            self.scanline_fill(pts_int, color_fill)
        
        n = len(points)
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]
            self.draw_line_bress(p1[0], p1[1], p2[0], p2[1], color)

    def scanline_fill(self, points, color_fill):
        ys = [p[1] for p in points]
        y_min = min(ys)
        y_max = max(ys)

        n = len(points)

        for y in range(y_min, y_max):
            intersections_x = []

            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]

                if y0 == y1:
                    continue

                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0

                if y < y0 or y >= y1:
                    continue

                x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                intersections_x.append(x)

            intersections_x.sort()

            for i in range(0, len(intersections_x), 2):
                if i + 1 < len(intersections_x):
                    x_inicio = int(round(intersections_x[i]))
                    x_fim = int(round(intersections_x[i + 1]))

                    for x in range(x_inicio, x_fim + 1):
                        self.setPixel(x, y, color_fill)

    def scaline_texture(self, points, uvs, texture):
        tex_w, tex_h = texture.get_width(), texture.get_height()
        n = len(points)

        ys = [p[1] for p in points]
        y_min = int(min(ys))
        y_max = int(max(ys))

        for y in range(y_min, y_max):
            intersections = []

            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]

                u0, v0 = uvs[i]
                u1, v1 = uvs[(i + 1) % n]

                if y0 == y1:
                    continue

                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                    u0, v0, u1, v1 = u1, v1, u0, v0

                if y < y0 or y >= y1:
                    continue

                t = (y - y0) / (y1 - y0)

                x = x0 + t * (x1 - x0)
                u = u0 + t * (u1 - u0)
                v = v0 + t * (v1 - v0)

                intersections.append((x, u, v))

            intersections.sort(key=lambda i: i[0])

            for i in range(0, len(intersections), 2):
                if i + 1 >= len(intersections):
                    continue

                x_start, u_start, v_start = intersections[i]
                x_end, u_end, v_end   = intersections[i + 1]

                if x_start == x_end:
                    continue

                for x in range(int(x_start), int(x_end) + 1):
                    t = (x - x_start) / (x_end - x_start)

                    u = u_start + t * (u_end - u_start)
                    v = v_start + t * (v_end - v_start)

                    tx = int(u * (tex_w - 1))
                    ty = int(v * (tex_h - 1))

                    if 0 <= tx < tex_w and 0 <= ty < tex_h:
                        cor = texture.get_at((tx, ty))
                        self.setPixel(x, y, cor)
    
    def _generate_uvs(self, points):
        if not points: return []
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        
        width = x_max - x_min if x_max != x_min else 1
        height = y_max - y_min if y_max != y_min else 1
        
        return [((p[0] - x_min) / width, (p[1] - y_min) / height) for p in points]
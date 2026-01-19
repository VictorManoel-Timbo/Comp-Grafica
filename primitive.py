import pygame 
import numpy as np
import json

class Primitive: 
    def __init__(self, surface):
        self.surface = surface

    def setPixel(self, x, y, color):
        if 0 <= x < self.surface.get_width() and 0 <= y < self.surface.get_height():
            self.surface.set_at((x, y), color)

    # Função para desenhar linhas usando o algoritmo de DDA
    '''def draw_line_dda(self ,x1, y1, x2, y2, color=(255, 255, 255)):
        x, y = x1, y1
        length = (x2 - x1)

        if length <= (y2 - y1):
            length = y2 - y1

        dx = (x2 - x1)/float(length)
        dy = (y2 - y1)/float(length)
        self.surface.set_at((round(x), round(y)), color)

        for i in range(length):
            x += dx
            y += dy
            self.setPixel(round(x), round(y), color)
        pygame.display.flip()'''

    # Função para desenhar linhas usando o algoritmo de Bresenham
    def draw_line_bress(self, x0, y0, x1, y1, color=(255, 255, 255)):
        # Flags para transformações
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

    # Função para desenhar uma circunferência
    '''def draw_circunference(self, xc, yc, radius, color=(255, 255, 255)):
        pi = 3.14
        x0 = 0
        y0 = 0
        
        for i in range (360):
            self.setPixel(x0 + xc, y0 + yc, color)
            x = float((pi * i) / 180)
            x0 = round(radius * np.cos(x))
            y0 = round(radius * np.sin(x))'''

    # Função auxiliar para fazer a rasterização do círculo com base na simetria dos 8
    def _symmetry_circle(self, xc, yc, x, y, color):
        self.setPixel(xc + x, yc - y, color) # 1 Octante
        self.setPixel(xc + y, yc - x, color) # 2 Octante
        self.setPixel(xc + y, yc + x, color) # 3 Octante
        self.setPixel(xc + x, yc + y, color) # 4 Octante

        self.setPixel(xc - x, yc + y, color) # 5 Octante
        self.setPixel(xc - y, yc + x, color) # 6 Octante
        self.setPixel(xc - y, yc - x, color) # 7 Octante
        self.setPixel(xc - x, yc - y, color) # 8 Octante

    def draw_circunference_bress(self, xc, yc, radius, color=(255, 255, 255), color_fill=(0, 0, 0)):
        x = 0
        y = radius
        d = 1 - radius

        self._symmetry_circle(xc, yc, x, y, color)

        while (y > x):
            if (d < 0):
                d+=2*x + 3
            else:
                d+=2*(x-y) + 5
                y-=1
            x+=1
            self._symmetry_circle(xc, yc, x, y, color)

    def _ellipse_points(self, xc, yc, x, y, color):
        self.setPixel(xc + x, yc + y, color)
        self.setPixel(xc - x, yc + y, color)
        self.setPixel(xc + x, yc - y, color)
        self.setPixel(xc - x, yc - y, color)

    def draw_elipse(self, xc, yc, a, b, color=(255, 255, 255), color_fill=(0, 0, 0)):
        x = 0
        y = b

        d1 = b*b - a*a*b + 0.25 * a*a
        self._ellipse_points(xc, yc, x, y, color)

        # Região 1
        while (b*b * x) <= (a*a * y):
            if d1 < 0:
                d1 += b*b * (2*x + 3)
                x += 1
            else:
                d1 += b*b * (2*x + 3) + a*a * (-2*y + 2)
                x += 1
                y -= 1
            self._ellipse_points(xc, yc, x, y, color)

        # Região 2
        d2 = (
            b*b * (x + 0.5) * (x + 0.5) +
            a*a * (y - 1) * (y - 1) -
            a*a * b*b
        )

        while y > 0:
            if d2 > 0:
                d2 += a*a * (-2*y + 3)
                y -= 1
            else:
                d2 += b*b * (2*x + 2) + a*a * (-2*y + 3)
                x += 1
                y -= 1
            self._ellipse_points(xc, yc, x, y, color)
    
    def draw_rectangle(self, x, y, width, height, color=(255, 255, 255), color_fill=(0, 0, 0)):   
        # Topo
        self.draw_line_bress(x, y, x + width, y, color)
        # Direita
        self.draw_line_bress(x + width, y, x + width, y + height, color)
        # Baixo
        self.draw_line_bress(x + width, y + height, x, y + height, color)
        # Esquerda
        self.draw_line_bress(x, y + height, x, y, color)

    def draw_triangle(self, x0, y0, x1, y1, x2, y2, color=(255, 255, 255), color_fill=(0, 0, 0)):
        self.draw_line_bress(x0, y0, x1, y1, color)
        self.draw_line_bress(x1, y1, x2, y2, color)
        self.draw_line_bress(x2, y2, x0, y0, color)

    def draw_polygon(self, points, color=(255, 255, 255), color_fill=(0, 0, 0)):
        n = len(points)
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n] # O operador % garante que o último ponto ligue ao primeiro
            self.draw_line_bress(p1[0], p1[1], p2[0], p2[1], color)

    def scanline_fill(self, points, color_fill):
        # Encontra Y mínimo e máximo
        ys = [p[1] for p in points]
        y_min = min(ys)
        y_max = max(ys)

        n = len(points)

        for y in range(y_min, y_max):
            intersections_x = []

            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]

                # Ignora arestas horizontais
                if y0 == y1:
                    continue

                # Garante y0 < y1
                if y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0

                # Regra Ymin ≤ y < Ymax
                if y < y0 or y >= y1:
                    continue

                # Calcula interseção
                x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                intersections_x.append(x)

            # Ordena interseções
            intersections_x.sort()

            # Preenche entre pares
            for i in range(0, len(intersections_x), 2):
                if i + 1 < len(intersections_x):
                    x_inicio = int(round(intersections_x[i]))
                    x_fim = int(round(intersections_x[i + 1]))

                    for x in range(x_inicio, x_fim + 1):
                        self.setPixel(x, y, color_fill)

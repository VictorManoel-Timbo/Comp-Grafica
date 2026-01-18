import pygame 
import numpy as np

class Primitive: 
    def __init__(self, surface):
        self.surface = surface

    def setPixel(self, x, y, color):
        self.surface.set_at((x, y), color)

    # Função para desenhar linhas usando o algoritmo de DDA
    def draw_line_dda(self ,x1, y1, x2, y2, color=(255, 255, 255)):
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
        pygame.display.flip()

    # Função para desenhar linhas usando o algoritmo de Bresenham
    def draw_line_bress(self, x1, y1, x2, y2, color=(255, 255, 255)):
        # 1. Calculamos as distâncias absolutas e a direção do passo
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        
        x = x1
        y = y1
        self.setPixel(x, y, color)

        # 2. CASO A: Linha mais horizontal (o seu código original era este caso)
        if dx >= dy:
            d = 2 * dy - dx
            incE = 2 * dy
            incNE = 2 * (dy - dx)
            
            # Usamos != para que funcione mesmo indo para a esquerda
            while x != x2:
                if d <= 0:
                    d += incE
                else:
                    d += incNE
                    y += sy # Incrementa o Y na direção correta
                x += sx     # Incrementa o X na direção correta
                self.setPixel(x, y, color)

        # 3. CASO B: Linha mais vertical (resolve o problema das linhas verticais)
        else:
            d = 2 * dx - dy
            incE = 2 * dx
            incNE = 2 * (dx - dy)
            
            while y != y2:
                if d <= 0:
                    d += incE
                else:
                    d += incNE
                    x += sx # Incrementa o X na direção correta
                y += sy     # Incrementa o Y na direção correta
                self.setPixel(x, y, color)

    # Função para desenhar uma circunferência
    def draw_circunference(self, xc, yc, radius, color=(255, 255, 255)):
        pi = 3.14
        x1 = 0
        y1 = 0
        
        for i in range (360):
            self.setPixel(x1 + xc, y1 + yc, color)
            x = float((pi * i) / 180)
            x1 = round(radius * np.cos(x))
            y1 = round(radius * np.sin(x))

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

    def draw_circunference_bress(self, xc, yc, raio, color=(255, 255, 255)):
        x = 0
        y = raio
        d = 1 - raio

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

    def draw_elipse(self, xc, yc, a, b, color=(255, 255, 255)):
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
    
    def draw_rectangle(self, x, y, width, height, color=(255, 255, 255)):
        """Desenha um retângulo (ou quadrado) conectando 4 pontos."""
        # Topo
        self.draw_line_bress(x, y, x + width, y, color)
        # Direita
        self.draw_line_bress(x + width, y, x + width, y + height, color)
        # Baixo
        self.draw_line_bress(x + width, y + height, x, y + height, color)
        # Esquerda
        self.draw_line_bress(x, y + height, x, y, color)

    def draw_triangle(self, x1, y1, x2, y2, x3, y3, color=(255, 255, 255)):
        """Desenha um triângulo conectando os 3 vértices."""
        self.draw_line_bress(x1, y1, x2, y2, color)
        self.draw_line_bress(x2, y2, x3, y3, color)
        self.draw_line_bress(x3, y3, x1, y1, color)

    def draw_polygon(self, points, color=(255, 255, 255)):
        """Desenha polígonos genéricos como o Hexágono."""
        n = len(points)
        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n] # O operador % garante que o último ponto ligue ao primeiro
            self.draw_line_bress(p1[0], p1[1], p2[0], p2[1], color)
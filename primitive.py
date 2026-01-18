import pygame 
import numpy as np

class Primitive: 
    def __init__(self, surface):
        self.surface = surface

    def setPixel(self, x, y, color):
        self.surface.set_at((x, y), color)

    # Função para desenhar linhas usando o algoritmo de DDA
    def draw_line_dda(self ,x1, y1, x2, y2):
        x, y = x1, y1
        length = (x2 - x1)

        if length <= (y2 - y1):
            length = y2 - y1

        dx = (x2 - x1)/float(length)
        dy = (y2 - y1)/float(length)
        self.surface.set_at((round(x), round(y)), (255 ,255, 255))

        for i in range(length):
            x += dx
            y += dy
            self.setPixel(round(x), round(y), (255 ,255, 255))
        pygame.display.flip()

    # Função para desenhar linhas usando o algoritmo de Bresenham
    def draw_line_bress(self, x1, y1, x2, y2):
        self.setPixel(x1, y1, (255, 255, 255))

        dx = x2 - x1
        dy = y2 - y1
        d = 2 * dy - dx
        incE = 2*dy
        incNE = 2 * (dy - dx)
        
        x = x1
        y = y1
        
        self.setPixel(x, y, (255, 255, 255))
        while x < x2:
            if(d <= 0):
                d += incE
                x+=1
            else:
                d += incNE
                x += 1
                y += 1
            self.setPixel(x, y, (255, 255, 255))

    # Função para desenhar uma circunferência
    def draw_circunference(self, xc, yc, radius, color):
        pi = 3.14
        x1 = 0
        y1 = 0
        
        for i in range (360):
            self.setPixel(x1 + xc, y1 + yc, (255, 255, 255))
            x = float((pi * i) / 180)
            x1 = round(radius * np.cos(x))
            y1 = round(radius * np.sin(x))

    # Função auxiliar para fazer a rasterização do círculo com base na simetria dos 8
    def symmetryCircle(self, xc, yc, x, y, cor):
        self.setPixel(xc + x, yc - y, cor) # 1 Octante
        self.setPixel(xc + y, yc - x, cor) # 2 Octante
        self.setPixel(xc + y, yc + x, cor) # 3 Octante
        self.setPixel(xc + x, yc + y, cor) # 4 Octante

        self.setPixel(xc - x, yc + y, cor) # 5 Octante
        self.setPixel(xc - y, yc + x, cor) # 6 Octante
        self.setPixel(xc - y, yc - x, cor) # 7 Octante
        self.setPixel(xc - x, yc - y, cor) # 8 Octante

    def draw_circunference_bress(self, xc, yc, raio, color):
        x = 0
        y = raio
        d = 1 - raio

        self.symmetryCircle(xc, yc, x, y, color)

        while (y > x):
            if (d < 0):
                d+=2*x + 3
            else:
                d+=2*(x-y) + 5
                y-=1
            x+=1
            self.symmetryCircle(xc, yc, x, y, color)

    def ellipsePoints(self, xc, yc, x, y, color):
        self.setPixel(xc + x, yc + y, color)
        self.setPixel(xc - x, yc + y, color)
        self.setPixel(xc + x, yc - y, color)
        self.setPixel(xc - x, yc - y, color)

    def draw_elipse(self, xc, yc, a, b, color):
        x = 0
        y = b

        d1 = b*b - a*a*b + 0.25 * a*a
        self.ellipsePoints(xc, yc, x, y, color)

        # Região 1
        while (b*b * x) <= (a*a * y):
            if d1 < 0:
                d1 += b*b * (2*x + 3)
                x += 1
            else:
                d1 += b*b * (2*x + 3) + a*a * (-2*y + 2)
                x += 1
                y -= 1
            self.ellipsePoints(xc, yc, x, y, color)

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
            self.ellipsePoints(xc, yc, x, y, color)
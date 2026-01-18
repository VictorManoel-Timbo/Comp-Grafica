import pygame 
import sys
import numpy as np

pygame.init()
largura, altura = 400, 300
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Set Pixel")

# Função SetPixel
def setPixel(superficie, x, y, cor):
    superficie.set_at((x, y), cor)

# Função para desenhar linhas usando o algoritmo de DDA
def draw_line_dda(x1, y1, x2, y2):
    x, y = x1, y1
    length = (x2 - x1)

    if length <= (y2 - y1):
        length = y2 - y1

    dx = (x2 - x1)/float(length)
    dy = (y2 - y1)/float(length)
    tela.set_at((round(x), round(y)), (255 ,255, 255))

    for i in range(length):
        x += dx
        y += dy
        setPixel(tela, round(x), round(y), (255 ,255, 255))
    pygame.display.flip()

# Função para desenhar linhas usando o algoritmo de Bresenham
def draw_line_bress(x1, y1, x2, y2):
    setPixel(tela, x1, y1, (255, 255, 255))

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2*dy
    incNE = 2 * (dy - dx)
    
    x = x1
    y = y1
    
    setPixel(tela, x, y, (255, 255, 255))
    while x < x2:
        if(d <= 0):
            d += incE
            x+=1
        else:
            d += incNE
            x += 1
            y += 1
        setPixel(tela, x, y, (255, 255, 255))

# Função para desenhar uma circunferência
def draw_circunference(xc, yc, raio, cor):
    pi = 3.14
    x1 = 0
    y1 = 0
    
    for i in range (360):
        setPixel(tela, x1 + xc, y1 + yc, (255, 255, 255))
        x = float((pi * i) / 180)
        x1 = round(raio * np.cos(x))
        y1 = round(raio * np.sin(x))

# Função auxiliar para fazer a rasterização do círculo com base na simetria dos 8
def SimetriaCirculo(xc, yc, x, y, cor):
    setPixel(tela, xc + x, yc - y, cor) # 1 Octante
    setPixel(tela, xc + y, yc - x, cor) # 2 Octante
    setPixel(tela, xc + y, yc + x, cor) # 3 Octante
    setPixel(tela, xc + x, yc + y, cor) # 4 Octante

    setPixel(tela, xc - x, yc + y, cor) # 5 Octante
    setPixel(tela, xc - y, yc + x, cor) # 6 Octante
    setPixel(tela, xc - y, yc - x, cor) # 7 Octante
    setPixel(tela, xc - x, yc - y, cor) # 8 Octante

def draw_circunference_bress(xc, yc, raio, cor):
    x = 0
    y = raio
    d = 1 - raio

    SimetriaCirculo(xc, yc, x, y, cor)

    while (y > x):
        if (d < 0):
            d+=2*x + 3
        else:
            d+=2*(x-y) + 5
            y-=1
        x+=1
        SimetriaCirculo(xc, yc, x, y, cor)

def pontosElipse(xc, yc, x, y, cor):
    setPixel(tela, xc + x, yc + y, cor)
    setPixel(tela, xc - x, yc + y, cor)
    setPixel(tela, xc + x, yc - y, cor)
    setPixel(tela, xc - x, yc - y, cor)

def draw_elipse(xc, yc, a, b, cor):
    x = 0
    y = b

    d1 = b*b - a*a*b + 0.25 * a*a
    pontosElipse(xc, yc, x, y, cor)

    # Região 1
    while (b*b * x) <= (a*a * y):
        if d1 < 0:
            d1 += b*b * (2*x + 3)
            x += 1
        else:
            d1 += b*b * (2*x + 3) + a*a * (-2*y + 2)
            x += 1
            y -= 1
        pontosElipse(xc, yc, x, y, cor)

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
        pontosElipse(xc, yc, x, y, cor)

# Código para testar as funções primitivas
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
    tela.fill((0, 0, 0))
    setPixel(tela, 200, 150, (255, 255, 255))
    draw_line_bress(150, 200, 200, 250)
    draw_circunference_bress(200, 150, 50, (255, 255, 255))
    draw_elipse(200, 150, 90, 60, (255, 255, 255))
    pygame.display.flip()

pygame.quit()
sys.exit()
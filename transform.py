import math

def identidade():
    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

def translacao(tx, ty):
    return [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ]

def escala(sx, sy):
    return [
        [sx, 0, 0],
        [0, sy, 0],
        [0, 0, 1]
    ]

def rotacao(theta):
    c = math.cos(theta)
    s = math.sin(theta)
    return [
        [ c, -s, 0],
        [ s,  c, 0],
        [ 0,  0, 1]
    ]

def multiplica_matrizes(a, b):
    r = [[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                r[i][j] += a[i][k] * b[k][j]
    return r

# =====================================================
# COMPOSIÇÃO DE TRANSFORMAÇÕES
# =====================================================
def cria_transformacao():
    return identidade()

def aplica_transformacao(m, pontos):
    novos = []
    for x, y in pontos:
        v = [x, y, 1]
        x_novo = round(m[0][0]*v[0] + m[0][1]*v[1] + m[0][2])
        y_novo = round(m[1][0]*v[0] + m[1][1]*v[1] + m[1][2])
        novos.append((x_novo, y_novo))
    return novos

def janela_viewport(janela, viewport):
    # janela e viewport: (x_min, y_min, x_max, y_max)
    x_min_j, y_min_j, x_max_j, y_max_j = janela
    x_min_v, y_min_v, x_max_v, y_max_v = viewport

    # Escalas
    sx = (x_max_v - x_min_v) / (x_max_j - x_min_j)
    sy = (y_max_v - y_min_v) / (y_max_j - y_min_j)

    # Matriz composta: Translacao para origem -> Escala -> Translacao para Viewport
    # Simplificando a composição:
    m = identidade()
    m = multiplica_matrizes(translacao(-x_min_j, -y_min_j), m)
    m = multiplica_matrizes(escala(sx, sy), m)
    m = multiplica_matrizes(translacao(x_min_v, x_min_v), m)
    
    return m

# Cohen–Sutherland (recorte de linhas)

INSIDE = 0
LEFT   = 1
RIGHT  = 2
BOTTOM = 4
TOP    = 8

def codigo_regiao(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin: code |= LEFT
    elif x > xmax: code |= RIGHT
    if y < ymin: code |= TOP      # Lógica de tela: y cresce para baixo
    elif y > ymax: code |= BOTTOM
    return code

def cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
    c0 = codigo_regiao(x0, y0, xmin, ymin, xmax, ymax)
    c1 = codigo_regiao(x1, y1, xmin, ymin, xmax, ymax)

    while True:
        if not (c0 | c1):
            return True, x0, y0, x1, y1
        if c0 & c1:
            return False, None, None, None, None

        c_out = c0 if c0 else c1

        if c_out & TOP:
            x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
            y = ymin
        elif c_out & BOTTOM:
            x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
            y = ymax
        elif c_out & RIGHT:
            y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
            x = xmax
        elif c_out & LEFT:
            y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
            x = xmin

        if c_out == c0:
            x0, y0 = x, y
            c0 = codigo_regiao(x0, y0, xmin, ymin, xmax, ymax)
        else:
            x1, y1 = x, y
            c1 = codigo_regiao(x1, y1, xmin, ymin, xmax, ymax)
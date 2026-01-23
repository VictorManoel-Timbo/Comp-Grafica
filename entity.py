import random
import transform

class Entity:
    def __init__(self, entity_type, x, y, colors):
        self.type = entity_type
        self.x = x
        self.y = y
        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(-3, 3)
        self.angle = 0.0
        self.timer = random.randint(30, 90)
        
        self.colors = colors
        self.color = self._set_color()
        self.model = self._set_model()

    def _set_color(self):
        if self.type == "scissors": return self.colors["red"]
        if self.type == "paper": return self.colors["white"]
        return self.colors["medium_gray"] 

    def _set_model(self):
        models = {
            "scissors": [(0, -20), (20, 20), (-20, 20)],
            "paper": [(-20, -20), (20, -20), (20, 20), (-20, 20)],
            "stone": [(10, -17), (20, 0), (10, 17), (-10, 17), (-20, 0), (-10, -17)]
        }
        return models[self.type]

    def update(self, width, height):
        # Movimentação e Rotação
        self.x += self.dx
        self.y += self.dy
        self.angle += 0.05

        # Rebater nas bordas
        if self.x < 50 or self.x > width - 50:
            self.dx *= -1
        if self.y < 50 or self.y > height - 50:
            self.dy *= -1

        # Mudar direção aleatoriamente
        self.timer -= 1
        if self.timer <= 0:
            self.dx = random.uniform(-3, 3)
            self.dy = random.uniform(-3, 3)
            self.timer = random.randint(60, 180)

    def draw(self, drawer, m_viewport=None):
        # 1. Matriz de transformação do objeto (Mundo)
        m = transform.cria_transformacao()
        m = transform.multiplica_matrizes(transform.rotacao(self.angle), m)
        m = transform.multiplica_matrizes(transform.translacao(self.x, self.y), m)
        
        # 2. Aplicar transformação para o espaço do mundo
        pts_trans = transform.aplica_transformacao(m, self.model)
        pts_int = [(int(p[0]), int(p[1])) for p in pts_trans]
        
        # 3. Desenhar na tela principal
        #drawer.scanline_fill(pts_int, self.color)
        drawer.draw_polygon(pts_trans, self.colors["black"], self.color)

        # 4. Desenhar no minimapa (se a matriz de viewport for fornecida)
        if m_viewport is not None:
            pts_mini = transform.aplica_transformacao(m_viewport, pts_trans)
            pts_mini_int = [(int(p[0]), int(p[1])) for p in pts_mini]
            drawer.scanline_fill(pts_mini_int, self.color)
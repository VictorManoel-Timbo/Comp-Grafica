import random
import transform
import math

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
        self.radius = 20  # para cálculo de colisão

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

    def _check_collision(self, other):
        """Verifica se há colisão entre duas entidades"""
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx**2 + dy**2)
        return distance < (self.radius + other.radius)

    def _resolve_collision(self, other):
        """Resolve a colisão aplicando as regras do jogo"""
        rules = {
            "stone": {"scissors": True, "paper": False},
            "paper": {"stone": True, "scissors": False},
            "scissors": {"paper": True, "stone": False}
        }
        
        # Verifica se a entidade atual vence
        if rules[self.type].get(other.type, False):
            # self vence, other se transforma
            other.type = self.type
            other.color = self._get_color_for_type(self.type, other.colors)
            other.model = self._get_model_for_type(self.type)
        else:
            # other vence, self se transforma
            self.type = other.type
            self.color = self._get_color_for_type(other.type, self.colors)
            self.model = self._get_model_for_type(other.type)

    def _get_color_for_type(self, entity_type, colors):
        """Retorna a cor baseada no tipo"""
        if entity_type == "scissors": return colors["red"]
        if entity_type == "paper": return colors["white"]
        return colors["medium_gray"]

    def _get_model_for_type(self, entity_type):
        """Retorna o modelo baseado no tipo"""
        models = {
            "scissors": [(0, -20), (20, 20), (-20, 20)],
            "paper": [(-20, -20), (20, -20), (20, 20), (-20, 20)],
            "stone": [(10, -17), (20, 0), (10, 17), (-10, 17), (-20, 0), (-10, -17)]
        }
        return models[entity_type]

    def update(self, width, height, entities=None):
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

        # Verificar colisões com outras entidades
        if entities is not None:
            for other in entities:
                if other is not self and self._check_collision(other):
                    self._resolve_collision(other)

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
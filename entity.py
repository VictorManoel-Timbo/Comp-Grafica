import random
from transform import Transform
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
        self.paper = [(-20, -20), (20, -20), (20, 20), (-20, 20)]
        self.scissors = [(-1, 5), (-10, 5), (-10, 15),(-1,20),(-10,20),(-10,40),(0,20),(10,40),(10,20),(1,20),(10,15),(10,5),(1,5),(0,20)]
        self.stone = [(10, -17), (20, 0), (10, 17), (-10, 17), (-20, 0), (-10, -17)]
        
        self.colors = colors
        self.color = self._set_color()
        self.model = self._set_model()
        self.hitbox_size = 25  # hitbox quadrada 20x20

    def _set_color(self):
        if self.type == "scissors": return self.colors["red"]
        if self.type == "paper": return self.colors["white"]
        return self.colors["medium_gray"] 

    def _set_model(self):
        models = {
            "scissors": self.scissors,
            "paper": self.paper,
            "stone": self.stone
        }
        return models[self.type]

    def _check_collision(self, other):
        # Hitbox como quadrado centrado na posição da entidade
        half_size = self.hitbox_size / 2
        
        self_left = self.x - half_size
        self_right = self.x + half_size
        self_top = self.y - half_size
        self_bottom = self.y + half_size
        
        other_left = other.x - half_size
        other_right = other.x + half_size
        other_top = other.y - half_size
        other_bottom = other.y + half_size
        
        # Colisão AABB (Axis-Aligned Bounding Box)
        return (self_left < other_right and self_right > other_left and
                self_top < other_bottom and self_bottom > other_top)

    def _resolve_collision(self, other):
        rules = {
            "stone": {"scissors": True, "paper": False},
            "paper": {"stone": True, "scissors": False},
            "scissors": {"paper": True, "stone": False}
        }
        
        # Verifica se a entidade atual vence
        if rules[self.type].get(other.type, False):
            other.type = self.type
            other.color = self._get_color_for_type(self.type, other.colors)
            other.model = self._get_model_for_type(self.type)
            self_dx = self.dx
            self_dy = self.dy
            other_dx = other.dx
            other_dy = other.dy
            self.dx = other_dy
            self.dy = other_dx
            other.dx = self_dy
            other.dy = self_dx

    def _get_color_for_type(self, entity_type, colors):
        if entity_type == "scissors": return colors["red"]
        if entity_type == "paper": return colors["white"]
        return colors["medium_gray"]

    def _get_model_for_type(self, entity_type):
        models = {
            "scissors": self.scissors,
            "paper": self.paper,
            "stone": self.stone
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
        m = Transform.create_transformation()
        m = Transform.multiply_matrices(Transform.rotation(self.angle), m)
        m = Transform.multiply_matrices(Transform.translation(self.x, self.y), m)
        
        pts_trans = Transform.apply_transformation(m, self.model)
        
        drawer.draw_polygon(pts_trans, self.colors["black"], self.color)

        if m_viewport is not None:
            pts_mini = Transform.apply_transformation(m_viewport, pts_trans)
            pts_mini_int = [(int(p[0]), int(p[1])) for p in pts_mini]
            drawer.scanline_fill(pts_mini_int, self.color)
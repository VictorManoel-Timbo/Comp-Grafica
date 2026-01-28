import math

class Transform:
    INSIDE = 0
    LEFT   = 1
    RIGHT  = 2
    BOTTOM = 4
    TOP    = 8

    @staticmethod
    def identity():
        return [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]

    @staticmethod
    def translation(tx, ty):
        return [
            [1, 0, tx],
            [0, 1, ty],
            [0, 0, 1]
        ]

    @staticmethod
    def scale(sx, sy):
        return [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ]

    @staticmethod
    def rotation(theta):
        c = math.cos(theta)
        s = math.sin(theta)
        return [
            [ c, -s, 0],
            [ s,  c, 0],
            [ 0,  0, 1]
        ]

    @staticmethod
    def multiply_matrices(a, b):
        r = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    r[i][j] += a[i][k] * b[k][j]
        return r

    @staticmethod
    def create_transformation():
        return Transform.identity()

    @staticmethod
    def apply_transformation(m, points):
        news = []
        for x, y in points:
            v = [x, y, 1]
            x_new = round(m[0][0]*v[0] + m[0][1]*v[1] + m[0][2])
            y_new = round(m[1][0]*v[0] + m[1][1]*v[1] + m[1][2])
            news.append((x_new, y_new))
        return news

    @staticmethod
    def window_viewport(window, viewport):
        x_min_j, y_min_j, x_max_j, y_max_j = window
        x_min_v, y_min_v, x_max_v, y_max_v = viewport

        sx = (x_max_v - x_min_v) / (x_max_j - x_min_j)
        sy = (y_max_v - y_min_v) / (y_max_j - y_min_j)

        m = Transform.identity()
        m = Transform.multiply_matrices(Transform.translation(-x_min_j, -y_min_j), m)
        m = Transform.multiply_matrices(Transform.scale(sx, sy), m)
        m = Transform.multiply_matrices(Transform.translation(x_min_v, y_min_v), m)
        
        return m

    @staticmethod
    def _region_code(x, y, xmin, ymin, xmax, ymax):
        code = Transform.INSIDE
        if x < xmin: code |= Transform.LEFT
        elif x > xmax: code |= Transform.RIGHT
        if y < ymin: code |= Transform.TOP
        elif y > ymax: code |= Transform.BOTTOM
        return code

    @staticmethod
    def cohen_sutherland(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
        c0 = Transform._region_code(x0, y0, xmin, ymin, xmax, ymax)
        c1 = Transform._region_code(x1, y1, xmin, ymin, xmax, ymax)

        while True:
            if not (c0 | c1): return True, x0, y0, x1, y1
            if c0 & c1: return False, None, None, None, None

            c_out = c0 if c0 else c1

            if c_out & Transform.TOP:
                x = x0 + (x1 - x0) * (ymin - y0) / (y1 - y0)
                y = ymin
            elif c_out & Transform.BOTTOM:
                x = x0 + (x1 - x0) * (ymax - y0) / (y1 - y0)
                y = ymax
            elif c_out & Transform.RIGHT:
                y = y0 + (y1 - y0) * (xmax - x0) / (x1 - x0)
                x = xmax
            elif c_out & Transform.LEFT:
                y = y0 + (y1 - y0) * (xmin - x0) / (x1 - x0)
                x = xmin

            if c_out == c0:
                x0, y0 = x, y
                c0 = Transform._region_code(x0, y0, xmin, ymin, xmax, ymax)
            else:
                x1, y1 = x, y
                c1 = Transform._region_code(x1, y1, xmin, ymin, xmax, ymax)

    @staticmethod
    def sutherland_hodgman(points, xmin, ymin, xmax, ymax):
        def clip_edge(pts, edge_type, limit):
            new_pts = []
            for i in range(len(pts)):
                p1 = pts[i]
                p2 = pts[(i + 1) % len(pts)]
                
                # Determina se os pontos estão "dentro" da borda
                if edge_type == 0:   inside1, inside2 = p1[0] >= limit, p2[0] >= limit # Esquerda
                elif edge_type == 1: inside1, inside2 = p1[0] <= limit, p2[0] <= limit # Direita
                elif edge_type == 2: inside1, inside2 = p1[1] >= limit, p2[1] >= limit # Topo
                else:                inside1, inside2 = p1[1] <= limit, p2[1] <= limit # Fundo

                if inside1 and inside2:
                    new_pts.append(p2)
                elif inside1 and not inside2:
                    new_pts.append(Transform._get_intersect(p1, p2, edge_type, limit))
                elif not inside1 and inside2:
                    new_pts.append(Transform._get_intersect(p1, p2, edge_type, limit))
                    new_pts.append(p2)
            return new_pts

        result = points
        if not result: return []
        
        # Aplica o recorte sequencialmente nas 4 bordas
        result = clip_edge(result, 0, xmin)
        result = clip_edge(result, 1, xmax)
        result = clip_edge(result, 2, ymin)
        result = clip_edge(result, 3, ymax)
        return result

    @staticmethod
    def _get_intersect(p1, p2, edge_type, limit):
        # Calcula a intersecção e interpola atributos extras (UVs)
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        dx, dy = x2 - x1, y2 - y1
        
        if edge_type < 2: # Vertical (Esquerda/Direita)
            x = limit
            t = (limit - x1) / dx if dx != 0 else 0
            y = y1 + t * dy
        else: # Horizontal (Topo/Fundo)
            y = limit
            t = (limit - y1) / dy if dy != 0 else 0
            x = x1 + t * dx
            
        # Interpola dado associado ao vértice
        res = [x, y]
        for i in range(2, len(p1)):
            res.append(p1[i] + t * (p2[i] - p1[i]))
            
        return tuple(res)
import math

def bhaskara(a, b, c):
    delta = b ** 2 - 4 * a * c

    if delta < 0:
        return

    delta = math.sqrt(delta)
    xi = (-b + delta) / (2 * a)
    xii = (-b - delta) / (2 * a)

    return (xi, xii)

def intersect_circles(b, c, a, r):
    bx, by = b
    cx, cy = c

    coef = (cy - by) / (- (cx - bx))
    cte = (- (cx ** 2) - (cy ** 2) + bx ** 2 + by ** 2 + (r ** 2) - (a ** 2)) / (-2 * cx + 2 * bx)

    bhaskara_a = coef ** 2 + 1
    bhaskara_b = 2 * coef * cte - 2 * coef * cx - 2 * cy
    bhaskara_c = cte ** 2 - 2 * cte * cx + cx ** 2 + cy ** 2 - r ** 2

    yi, yii = bhaskara(bhaskara_a, bhaskara_b, bhaskara_c)

    xi = yi * coef + cte
    xii = yii * coef + cte

    return ((xi, yi), (xii, yii))

def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def nearest_points(points1, points2):
    if len(points1) != 2 or len(points2) != 2:
        return

    nearest = None
    distance = None

    for p1 in points1:
        for p2 in points2:
            d = euclidean_distance(p1, p2)
            if not distance or d < distance:
                distance = d
                nearest = (p1, p2)

    return nearest


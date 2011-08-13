import math


def bhaskara(a, b, c):
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        return
    delta = math.sqrt(delta)
    xi = (-b + delta) / (2 * a)
    xii = (-b - delta) / (2 * a)
    return (xi, xii)

def intersect_circles(center1, center2, radius1, radius2):
    bx, by = center1
    cx, cy = center2
    coef = (cy - by) / (- (cx - bx))
    cte = (- (cx ** 2) - (cy ** 2) + bx ** 2 + by ** 2 + (radius2 ** 2) - (radius1 ** 2))
    cte /= (-2 * cx + 2 * bx)
    bhaskara_a = coef ** 2 + 1
    bhaskara_b = 2 * coef * cte - 2 * coef * cx - 2 * cy
    bhaskara_c = cte ** 2 - 2 * cte * cx + cx ** 2 + cy ** 2 - radius2 ** 2
    yy = bhaskara(bhaskara_a, bhaskara_b, bhaskara_c)
    if yy == None:
        return None
    yi, yii = yy
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

def straight_intersection(straight1, straight2):
    p1x = straight1[0][0]
    p1y = straight1[0][1]
    p2x = straight1[1][0]
    p2y = straight1[1][1]
    p3x = straight2[0][0]
    p3y = straight2[0][1]
    p4x = straight2[1][0]
    p4y = straight2[1][1]
    x = p1y * p2x * p3x - p1y * p2x * p4x - p1x * p2y * p4x + p1x * p2y * p3x - p2x * p3x * p4y + p2x * p3y * p4x + p1x * p3x * p4y - p1x * p3y * p4x
    x = x / (p2x * p3y - p2x * p4y - p1x * p3y + p1x * p4y + p4x * p2y - p4x * p1y - p3x * p2y + p3x * p1y)
    y = ((p2y - p1y) * x + p1y * p2x - p1x * p2y) / (p2x - p1x)
    return (x, y)

def get_edge_line(edge, alpha):
    x1, y1 = edge.start.position[0], edge.start.position[1]
    x2, y2 = edge.end.position[0], edge.end.position[1]
    angle = math.atan2(y2 - y1, x2 - x1) + math.pi
    radius1 = (edge.start.border_size + edge.start.size) / 2
    radius2 = (edge.end.border_size + edge.end.size) / 2
    point_out1_x = x1 - radius1 * math.cos(angle + alpha)
    point_out1_y = y1 - radius1 * math.sin(angle + alpha)
    point_out2_x = x2 + radius2 * math.cos(angle - alpha)
    point_out2_y = y2 + radius2 * math.sin(angle - alpha)
    if alpha != 0:
        distance = euclidean_distance((x1, y1), (x2, y2)) / 4
        point_out3_x = x1 - (distance + radius1) * math.cos(angle + alpha)
        point_out3_y = y1 - (distance + radius1) * math.sin(angle + alpha)
        point_out4_x = x2 + (distance + radius2) * math.cos(angle - alpha)
        point_out4_y = y2 + (distance + radius2) * math.sin(angle - alpha)
        return (point_out1_x, point_out1_y, point_out2_x, point_out2_y, point_out3_x, point_out3_y, point_out4_x, point_out4_y)
    return (point_out1_x, point_out1_y, point_out2_x, point_out2_y)

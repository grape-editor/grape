from gtk import DrawingArea, EventBox
from app.helpers.graph_helper import *
from app.models.edge import Edge
import gtk
import math

class GraphArea(DrawingArea):

    def __init__(self, graph):
        DrawingArea.__init__(self)

        self.connect('expose-event', self.expose)

        self.graph = graph
        self.cairo = None
        self.path = None
        self.adding_edge = None

        self.set_double_buffered(True)

    def draw_vertex(self, cairo, area, vertex):
        import math

        x = vertex.position[0]
        y = vertex.position[1]

        radius = vertex.size / 2

        # TODO - Custom colors

        if vertex.selected:
            cairo.set_source_rgb(0.4, 0.8, 0.2)
        else:
            cairo.set_source_rgb(vertex.color[0], vertex.color[1], vertex.color[2])

        cairo.arc(x, y, radius, 0, 2 * math.pi)
        cairo.fill_preserve()
        cairo.stroke()

    def draw_arrow(self, cairo, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        arrow_lenght = 10
        arrow_degrees = 0.25

        angle = math.atan2(y2 - y1, x2 - x1) + math.pi

        arrow_x1 = x2 + arrow_lenght * math.cos(angle - arrow_degrees)
        arrow_y1 = y2 + arrow_lenght * math.sin(angle - arrow_degrees)
        arrow_x2 = x2 + arrow_lenght * math.cos(angle + arrow_degrees)
        arrow_y2 = y2 + arrow_lenght * math.sin(angle + arrow_degrees)

        cairo.move_to(x2, y2)
        cairo.line_to(arrow_x1, arrow_y1)
        cairo.stroke()

        cairo.move_to(x2, y2)
        cairo.line_to(arrow_x2, arrow_y2)
        cairo.stroke()

    def draw_edges(self, cairo, area, vertex1, vertex2, touching=None):
        edges = []

        if not touching:
            touching = vertex1.touching_edges

        for edge in touching:
            if edge.touches(vertex2):
                edges.append(edge)
                edge.visited = True

        if len(edges) == 0:
            return

        x1, y1 = edges[0].start.position
        x2, y2 = edges[0].end.position
        mx, my = ((x1 + x2) / 2, (y1 + y2) / 2)
        distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        angular_coeficient = x2 - x1

        if y1 != y2:
            angular_coeficient = (x2 - x1) / (y1 - y2)

        distance_arc = math.atan(angular_coeficient)
        constant = my - mx * angular_coeficient

        alpha = 0
        step = 16 * math.pi / (32 + distance)
        bhaskara_a = angular_coeficient ** 2 + 1
        bhaskara_b = (2 * angular_coeficient * constant) - (2 * mx) - (2 * angular_coeficient * my)
        bhaskara_c = (mx ** 2) - (2 * constant * my) + (my ** 2) + (constant ** 2)

        stack = list(edges)

        while len(stack) > 1:
            alpha += step

            radius = (distance / 2) / math.sin(alpha)
            adjacent = math.cos(alpha) * radius

            roots = bhaskara(bhaskara_a, bhaskara_b, bhaskara_c - (adjacent ** 2))

            angle = distance_arc + math.pi

            for i in range(2):
                edge = stack.pop()
                x = roots[i]
                y = angular_coeficient * x + constant

                points1 = intersect_circles((x, y), vertex1.position, radius, vertex1.size / 2)
                points2 = intersect_circles((x, y), vertex2.position, radius, vertex2.size / 2)
                points = nearest_points(points1, points2)

                opposite = euclidean_distance(points[0], points[1]) / 2
                beta = math.asin(opposite / radius) * 2
                offset = beta / 2

                cairo.set_source_rgb(edge.color[0], edge.color[1], edge.color[2])
                cairo.set_line_width(edge.width)

                cairo.arc(x, y, radius, angle - offset, angle + offset)
                cairo.stroke()

                if not edge.bidirectional:
                    point = points[0]
                    v = vertex1

                    if edge.start == vertex1:
                        point = points[1]
                        v = vertex2

                    x1 = point[0] ** 2 / v.position[0]
                    y1 = point[1] ** 2 / v.position[1]
                    self.draw_arrow(cairo, (x1, y1), point)

                angle -= math.pi

        if len(stack) == 1:
            edge = stack.pop()
            self.draw_edge_straight(cairo, edge)

    def draw_edge_straight(self, cairo, edge):
        x1, y1 = edge.start.position[0], edge.start.position[1]
        x2, y2 = edge.end.position[0], edge.end.position[1]

        angle = math.atan2(y2 - y1, x2 - x1) + math.pi
        radius = edge.end.size / 2s

        cairo.set_source_rgb(edge.color[0], edge.color[1], edge.color[2])
        cairo.set_line_width(edge.width)

        cairo.move_to(x1, y1)
        cairo.line_to(x2, y2)
        cairo.stroke()

        if not edge.bidirectional:
            self.draw_arrow(cairo, (x1, y1), (x2, y2))

    def draw_graph(self, cairo, area):
        for edge in self.graph.edges:
            edge.visited = False

        for vertex in self.graph.vertices:
            self.draw_vertex(cairo, area, vertex)

            vertex.visited = True
            touching = list(vertex.touching_edges)

            if self.adding_edge:
                end = self.graph.find_by_position(self.adding_edge[1])

                if end == vertex:
                    start = self.graph.find_by_position(self.adding_edge[0])
                    edge = Edge(-1, start, end, not self.graph.directed, False)
                    edge.color = [0.7, 0.7, 0.7]
                    edge.visited = False

                    touching.append(edge)

                    self.adding_edge = None

            for edge in touching:
                if not edge.visited:
                    self.draw_edges(cairo, area, edge.start, edge.end, touching)

        for vertex in self.graph.vertices:
            vertex.visited = None

        for edge in self.graph.edges:
            edge.visited = None

        if self.adding_edge:
            cairo.set_source_rgb(0.7, 0.7, 0.7)
            cairo.set_line_width(1)

            cairo.move_to(self.adding_edge[0][0], self.adding_edge[0][1])
            cairo.line_to(self.adding_edge[1][0], self.adding_edge[1][1])
            cairo.stroke()

            self.adding_edge = None

    def create_area(self, widget, event):
        self.area = widget.get_allocation()

        self.cairo = widget.window.cairo_create()

        self.cairo.rectangle(0, 0, self.area.width, self.area.height)
        self.cairo.clip()

    def expose(self, widget, event):
        self.create_area(widget, event)
        self.cairo.rectangle(0, 0, self.area.width, self.area.height)
        self.cairo.set_source_rgb(1, 1, 1)
        self.cairo.fill()

        self.draw_graph(self.cairo, self.area)

    def draw(self):
        self.cairo.save()
        self.queue_draw_area(0, 0, self.area.width, self.area.height)
        self.cairo.restore()


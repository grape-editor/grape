from gtk import DrawingArea, EventBox
from app.helpers.graph_helper import *
from app.models.edge import Edge
import gtk
import math


class GraphArea(DrawingArea):

    def __init__(self, graph, controller):
        DrawingArea.__init__(self)

        self.connect('expose-event', self.expose)

        self.graph = graph
        self.controller = controller
        self.cairo = None
        self.path = None
        self.adding_edge = None
        self.scale = 1

        self.set_double_buffered(True)

        self.selected_area = None

        self.set_size_request(8096, 8096)

    def draw_selection_box(self, cairo):
        if not self.selected_area: return

        x, y, w, h = self.selected_area

        cairo.set_line_width(1.5)
        cairo.rectangle(x, y, w, h)

        cairo.set_source_rgba(0.7, 0.7, 1.0, 0.5)
        cairo.fill_preserve()

        cairo.set_source_rgba(0.3, 0.3, 0.7, 0.8)
        cairo.stroke()

    def draw_vertex(self, cairo, area, vertex):
        import math

        x = vertex.position[0]
        y = vertex.position[1]

        radius = vertex.size / 2

        # TODO - Custom colors

        if vertex.selected:
            cairo.set_source_rgb(0.4, 0.8, 0.2)
        else:
            r, g, b = vertex.fill_color[0], vertex.fill_color[1], vertex.fill_color[2]
            cairo.set_source_rgb(r, g, b)

        cairo.arc(x, y, radius, 0, 2 * math.pi)
        cairo.fill_preserve()

        r, g, b = vertex.border_color[0], vertex.border_color[1], vertex.border_color[2]
        cairo.set_source_rgb(r, g, b)
        cairo.set_line_width(vertex.border_size)
        cairo.arc(x, y, radius, 0, 2 * math.pi)
        cairo.stroke()

        font_size = 12
        cairo.set_font_size(font_size)
        x -= font_size
        y += font_size / 3.25
        cairo.move_to(x, y)
        cairo.show_text("%3s" % vertex.title)
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

    def draw_edges(self, cairo, area, vertex1, vertex2):
        edges = []

        for edge in vertex1.touching_edges:
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
        bhaskara_b = (2 * angular_coeficient * constant) - (2 * mx)
        bhaskara_b -= (2 * angular_coeficient * my)
        bhaskara_c = (mx ** 2) - (2 * constant * my) + (my ** 2)
        bhaskara_c += (constant ** 2)

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
        radius = edge.end.size / 2

        x1 = x1 - radius * math.cos(angle)
        y1 = y1 - radius * math.sin(angle)

        x2 = x2 + radius * math.cos(angle)
        y2 = y2 + radius * math.sin(angle)

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
            for edge in vertex.touching_edges:
                if not edge.visited:
                    if euclidean_distance(edge.start.position, edge.end.position) < 5:
                        edge.visited = True
                    else:
                        self.draw_edges(cairo, area, edge.start, edge.end)

        for vertex in self.graph.vertices:
            self.draw_vertex(cairo, area, vertex)

        for edge in self.graph.edges:
            edge.visited = None

        if self.adding_edge:
            cairo.set_source_rgb(0.7, 0.7, 0.7)
            cairo.set_line_width(1)

            cairo.set_dash((4, 1), 1)
            cairo.move_to(self.adding_edge[0][0], self.adding_edge[0][1])
            cairo.line_to(self.adding_edge[1][0], self.adding_edge[1][1])
            cairo.stroke()

            if self.graph.directed:
                self.draw_arrow(cairo, self.adding_edge[0], self.adding_edge[1])

            self.adding_edge = None

    def create_area(self, widget, event):
        self.area = widget.get_allocation()

        self.cairo = widget.window.cairo_create()

        self.cairo.rectangle(0, 0, self.area.width, self.area.height)
        self.cairo.clip()

    def expose(self, widget, event):
        self.create_area(widget, event)
        self.cairo.rectangle(0, 0, self.area.width, self.area.height)
        self.cairo.set_source_rgb(0.98, 1, 0.98)
        self.cairo.fill()

        self.draw_graph(self.cairo, self.area)
        self.draw_selection_box(self.cairo)

    def draw(self):
        self.cairo.save()
        self.queue_draw_area(0, 0, self.area.width, self.area.height)
        self.cairo.restore()


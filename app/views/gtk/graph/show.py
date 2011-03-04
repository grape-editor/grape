from gtk import DrawingArea
from app.models.graph import Graph
from app.controllers.graphs_controller import GraphsController
import gtk
import math

# TODO - Add scrollbars to graph

class GraphShow(DrawingArea):

    def __init__(self, changed_method):
        DrawingArea.__init__(self)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.MOTION_NOTIFY)
        self.add_events(gtk.gdk.BUTTON1_MOTION_MASK)
        self.add_events(gtk.gdk.KEY_PRESS_MASK)

        self.connect('expose-event', self.expose)
        self.connect('button-press-event', self.mouse_press)
        self.connect('button-release-event', self.mouse_release)
        self.connect('motion-notify-event', self.mouse_motion)

        self.action = None
        self.graph = Graph()
        self.controller = GraphsController()
        self.cairo = None
        self.changed = False
        self.path = None

        self.set_double_buffered(True)

        self.changed_method = changed_method

        self.last_clicked = None

    def set_changed(self, value):
        if self.changed != value:
            self.changed = value
            self.changed_method(self)

    def add_vertex(self, event):
        position = event.get_coords()
        self.controller.add_vertex(self.graph, position)
        self.action = None

    def remove_vertex(self, event):
        position = event.get_coords()
        vertex = self.graph.find_by_position(position)
        self.controller.remove_vertex(self.graph, vertex)
        self.action = None

    def add_edge(self, event):
        if len(self.graph.selected_vertices()) == 1:
            position = event.get_coords()
            vertex = self.graph.find_by_position(position)

            if vertex != None:
                self.controller.add_edge(self.graph, self.graph.selected_vertices()[0], vertex)
                self.controller.deselect_vertex(self.graph, self.graph.selected_vertices()[0])
                self.action = None

                return True
        else:
            self.select_vertex(event)

        return False

    def remove_edge(self, event):
        if len(self.graph.selected_vertices()) == 1:
            position = event.get_coords()
            vertex = self.graph.find_by_position(position)

            if vertex != None:
                # TODO - Handle multiple edges
                edge = self.graph.find_edge(self.graph.selected_vertices()[0], vertex)
                self.controller.remove_edge(self.graph, edge[0])
                self.controller.deselect_vertex(self.graph, self.graph.selected_vertices()[0])
                self.action = None

                return True
        else:
            self.select_vertex(event)

        return False

    def select_vertex(self, event):
        position = event.get_coords()
        vertex = self.graph.find_by_position(position)

        from gtk.gdk import CONTROL_MASK, SHIFT_MASK

        if not (event.state & CONTROL_MASK or event.state & SHIFT_MASK) and (len(self.graph.selected_vertices()) > 0):
            if not vertex or not vertex.selected:
                self.controller.clear_selection(self.graph)

        if vertex:
            if vertex.selected and (event.state & CONTROL_MASK or event.state & SHIFT_MASK):
                self.controller.deselect_vertex(self.graph, vertex)
            else:
                self.controller.select_vertex(self.graph, vertex)

            self.last_clicked = vertex
        else:
            self.controller.clear_selection(self.graph)

    def mouse_press(self, widget, event):
        if self.action != None:
            self.set_changed(True)
        if self.action == None:
            self.select_vertex(event)
        elif self.action == "add_vertex":
            self.add_vertex(event)
        elif self.action == "remove_vertex":
            self.remove_vertex(event)
        elif self.action == "add_edge":
            self.add_edge(event)
        elif self.action == "remove_edge":
            self.remove_edge(event)

        self.draw()

    def mouse_release(self, widget, event):
        self.last_clicked = None

    def mouse_motion(self, widget, event):
        selected_vertices = self.graph.selected_vertices()

        if len(selected_vertices) > 0:
            end_position = event.get_coords()
            start_position = self.last_clicked.position

            delta_x = end_position[0] - start_position[0]
            delta_y = end_position[1] - start_position[1]

            self.set_changed(True)

            for vertex in selected_vertices:
                new_position = [vertex.position[0] + delta_x, vertex.position[1] + delta_y]
                vertex.position = new_position

            self.draw()
            self.queue_draw()

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

    def bhaskara(self, a, b, c):
        delta = b ** 2 - 4 * a * c

        if delta < 0:
            return

        delta = math.sqrt(delta)
        xi = (-b + delta) / (2 * a)
        xii = (-b - delta) / (2 * a)

        return (xi, xii)

    def intersect_circles(self, b, c, a, r):
        bx, by = b
        cx, cy = c

        coef = (cy - by) / (- (cx - bx))
        cte = (- (cx ** 2) - (cy ** 2) + bx ** 2 + by ** 2 + (r ** 2) - (a ** 2)) / (-2 * cx + 2 * bx)

        bhaskara_a = coef ** 2 + 1
        bhaskara_b = 2 * coef * cte - 2 * coef * cx - 2 * cy
        bhaskara_c = cte ** 2 - 2 * cte * cx + cx ** 2 + cy ** 2 - r ** 2

        yi, yii = self.bhaskara(bhaskara_a, bhaskara_b, bhaskara_c)

        xi = yi * coef + cte
        xii = yii * coef + cte

        return ((xi, yi), (xii, yii))

    def euclidean_distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def nearest_points(self, points1, points2):
        if len(points1) != 2 or len(points2) != 2:
            return

        nearest = None
        distance = None

        for p1 in points1:
            for p2 in points2:
                d = self.euclidean_distance(p1, p2)
                if not distance or d < distance:
                    distance = d
                    nearest = (p1, p2)

        return nearest

    def draw_edges(self, cairo, area, vertex1, vertex2):
        edges = []

        for edge in vertex1.touching_edges:
            if edge.touches(vertex2):
                edges.append(edge)
                edge.visited = True

        if len(edges) == 0:
            return

        cairo.set_source_rgb(0, 0, 0)
        cairo.set_line_width(1)

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

            roots = self.bhaskara(bhaskara_a, bhaskara_b, bhaskara_c - (adjacent ** 2))

            angle = distance_arc + math.pi

            for i in range(2):
                edge = stack.pop()
                x = roots[i]
                y = angular_coeficient * x + constant

                points1 = self.intersect_circles((x, y), vertex1.position, radius, vertex1.size / 2)
                points2 = self.intersect_circles((x, y), vertex2.position, radius, vertex2.size / 2)
                points = self.nearest_points(points1, points2)

                opposite = self.euclidean_distance(points[0], points[1]) / 2
                beta = math.asin(opposite / radius) * 2
                offset = beta / 2

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

            for edge in vertex.touching_edges:
                if not edge.visited:
                    self.draw_edges(cairo, area, edge.start, edge.end)

        for vertex in self.graph.vertices:
            vertex.visited = None

        for edge in self.graph.edges:
            edge.visited = None

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


from gtk import DrawingArea, EventBox
from lib.mathemathical import *
from lib.edge import Edge
import gtk
import math
import cairo as cairolib


class GraphArea(DrawingArea):

    def __init__(self, graph):
        DrawingArea.__init__(self)
        self.connect('expose-event', self.expose)

        self.graph = graph
        self.cairo = None
        self.path = None
        self.adding_edge = None
        self.scale = 1

        self.set_double_buffered(True)
        self.selected_area = None
        self.area = None
        self.zoom = 1
        self.set_size_request(8096, 8096)

    def draw_selection_box(self, cairo):
        if not self.selected_area: return

        x, y, w, h = self.selected_area

        cairo.set_line_width(1.5)
        cairo.rectangle(x, y, w, h)

        # TODO - Config file
        cairo.set_source_rgba(0.7, 0.7, 1.0, 0.5)
        cairo.fill_preserve()

        cairo.set_source_rgba(0.3, 0.3, 0.7, 0.8)
        cairo.stroke()

    def draw_vertex(self, cairo, area, vertex):
        import math

        x = vertex.position[0]
        y = vertex.position[1]

        radius = vertex.size / 2

        if vertex.selected:
            # TODO - Config file
            cairo.set_source_rgb(0.4, 0.8, 0.2)
        else:
            cairo.set_source_color(gtk.gdk.Color(vertex.fill_color))

        cairo.arc(x, y, radius, 0, 2 * math.pi)
        cairo.fill_preserve()

        cairo.set_source_color(gtk.gdk.Color(vertex.border_color))
        cairo.set_line_width(vertex.border_size)
        cairo.arc(x, y, radius, 0, 2 * math.pi)
        cairo.stroke()

        cairo.set_font_size(vertex.font_size)
        
        x_bearing, y_bearing, width, height = cairo.text_extents(vertex.title)[:4]
        
        x = vertex.position[0]
        y = vertex.position[1]
        
        cairo.move_to(x, y)
        cairo.move_to(x - width / 2 - x_bearing, y - height / 2 - y_bearing)
        cairo.show_text(vertex.title)
        
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

    def draw_edges(self, cairo, area, vertex1, vertex2, closer=False):
        edges = []

        for edge in vertex1.touching_edges:
            if edge.touches(vertex2):
                edges.append(edge)
                edge.visited = True

        if len(edges) == 0:
            return

        if len(edges) > 1:
            x1, y1 = edges[0].start.position
            x2, y2 = edges[0].end.position
            mx, my = ((x1 + x2) / 2, (y1 + y2) / 2)
            distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    
            alpha = (math.pi / 4) / (len(edges) / 2) / 1.5
            step = (math.pi / 4) / (len(edges) / 2)
    
            stack = list(edges)
            before = None
    
            while len(stack) > 1:
                angle = alpha
                
                for i in range(2):
                    edge = stack.pop()
                    
                    if before and edge.start == before.start:
                        angle *= -1
                    
                    x1, y1, x2, y2, x3, y3, x4, y4 = get_edge_line(edge, angle)
                    
                    cairo.set_source_color(gtk.gdk.Color(edge.color))
                    cairo.set_line_width(edge.width)
                    
                    cairo.move_to(x1, y1)
                    
                    cairo.curve_to(x3, y3, x4, y4, x2, y2)
                    cairo.stroke()
                    
                    if not edge.bidirectional:
                        self.draw_arrow(cairo, (x4, y4), (x2, y2))
                        
                    before = edge
                alpha += step

            if len(stack) == 1:
                edge = stack.pop()
                self.draw_edge_straight(cairo, edge)
        else:
            self.draw_edge_straight(cairo, edges[0])

    def draw_edge_straight(self, cairo, edge):
        x1, y1, x2, y2 = get_edge_line(edge, 0)

        print edge.color
        cairo.set_source_color(gtk.gdk.Color(edge.color))
        
        cairo.set_line_width(edge.width)

        cairo.move_to(x1, y1)
        cairo.line_to(x2, y2)
        cairo.stroke()

        if not edge.bidirectional:
            self.draw_arrow(cairo, (x1, y1), (x2, y2))

    def draw_graph(self, cairo, area):
        #Creating atributte visited for each edge
        for edge in self.graph.edges:
            edge.system_visited = False

        for vertex in self.graph.vertices:
            self.draw_vertex(cairo, area, vertex)

        for vertex in self.graph.vertices:
            for edge in vertex.touching_edges:
                if not edge.system_visited:
                    if euclidean_distance(edge.start.position, edge.end.position) < (edge.start.size / 2 + edge.start.border_size + edge.end.size / 2 + edge.end.border_size):
                        self.draw_edge_straight(cairo, edge)
                    else:
                        self.draw_edges(cairo, area, edge.start, edge.end)

        #Removing atributte visited from each edge
        for edge in self.graph.edges:
            del edge.system_visited

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
        m = cairolib.Matrix(self.zoom, 0, 0, self.zoom, 0, 0)
        self.cairo.transform(m)
        self.cairo.rectangle(0, 0, self.area.width, self.area.height)

        self.cairo.set_source_color(gtk.gdk.Color(self.graph.background_color))
        self.cairo.fill()

        self.draw_graph(self.cairo, self.area)
        self.draw_selection_box(self.cairo)

    def draw(self):
        self.cairo.save()
        self.queue_draw_area(0, 0, self.area.width, self.area.height)
        self.cairo.restore()


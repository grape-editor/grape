from gtk import DrawingArea
from app.models.graph import Graph
from app.controllers.graphs_controller import GraphsController
import gtk
        
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
        
    def move_vertex(self, event):
        #Comment here to take this code cool
        #if len(self.graph.selected_vertices()) > 0:
        #    self.controller.clear_selection(self.graph)
        ###
        self.select_vertex(event)
            
    def select_vertex(self, event):
        position = event.get_coords()
        vertex = self.graph.find_by_position(position)
        
        if vertex:
            self.controller.select_vertex(self.graph, vertex)
        else:
            self.controller.clear_selection(self.graph)
        
    def mouse_press(self, widget, event):
        if self.action != None:
            self.set_changed(True)
        if self.action == None:
            self.move_vertex(event)
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
        pass
    
    def mouse_motion(self, widget, event):
        selected_vertices = self.graph.selected_vertices()
        if len(selected_vertices) > 0:
            start_position = selected_vertices[-1].position
            end_position = event.get_coords()
            
            delta_x = end_position[0] - start_position[0]
            delta_y = end_position[1] - start_position[1]
                        
            self.set_changed(True)
            
            for vertex in selected_vertices:
                new_position = [vertex.position[0] + delta_x, vertex.position[1] + delta_y]
                vertex.position = new_position
            
            self.draw()
            self.queue_draw()

#    def keyboard_press(self, widget, event):
#        keyname = gtk.gdk.keyval_name(event.keyval)
#        print "Key %s (%d) was pressed" % (keyname, event.keyval)
#        if event.state & gtk.gdk.CONTROL_MASK:
#            print "Control was being held down"
#        if event.state & gtk.gdk.MOD1_MASK:
#            print "Alt was being held down"
#        if event.state & gtk.gdk.SHIFT_MASK:
#            print "Shift was being held down"

    def draw_vertex(self, cairo, area, vertex):
        import math
        
        x = vertex.position[0]
        y = vertex.position[1]
        
        radius = vertex.size / 2
        
        # TODO - Custom colors
        
        if vertex.selected:
            cairo.set_source_rgb(1, 0, 0)
        else:
            cairo.set_source_rgb(vertex.color[0], vertex.color[1], vertex.color[2])
        
        cairo.arc(x, y, radius, 0, 2 * math.pi)
        cairo.fill_preserve()
        cairo.stroke()

    def draw_edge(self, cairo, area, edge):
        # TODO - Directional edges arrows
        
        cairo.set_source_rgb(0, 0, 0)
        cairo.set_line_width(1)
        
        x1, y1 = edge.start.position[0], edge.start.position[1]
        x2, y2 = edge.end.position[0], edge.end.position[1]
        
        cairo.move_to(x1, y1)
        cairo.line_to(x2, y2)
        cairo.stroke()

    def draw_graph(self, cairo, area):
        for edge in self.graph.edges:
            edge.visited = False
            
        for vertex in self.graph.vertices:
            self.draw_vertex(cairo, area, vertex)
            
            vertex.visited = True
            
            for edge in vertex.adjacencies:
                if not edge.visited:
                    self.draw_edge(cairo, area, edge)

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

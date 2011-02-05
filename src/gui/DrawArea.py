from gtk import DrawingArea
from lib.graph.Graph import Graph

import gtk

class DrawArea(DrawingArea):
    def __init__(self, changed_method, complete=False):
        DrawingArea.__init__(self)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.MOTION_NOTIFY)
        self.add_events(gtk.gdk.BUTTON1_MOTION_MASK)
        self.add_events(gtk.gdk.KEY_PRESS_MASK)
         
        self.connect('expose-event', self.expose)
        self.connect('button-press-event', self.mouse_press)
        self.connect('button-release-event',self.mouse_release)
        self.connect('motion-notify-event',self.mouse_motion)
        
        self.action = None
        self.select = None
        self.graph = Graph(complete)
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
        self.graph.add_vertex(position)
        self.action = None
    
    def remove_vertex(self, event):
        position = event.get_coords()
        self.graph.remove_vertex(position)
        self.action = None
        
    def add_edge(self, event):
        if self.select:
            position = event.get_coords()
            vertex = self.graph.get_vertex_position(position)
            if vertex != None:
                self.graph.add_edge(self.select, vertex)
                self.deselect_vertex()
                #self.action = None
                return True
        else:
            self.select_vertex(event)
        return False
            
    def remove_edge(self, event):
        if self.select:
            position = event.get_coords()
            vertex = self.graph.get_vertex_position(position)
            if vertex != None:
                self.graph.remove_edge(self.select, vertex)
                self.deselect_vertex()
                #self.action = None
                return True
        else:
            self.select_vertex(event)
        return False
        
    def move_vertex(self, event):
        if self.select:
            self.deselect_vertex()
        self.select_vertex(event)
            
    def select_vertex(self, event):
        if self.select:
            self.deselect_vertex()
        position = event.get_coords()
        self.select = self.graph.get_vertex_position(position)
        if self.select:
            self.select.select(True)
    
    def deselect_vertex(self):
        if self.select:
            self.select.select(False)
            self.select = None
        
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
        pass
        
    def mouse_motion(self, widget, event):
        if self.select:
            self.set_changed(True)
            position = event.get_coords()
            self.select.position = position
            self.draw()
            self.queue_draw()

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
        
        self.graph.draw(self.cairo, self.area)
        
    def draw(self):
        self.cairo.save()
        self.queue_draw_area(0, 0, self.area.width, self.area.height)
        self.cairo.restore()

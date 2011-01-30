from gtk import DrawingArea
from lib.Graph import Graph

import gtk

class DrawArea(DrawingArea):
    
    def __init__(self):
        DrawingArea.__init__(self)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.MOTION_NOTIFY)
        self.add_events(gtk.gdk.BUTTON1_MOTION_MASK)
        self.add_events(gtk.gdk.KEY_PRESS_MASK)
         
        
        self.connect('expose-event', self.draw)
        self.connect('button-press-event', self.mouse_press)
        self.connect('button-release-event',self.mouse_release)
        self.connect('motion-notify-event',self.mouse_motion)
        
        self.action = None
        self.select = None
        self.title = "New Graph"
        self.graph = Graph(self.title)
        

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
            vertex = self.graph.get_vertex(position)
            if vertex != None:
                self.graph.add_edge(self.select, vertex)
                self.deselect_vertex()
                self.action = None
                return True
        else:
            self.select_vertex(event)     
            
        return False
            
    def remove_Edge(self, event):
        print ("remove_edge")
        
    def move_vertex(self, event):
        if self.select:
            self.deselect_vertex()
        self.select_vertex(event)
            
    def select_vertex(self, event):
        if self.select:
            self.deselect_vertex()
        position = event.get_coords()
        self.select = self.graph.get_vertex(position)
        if self.select:
            self.select.select(True)
    
    def deselect_vertex(self):
        if self.select:
            self.select.select(False)
            self.select = None
        
    def remove_neighborhood(self):
        print "Opcao nao existe"
        
    def mouse_press(self, widget, event):       
        if self.action == None:
            self.select_vertex(event)
        elif self.action == "add_vertex":
            self.add_vertex(event)
        elif self.action == "remove_vertex":
            self.remove_vertex(event)
        elif self.action == "add_edge":
            self.add_edge(event)
        elif self.action == "remove_edge":
            self.remove_Edge(event)

        self.draw(self, event)
        
    def mouse_release(self, widget, event):
        print "mouse_released"
        
    def mouse_motion(self, widget, event):
        if self.select:
            position = event.get_coords()
            self.select.position = position
            self.draw(self, event)

    def draw(self, widget, event):
        area = widget.get_allocation()
        cairo = widget.window.cairo_create()
        cairo.rectangle(0, 0, area.width, area.height)
        cairo.set_source_rgb(1, 1, 1)     
        cairo.fill()
        
        self.graph.draw(cairo, area)
from gtk import DrawingArea
from lib.Graph import Graph

import gtk

class DrawArea(DrawingArea):
    
    def __init__(self):
        DrawingArea.__init__(self)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.MOTION_NOTIFY)
        self.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.connect('expose-event', self.draw)
        self.connect('button-press-event', self.mouse_press)
        self.connect('button-release-event',self.mouse_release)
        self.connect('motion-notify-event',self.mouse_motion)
        
        self.action = None
        self.title = "New Graph"
        self.graph = Graph(self.title)


    def add_vertex(self, event):
        print "add_vertex"
        position = event.get_coords()
        self.graph.add_vertex(position)
    
    def remove_vertex(self, event):
        print "remove_vertex"
        position = event.get_coords()
        self.graph.remove_vertex(position)
        
    def add_neighborhood(self):
        print "Opcao nao existe"
        
    def remove_neighborhood(self):
        print "Opcao nao existe"
        
    def mouse_press(self, widget, event):
        print "mouse press"
        if self.action == "add_vertex":
            self.add_vertex(event)
        elif self.action == "remove_vertex":
            self.remove_vertex(event)
        self.draw(self, event)
        
    def mouse_release(self, widget, event):
        print "mouse release"
    
    def mouse_motion(self, widget, event):
        print "mouse motion"

    def draw(self, widget, event):
        area = widget.get_allocation()
        cairo = widget.window.cairo_create()
        cairo.rectangle(0, 0, area.width, area.height)
        cairo.set_source_rgb(1, 1, 1)     
        cairo.fill()
        
        self.graph.draw(cairo, area)
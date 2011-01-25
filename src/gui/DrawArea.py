import gtk

class DrawArea:
    name = 0

    def __init__(self, draw_area):
        self.draw_area = draw_area
        self.draw_area.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.draw_area.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.draw_area.add_events(gtk.gdk.MOTION_NOTIFY)
        self.draw_area.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.draw_area.connect('expose-event', self.expose)
        self.draw_area.connect('button-press-event', self.mouse_press)
        self.draw_area.connect('button-release-event',self.mouse_release)
        self.draw_area.connect('motion-notify-event',self.mouse_motion)
        

    def add_vertex(self, event):
        print "Adicionando um vertice"
        position = event.get_coords()
        self.graph.add_vertex(self.name, position)
        self.name = self.name + 1
                
    def remove_vertex(self, event):
        mouse = event.get_coords()
        for v in self.graph.vertex:
            r = v.size / 2
            x = v.position[0]
            y = v.position[1]
            if (x - r) <= mouse[0] and (x + r) >= mouse[0] and (y - r) <= mouse[1] and (y + r) >= mouse[1]:
                print "Clicou em um vertice"
                self.graph.remove_vertex(v)
                break

        
    def add_neighborhood(self):
        print "Opcao nao existe"
        
    def remove_neighborhood(self):
        print "Opcao nao existe"
        

    def mouse_press(self, widget, event):
        if self.action == "add_vertex":
            self.add_vertex(event)
        elif self.action == "remove_vertex":
            self.remove_vertex(event)
        print self.action
        self.expose(self.draw_area, event)
        
    def mouse_release(self, widget, event):
        print "mouse release"
    
    def mouse_motion(self, widget, event):
        print "mouse motion"

    def expose(self, widget, event):
        cairo = widget.window.cairo_create()
        area = widget.get_allocation()
        cairo.rectangle(0, 0, area.width, area.height)
        cairo.set_source_rgb(1, 1, 1)
        cairo.fill()
        self.draw(cairo, area)    
    
    def draw(self, cairo, area):
        for v in self.vertex:
            v.draw(cairo, area)















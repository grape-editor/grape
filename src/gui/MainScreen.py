import gtk
import math

class Vertex(object):
    name = None
    color = [0, 0, 0]
    position = [0, 0]
    neighborhood = [] 
    size = 10

    def __init__(self, name):
        self.name = name
    
    def set_position(self, posx, posy):
        self.position = [posx, posy]
    
    def set_color(self, r, g, b):
        self.color = [r, g, b]
    
    def is_neighbor(self, vertex):
        for v in self.neighborhood:
            if v == vertex:
                return True
        return False
    
    def add_neighbor(self, vertex):
        if isinstance(vertex, Vertex):
            self.neighborhood.append(vertex)
            vertex.add_neighbor(self)
        
    def remove_neighbor(self, vertex):
        for v in self.neighborhood:
            if v == vertex:
                self.neighborhood.remove(v)
                v.remove_neighbor(self)

    def remove_all_neighbor(self):
        for v in self.neighborhood:
            self.neighborhood.remove(v)
            v.remove_neighbor(self)

    def draw(self, cairo, area):
            x = self.position[0]
            y = self.position[1]
            radius = self.size / 2
            cairo.arc(x, y, radius, 0, 2 * math.pi)
            cairo.set_source_rgb(0, 0, 0)
            cairo.fill_preserve()
            cairo.stroke()  
    
class MainScreen(object):
    

    name = 0

    vertex = []
    edge = []
    
        
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("gui/MainScreen.ui")
        builder.connect_signals(self)
        #self.main_window = gtk.Window()
        #self.draw_area = gtk.DrawingArea()
        self.main_window = builder.get_object("main_screen")
        self.draw_area = builder.get_object("drawingarea")
        self.main_window.connect("destroy", gtk.main_quit)
        self.draw_area.connect("expose-event", self.expose)
        self.init_drawarea()
        self.main_window.show_all()
        gtk.main()
         
    def main_quit(self, widget):
        gtk.main_quit()
                
    def menu_file_new(self, widget):
        print "menu_file_new"
    
    def menu_file_open(self, widget):
        print "menu_file_open"
    
    def menu_file_save(self, widget):
        print "menu_file_save"
    
    def menu_file_saveas(self, widget):
        print "menu_file_saveas"
    
    def menu_file_quit(self, widget):
        print "menu_file_quit"
        self.main_quit(widget)
    
    def menu_edit_cut(self, widget):
        print "menu_edit_cut"
    
    def menu_edit_copy(self, widget):
        print "menu_edit_copy"
    
    def menu_edit_paste(self, widget):
        print "menu_edit_past"
    
    def menu_edit_delete(self, widget):
        print "menu_edit_delete"



    def init_drawarea(self):
        self.draw_area.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.draw_area.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.draw_area.add_events(gtk.gdk.MOTION_NOTIFY)
        self.draw_area.add_events(gtk.gdk.KEY_PRESS_MASK)

        self.draw_area.connect('expose-event', self.expose)
        self.draw_area.connect('button-press-event', self.mouse_press)
        self.draw_area.connect('button-release-event',self.mouse_release)
        self.draw_area.connect('motion-notify-event',self.mouse_motion)
        
        self.main_window.connect('key-press-event', self.keyboard_type)            

    def add_vertex(self, event):
        print "Adicionando um vertice"
        mouse = event.get_coords()
        v = Vertex(self.name)
        v.position = mouse
        self.name = self.name + 1
        self.vertex.append(v)
        
    def remove_vertex(self, event):
        mouse = event.get_coords()
        for v in self.vertex:
            r = v.size / 2
            x = v.position[0]
            y = v.position[1]
            if (x - r) <= mouse[0] and (x + r) >= mouse[0] and (y - r) <= mouse[1] and (y + r) >= mouse[1]:
                print "Clicou em um vertice"
                self.vertex.remove(v)
                v.remove_all_neighbor()
                break

        
    def add_neighborhood(self):
        print "Opcao nao existe"
        
    def remove_neighborhood(self):
        print "Opcao nao existe"
        
    def keyboard_type(self, widget, event):
        key = event.keyval
        if key == gtk.keysyms.a or key == gtk.keysyms.A: 
            self.action = "add_vertex"
        elif key == gtk.keysyms.r or key == gtk.keysyms.R:
            self.action = "remove_vertex"
        
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
        self.draw(cairo, widget.get_allocation())
    
    def draw(self, cairo, area):
        size = self.main_window.get_size()
        cairo.rectangle(0, 0, size[0], size[1])
        cairo.clip()
        for v in self.vertex:
            v.draw(cairo, area)
        
        
import gtk

class MainScreen(object):
    window = gtk.Window() 
    builder = gtk.Builder()
    drawarea = gtk.DrawingArea()
    

    
    def __init__(self):
        self.builder.add_from_file("gui/MainScreen.ui")         
        self.window = self.builder.get_object("main_screen")       
        self.builder.connect_signals(self)
        self.initDrawarea()
        self.window.show_all()
         
    
    
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
            
       
    def teste(self):
        print 'teste'
        
    def initDrawarea(self):
        self.drawarea = self.builder.get_object("drawingarea")
        self.drawarea.connect('expose-event', self.paint)
        
        self.drawarea.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.drawarea.connect('button-press-event', self.node)
    
        
    
    def main(self):
        gtk.main()
    
    def paint(self, drawning, event):
        print "Pintei"
        
    def node(self, drawning, event):
        print "lalala"
        point = event.get_coords()
        print point[0]
        print point[1]
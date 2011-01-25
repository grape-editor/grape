from DrawArea import DrawArea

import gtk
import math


class MainScreen(object):

    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("gui/MainScreen.ui")
        builder.connect_signals(self)
        self.main_window = builder.get_object("main_screen")
        
        self.draw_area = DrawArea(builder.get_object("drawingarea"))
        
        self.main_window.connect("destroy", self.main_quit)
        self.main_window.connect('key-press-event', self.keyboard_type) 
        
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
    
    def keyboard_type(self, widget, event):
        key = event.keyval
        if key == gtk.keysyms.a or key == gtk.keysyms.A: 
            self.draw_area.action = "add_vertex"
        elif key == gtk.keysyms.r or key == gtk.keysyms.R:
            self.draw_area.action = "remove_vertex"

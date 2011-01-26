from DrawArea import DrawArea
import gtk
import math


class MainScreen(object):

    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("gui/MainScreen.ui")
        builder.connect_signals(self)
        self.main_window = builder.get_object("main_screen")
        
        self.notebook = builder.get_object("notebook")
        self.notebook.connect("page-removed", self.page_has_change)
        
        self.main_window.connect("destroy", self.main_quit)
        self.main_window.connect('key-press-event', self.keyboard_type) 
        
        self.name = 0
        self.main_window.show_all()
        gtk.main()

    def main_quit(self, widget):
        gtk.main_quit()
    
    def menu_file_new(self, widget):
        print "menu_file_new"

        draw_area = DrawArea()
        
        hbox = gtk.HBox(False, 0)
        #get a stock close button image
        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
        
        #make the close button
        btn = gtk.Button()
        btn.set_relief(gtk.RELIEF_NONE)
        btn.set_focus_on_click(False)
        btn.add(close_image)
        
        #this reduces the size of the button
        style = gtk.RcStyle()
        style.xthickness = 0
        style.ythickness = 0
        btn.modify_style(style)
        
        #Added title and buttom
        hbox.pack_start(gtk.Label(draw_area.title))
        hbox.pack_start(btn, False, False)        
        hbox.show_all()

        #Put this tab in the notebook
        self.notebook.append_page(draw_area, hbox) 
        self.notebook.show_all() 
        
        #connect the close button        
        btn.connect('clicked', self.page_close_buttom_clicked, draw_area)
    
    def page_has_change(self, notebook, child, pagenum):
        print "page_has_change"
        self.menu_file_save(child)
        self.menu_file_save_as(child)
    
    def page_close_buttom_clicked(self, sender, widget):
        page_number = self.notebook.page_num(widget)
        self.notebook.remove_page(page_number)
    
    def menu_file_open(self, widget):
        print "menu_file_open"
    
    def menu_file_save(self, widget):
        print "menu_file_save"
    
    def menu_file_save_as(self, widget):
        print "menu_file_save_as"
    
    def menu_file_revert(self, widget):
        print "menu_file_revert"
            
    def menu_file_close(self, widget):
        print "menu_file_close"
        i = self.notebook.get_current_page()
        page = self.notebook.get_nth_page(i)
        if page and self.notebook.get_n_pages() > 0:
            self.notebook.remove_page(i)
            page.destroy()
            #self.tabs.remove(page)
    
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
            
    def menu_view_fullscreen_on(self, widget):
        print "menu_view_fullscreen_on"
    
    def menu_view_fullscreen_off(self, widget):
        print "menu_view_fullscreen_off"

    def keyboard_type(self, widget, event):
        key = event.keyval
        if key == gtk.keysyms.a or key == gtk.keysyms.A: 
            self.draw_area.action = "add_vertex"
        elif key == gtk.keysyms.r or key == gtk.keysyms.R:
            self.draw_area.action = "remove_vertex"

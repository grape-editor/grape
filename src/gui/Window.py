from DrawArea import DrawArea
from AboutDialog import AboutDialog
from SaveAs import SaveAs


import gtk
import os
import sys

class Window(object):  
    def __init__(self, builder):
        #domain = self.translate()
        #builder = gtk.Builder()
        #builder.set_translation_domain(domain)          

        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        path = os.path.join(path, "gui", "Window.ui")
        
        self.builder = builder
        self.builder.add_from_file(path)
        self.builder.connect_signals(self)
        
        self.window = builder.get_object("window")
        self.notebook = builder.get_object("notebook")
        
        self.window.connect("destroy", self.main_quit)
        self.window.connect('key-press-event', self.keyboard_type) 
        self.notebook.connect("page-removed", self.page_has_change)
        self.notebook.set_scrollable(True)
        self.notebook.set_group_id(0)
        
        self.name = 0
        self.window.show_all()
        
    def move_screen(self, x, y):
        self.window.move(x, y)
    
    def page_current_draw_area(self):
        current_page_number = self.notebook.get_current_page()
        draw_area = self.notebook.get_nth_page(current_page_number)
        return draw_area 
        
    def page_has_change(self, notebook, child, pagenum):
        print _("page_has_change")
        self.menu_file_save(child)
        self.menu_file_save_as(child)
    
    def page_close_buttom_clicked(self, widget):
        page_number = widget.get_parent().page_num(widget)
        widget.get_parent().remove_page(page_number)
    
    def main_quit(self, widget):
        self.window.destroy()
        
    def add_tab(self, tab):
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
        hbox.pack_start(gtk.Label(tab.title))
        hbox.pack_start(btn, False, False)        
        hbox.show_all()

        #Put this tab in the notebook
        self.notebook.append_page(tab, hbox)
        last_page = self.notebook.get_n_pages() - 1
        if last_page > 0:
            self.notebook.set_current_page(last_page)
        
        print last_page
        print self.notebook.get_current_page()
        
        self.notebook.set_tab_reorderable(tab, True)
        self.notebook.set_tab_detachable(tab, True)
        
        #connect the close button        
        btn.connect_object('clicked', self.page_close_buttom_clicked, tab)
        self.notebook.show_all()
        
        tab.close_button = btn
    
    def menu_file_new(self, widget):
        print _("menu_file_new")
        draw_area = DrawArea()
        self.add_tab(draw_area)
    
    def menu_file_open(self, widget):
        print _("menu_file_open")
    
    def menu_file_save(self, widget):
        print _("menu_file_save")
    
    def menu_file_save_as(self, widget):
        print _("menu_file_save_as")
        i = self.notebook.get_current_page()
        draw_area = self.notebook.get_nth_page(i)
        if draw_area and self.notebook.get_n_pages() > 0:
            SaveAs(self.builder, draw_area.graph)
    
    def menu_file_revert(self, widget):
        print _("menu_file_revert")
            
    def menu_file_close(self, widget):
        i = self.notebook.get_current_page()
        page = self.notebook.get_nth_page(i)
        if page and self.notebook.get_n_pages() > 0:
            self.notebook.remove_page(i)
            page.destroy()
            #self.tabs.remove(page)
    
    def menu_file_quit(self, widget):
        print _("menu_file_quit")
        self.main_quit(widget)
    
    def menu_edit_cut(self, widget):
        print _("menu_edit_cut")
    
    def menu_edit_copy(self, widget):
        print _("menu_edit_copy")
    
    def menu_edit_paste(self, widget):
        print _("menu_edit_past")
        
    def menu_edit_add_vertex(self, widget):
        draw_area = self.page_current_draw_area()
        if draw_area:
            draw_area.action = "add_vertex"
    
    def menu_edit_remove_vertex(self, widget):
        draw_area = self.page_current_draw_area()
        if draw_area:
            draw_area.action = "remove_vertex"
    
    def menu_edit_add_edge(self, widget):
        draw_area = self.page_current_draw_area()
        if draw_area:
            draw_area.action = "add_edge"
      
    def menu_edit_remove_edge(self, widget):
        draw_area = self.page_current_draw_area()
        if draw_area:
            draw_area.action = "remove_edge"
    
    def menu_edit_delete(self, widget):
        print _("menu_edit_delete")
            
    def menu_view_fullscreen_on(self, widget):
        print _("menu_view_fullscreen_on")
    
    def menu_view_fullscreen_off(self, widget):
        print _("menu_view_fullscreen_off")
        
    def menu_help_about(self, widget):
        AboutDialog()
        
    def keyboard_type(self, widget, event):
        print _("keyboard_type")
        draw_area = self.page_current_draw_area()
        
        key = event.keyval
        if key == gtk.keysyms.a or key == gtk.keysyms.A: 
            draw_area.action = "add_vertex"
        elif key == gtk.keysyms.r or key == gtk.keysyms.R:
            draw_area.action = "remove_edge"
        elif key == gtk.keysyms.e or key == gtk.keysyms.E:
            draw_area.action = "add_edge"

    

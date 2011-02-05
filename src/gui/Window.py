from DrawArea import DrawArea
from AboutDialog import AboutDialog
from FileChooserDialog import FileChooserDialog


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
        
        #self.window.connect("destroy", self.window_main_quit)
        self.window.connect('key-press-event', self.window_keyboard_type) 
        #self.notebook.connect("page-removed", self.notebook_page_has_change)
        self.notebook.set_scrollable(True)
        self.notebook.set_group_id(0)
        
        self.name = 0
        self.window.show_all()
        
    def notebook_page_current_draw_area(self):
        current_page_number = self.notebook.get_current_page()
        draw_area = self.notebook.get_nth_page(current_page_number)
        return draw_area 
    
    def notebook_page_close_buttom_clicked(self, widget):
        page_number = widget.get_parent().page_num(widget)
        widget.get_parent().remove_page(page_number)
       
    def notebook_add_tab(self, tab):
        #Put this tab in the notebook
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
        hbox.pack_start(gtk.Label(tab.graph.title))
        hbox.pack_start(btn, False, False)        
        
        self.notebook.append_page(tab, hbox)
        last_page = self.notebook.get_n_pages() - 1
        if last_page > 0:
            self.notebook.set_current_page(last_page)
        
        self.notebook.set_tab_reorderable(tab, True)
        self.notebook.set_tab_detachable(tab, True)
        
        #connect the close button        
        n = self.notebook.page_num(tab)
        
        btn.connect_object('clicked', self.notebook_page_close_buttom_clicked, tab)
        
        hbox.show_all()
        self.notebook.show_all()
        
        tab.close_button = btn
        self.notebook.set_current_page(n)
    
    def notebook_tab_changed(self, drawarea):
        box = self.notebook.get_tab_label(drawarea)
        label = box.get_children()[0]
        if drawarea.changed:
            label.set_label("* " + drawarea.graph.title)
        else:
            label.set_label(drawarea.graph.title)
    
    def menu_file_new(self, widget):
        draw_area = DrawArea(self.notebook_tab_changed)
        self.notebook_add_tab(draw_area)

    def menu_file_new_complete(self, widget):
        draw_area = DrawArea(self.notebook_tab_changed, True)
        self.notebook_add_tab(draw_area)
    
    def menu_file_open(self, widget):
        draw_area = DrawArea(self.notebook_tab_changed)
        open_file = FileChooserDialog(self.builder, draw_area)
        open_file.file_chooser_dialog_method_open()
        open_file.file_chooser_dialog_show()
        self.notebook_add_tab(draw_area)
        #draw_area.expose(widget, None)
        
  
    def menu_file_save(self, widget):
        i = self.notebook.get_current_page()
        draw_area = self.notebook.get_nth_page(i)
        if draw_area:
            if not draw_area.path:
                self.menu_file_save_as(widget)
            else:
                save = FileChooserDialog(self.builder, draw_area)
                save.save_file(draw_area.path)
    
    def menu_file_save_as(self, widget):
        i = self.notebook.get_current_page()
        draw_area = self.notebook.get_nth_page(i)
        if draw_area and self.notebook.get_n_pages() > 0:
            save_as = FileChooserDialog(self.builder, draw_area)
            save_as.file_chooser_dialog_method_save()
            save_as.file_chooser_dialog_show()
    
    def menu_file_revert(self, widget):
        pass
                    
    def menu_file_close(self, widget):
        i = self.notebook.get_current_page()
        page = self.notebook.get_nth_page(i)
        if page and self.notebook.get_n_pages() > 0:
            self.notebook.remove_page(i)
            page.destroy()
            #self.tabs.remove(page)
    
    def menu_file_quit(self, widget):
        self.window_main_quit(widget)
    
    def menu_edit_cut(self, widget):
        pass
            
    def menu_edit_copy(self, widget):
        pass
            
    def menu_edit_paste(self, widget):
        pass
        
    def menu_edit_add_vertex(self, widget):
        draw_area = self.notebook_page_current_draw_area()
        if draw_area:
            draw_area.action = "add_vertex"
    
    def menu_edit_remove_vertex(self, widget):
        draw_area = self.notebook_page_current_draw_area()
        if draw_area:
            draw_area.action = "remove_vertex"
    
    def menu_edit_add_edge(self, widget):
        draw_area = self.notebook_page_current_draw_area()
        if draw_area:
            draw_area.action = "add_edge"
      
    def menu_edit_remove_edge(self, widget):
        draw_area = self.notebook_page_current_draw_area()
        if draw_area:
            draw_area.action = "remove_edge"
    
    def menu_edit_delete(self, widget):
        pass
                    
    def menu_view_fullscreen_on(self, widget):
        pass
        
    def menu_view_fullscreen_off(self, widget):
        pass
        
    def menu_help_about(self, widget):
        AboutDialog(self.builder)
        
    def window_keyboard_type(self, widget, event):
        draw_area = self.notebook_page_current_draw_area()
        
        key = event.keyval
        if key == gtk.keysyms.a or key == gtk.keysyms.A: 
            draw_area.action = "add_vertex"
        elif key == gtk.keysyms.r or key == gtk.keysyms.R:
            draw_area.action = "remove_vertex"
        elif key == gtk.keysyms.e or key == gtk.keysyms.E:
            draw_area.action = "add_edge"

    def window_move_screen(self, x, y):
        self.window.move(x, y)
    
    def window_main_quit(self, widget):
        self.window.destroy()

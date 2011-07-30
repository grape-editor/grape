import gtk
import os
import sys
import locale
import gettext

class Edge(object):
    def __init__(self, graph_show, edge):
        path = os.path.dirname(__file__)
        path = os.path.join(path, "edge.ui")

        self.edge = edge
        self.area = graph_show.area
        self.set_changed = graph_show.set_changed
        self.graph = graph_show.graph
        self.controller = graph_show.controller
        self.add_state = graph_show.add_state
        self.builder = graph_show.builder

        self.menu = None

        self.builder.add_from_file(path)

        self.screen = self.builder.get_object("edge_edit")
        self.label_id = self.builder.get_object("label_id")
        self.text_title = self.builder.get_object("text_title")
        self.color_edge = self.builder.get_object("color_edge")
        self.adjustment_width = self.builder.get_object("adjustment_width")

        self.treeview_properties = self.builder.get_object("treeview_properties")
        self.treeview_properties.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

        self.init_general_fields()
                
        self.builder.connect_signals(self)
        self.screen.show_all()

        self.liststore_properties = gtk.ListStore(str, str)
        self.treeview_properties.set_model(self.liststore_properties)
		
    def switch_page(self, notebook, page, page_num):
        if page_num == 0:
            self.init_general_fields()
        elif page_num == 1:
            self.init_property_fields()

    def update_property(self, cell, path, new_text, column):
        row_iter = self.liststore_properties.get_iter(path)
    
        identifier, value = self.liststore_properties.get(row_iter, 0, 1)

        if column == 0:
            # change attribue name
            t_value = getattr(self.edge, "user_" + identifier)
            delattr(self.edge, "user_" + identifier)
            setattr(self.edge, "user_" + new_text, t_value)

        elif column == 1:
            # change attribute value
            setattr(self.edge, "user_" + identifier, value)

        self.liststore_properties.set_value(row_iter, column, new_text)

        return

    def init_general_fields(self):
        renderer = gtk.CellRendererText()
        renderer.connect('edited', self.update_property, 0)
        renderer.set_property('editable', True)
        self.treeview_properties.insert_column_with_attributes(-1, 'Identifier', renderer, text=0)

        renderer = gtk.CellRendererText()
        renderer.connect('edited', self.update_property, 1)
        renderer.set_property('editable', True)
        self.treeview_properties.insert_column_with_attributes(-1, 'Value', renderer, text=1)

        self.label_id.set_label(str(self.edge.id))
        self.text_title.set_text(self.edge.title)
        
        self.color_edge.set_color(self.cairo_to_spin(self.edge.color))
        
        self.adjustment_width.value = self.edge.width

    def init_property_fields(self):
        self.liststore_properties.clear()
        for attr in self.edge.__dict__:
            if attr.startswith("user_"):
                t_identifier = attr[5:]
                t_value = getattr(self.edge, attr)
                self.liststore_properties.append([t_identifier, t_value])
        
    def keyboard_press(self, widget, event):
        key = event.keyval

        if key == gtk.keysyms.Delete:
            self.remove_edge()
            
        from gtk.gdk import CONTROL_MASK

        if (event.state & CONTROL_MASK):
            if key == gtk.keysyms.N or key == gtk.keysyms.n:
                self.add_edge()

    def mouse_press(self, widget, event):
        path = widget.get_path_at_pos(int(event.x), int(event.y))
        selection = widget.get_selection()
        
        store, row = selection.get_selected_rows()
        if not path:
            selection.unselect_all()

        if event.button == 3:
            if path:
                selection.select_path(path[0])
            self.right_click_menu(event)
            
    
    def right_click_menu(self, event):
        selection = self.treeview_properties.get_selection()

        def execute_action(event, action):
            action()

        if not self.menu:
            self.menu = gtk.Menu()
            self.menu_add_property = gtk.MenuItem(_("_Add property"))
            self.menu_remove_property = gtk.MenuItem(_("_Remove property"))

            self.menu_add_property.connect("activate", execute_action, self.add_property)
            self.menu_remove_property.connect("activate", execute_action, self.remove_property)

            self.menu.append(self.menu_add_property)
            self.menu.append(self.menu_remove_property)
            
        if selection.count_selected_rows() > 0:
            self.menu_remove_property.set_sensitive(True)
        else:
            self.menu_remove_property.set_sensitive(False)

        self.menu.show_all()
        self.menu.popup(None, None, None, event.button, event.time)

    def add_property(self):
        t_identifier = "foo"
        t_value = "bar"
        self.liststore_properties.append([t_identifier, t_value])

        setattr(self.edge, "user_" + t_identifier, t_value)
        
#        self.add_state()
#        self.area.queue_draw()

    def remove_property(self):
        selection = self.treeview_properties.get_selection()
        store, rows = selection.get_selected_rows()
        
        #Scamp way to delete all selecteds rows =D
        rows_reference = [gtk.TreeRowReference(store, row) for row in rows]

        for row in rows_reference:
            row_iter = store.get_iter(row.get_path())
            property_identifier = store.get_value(row_iter, 0)
            store.remove(row_iter)

            for attr in self.edge.__dict__:
                if attr.startswith("user_"):
                    t_identifier = attr[5:]
                    if t_identifier == property_identifier:
                        delattr(self.edge, attr)
    
#        self.add_state()
#        self.area.queue_draw()

    def cairo_to_spin(self, color):
        return gtk.gdk.Color(color[0] * 65535, color[1] * 65535, color[2] * 65535)
        
    def spin_to_cairo(self, color):
        return [color.red / 65535.0, color.green / 65535.0, color.blue / 65535.0]

    def title_changed(self, widget):
        self.edge.title = self.text_title.get_text()
        self.area.queue_draw()
        self.set_changed(True)
    
    def color_edge_changed(self, widget):
        self.edge.color = self.spin_to_cairo(widget.get_color())
        self.area.queue_draw()
        self.set_changed(True)
        
    def width_scale_changed(self, widget):
        self.edge.width = widget.value
        self.area.queue_draw()
        self.set_changed(True)
    
    def close(self, widget):
        self.screen.destroy()


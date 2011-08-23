import gtk
import os
import sys
import locale
import gettext

from gui.edge import Edge

class Vertex(object):
    def __init__(self, graph_show, vertex):
        path = os.path.dirname(__file__)
        path = os.path.join(path, "vertex.ui")

        self.graph_show = graph_show
        self.vertex = vertex
        self.area = graph_show.area
        self.set_changed = graph_show.set_changed
        self.graph = graph_show.graph
        self.add_state = graph_show.add_state

        self.builder = gtk.Builder()

        self.menu_edges = None
        self.menu_properties = None

        self.builder.add_from_file(path)

        self.screen = self.builder.get_object("vertex_edit")
        self.label_id = self.builder.get_object("label_id")
        self.text_title = self.builder.get_object("text_title")
        self.spin_posx = self.builder.get_object("spin_posx")
        self.spin_posy = self.builder.get_object("spin_posy")
        self.color_vertex = self.builder.get_object("color_vertex")
        self.color_border = self.builder.get_object("color_border")
        self.adjustment_radius = self.builder.get_object("adjustment_radius")
        self.adjustment_border = self.builder.get_object("adjustment_border")
        self.notebook = self.builder.get_object("notebook")
        self.treeview_edges = self.builder.get_object("treeview_edges")
        self.treeview_properties = self.builder.get_object("treeview_properties")

        self.treeview_edges.get_selection().set_mode(gtk.SELECTION_MULTIPLE)                
        self.treeview_properties.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

        self.liststore_edges = gtk.ListStore(str, str, str)
        self.liststore_properties = gtk.ListStore(str, str)

        self.treeview_edges.set_model(self.liststore_edges)
        self.treeview_properties.set_model(self.liststore_properties)

        self.treeview_create()
        self.builder.connect_signals(self)
        self.init_general_fields()
        self.screen.show_all()

    def treeview_create(self):
        renderer1 = gtk.CellRendererText()
        renderer1.connect('edited', self.edit_properties, 0)
        renderer1.set_property('editable', True)

        renderer2 = gtk.CellRendererText()
        renderer2.connect('edited', self.edit_properties, 1)
        renderer2.set_property('editable', True)

        self.treeview_properties.insert_column_with_attributes(-1, 'Identifier', renderer1, text=0)
        self.treeview_properties.insert_column_with_attributes(-1, 'Value', renderer2, text=1)

    def switch_page(self, notebook, page, page_num):
        if page_num == 0:
            self.init_general_fields()
        elif page_num == 1:
            self.init_edges_fields()
        elif page_num == 2:
            self.init_properties_fields()

    def init_general_fields(self):
        self.label_id.set_label(str(self.vertex.id))
        self.text_title.set_text(self.vertex.title)
        self.spin_posx.set_value(self.vertex.position[0])
        self.spin_posy.set_value(self.vertex.position[1])
        
        self.color_vertex.set_color(gtk.gdk.Color(self.vertex.fill_color))
        self.color_border.set_color(gtk.gdk.Color(self.vertex.border_color))
        
        self.adjustment_radius.value = self.vertex.size
        self.adjustment_border.value = self.vertex.border_size

    def init_edges_fields(self):
        number_of_edges = len(self.vertex.adjacencies)
        self.liststore_edges.clear()

        for i in range(number_of_edges):
            t_id = self.vertex.adjacencies[i].id
            t_start = self.vertex.adjacencies[i].start.title
            t_end = self.vertex.adjacencies[i].end.title
            self.liststore_edges.append([t_id, t_start, t_end])

    def init_properties_fields(self):
        self.liststore_properties.clear()
        for attr in self.vertex.__dict__:
            if attr.startswith("user_"):
                t_identifier = attr[5:]
                t_value = getattr(self.vertex, attr)
                self.liststore_properties.append([t_identifier, t_value])

    def keyboard_press(self, widget, event):
        current_page_number = self.notebook.get_current_page()
        key = event.keyval

        # Get like pointer to function
        add = remove = None
        if current_page_number == 1:
            add = self.add_edge
            remove = self.remove_edge
        elif current_page_number == 2:
            add = self.add_properties
            remove = self.remove_properties

        from gtk.gdk import CONTROL_MASK
        if key == gtk.keysyms.Delete:
            remove()
        if (event.state & CONTROL_MASK):
            if key == gtk.keysyms.N or key == gtk.keysyms.n:
                add()

    def mouse_press(self, widget, event):
        current_page_number = self.notebook.get_current_page()

        # Get like pointer to function
        right_click_menu = None
        if current_page_number == 1:
            right_click_menu = self.right_click_menu_edges
        elif current_page_number == 2:
            right_click_menu = self.right_click_menu_properties

        path = widget.get_path_at_pos(int(event.x), int(event.y))
        selection = widget.get_selection()
        
        store, row = selection.get_selected_rows()
        if not path:
            selection.unselect_all()

        if event.button == 3:
            if path:
                selection.select_path(path[0])
            right_click_menu(event)
    
    def right_click_menu_edges(self, event):
        selection = self.treeview_edges.get_selection()

        def execute_action(event, action):
            action()

        if not self.menu_edges:
            self.menu_edges = gtk.Menu()
            self.menu_add_edge = gtk.MenuItem(_("_Add edge"))
            self.menu_remove_edge = gtk.MenuItem(_("_Remove edge"))
            self.menu_edit_edge = gtk.MenuItem(_("_Edit edge settings"))

            self.menu_add_edge.connect("activate", execute_action, self.add_edge)
            self.menu_remove_edge.connect("activate", execute_action, self.remove_edge)
            self.menu_edit_edge.connect("activate", execute_action, self.edit_edge)

            self.menu_edges.append(self.menu_add_edge)
            self.menu_edges.append(self.menu_remove_edge)
            self.menu_edges.append(self.menu_edit_edge)

        if len(self.graph.vertices) > 1:
            self.menu_add_edge.set_sensitive(True)
        else:
            self.menu_add_edge.set_sensitive(False)
            
        if selection.count_selected_rows() == 1:
            self.menu_remove_edge.set_sensitive(True)
            self.menu_edit_edge.set_sensitive(True)
        elif selection.count_selected_rows() > 1:
            self.menu_remove_edge.set_sensitive(True)
            self.menu_edit_edge.set_sensitive(False)
        else:
            self.menu_remove_edge.set_sensitive(False)
            self.menu_edit_edge.set_sensitive(False)

        self.menu_edges.show_all()
        self.menu_edges.popup(None, None, None, event.button, event.time)

    def right_click_menu_properties(self, event):
        selection = self.treeview_properties.get_selection()

        def execute_action(event, action):
            action()

        if not self.menu_properties:
            self.menu_properties = gtk.Menu()
            self.menu_add_properties = gtk.MenuItem(_("_Add properties"))
            self.menu_remove_properties = gtk.MenuItem(_("_Remove properties"))

            self.menu_add_properties.connect("activate", execute_action, self.add_properties)
            self.menu_remove_properties.connect("activate", execute_action, self.remove_properties)

            self.menu_properties.append(self.menu_add_properties)
            self.menu_properties.append(self.menu_remove_properties)
            
        if selection.count_selected_rows() > 0:
            self.menu_remove_properties.set_sensitive(True)
        else:
            self.menu_remove_properties.set_sensitive(False)

        self.menu_properties.show_all()
        self.menu_properties.popup(None, None, None, event.button, event.time)

    def edit_edge(self):
        selection = self.treeview_edges.get_selection()
        store, rows = selection.get_selected_rows()

        row_iter = store.get_iter(rows[0])
        edge_id = store.get_value(row_iter, 0)
        
        edge = self.graph.find_edge_from_vertex(self.vertex, edge_id)
        if edge:
            edit_edge = Edge(self.graph_show, edge)
        
    def add_edge(self):
        idx = 0
        
        if self.vertex.id == 0:
            idx = len(self.graph.vertices) - 1
            
        vertex = self.graph.find(idx)
            
        if vertex:
            edge = self.graph.add_edge(self.vertex, vertex)

            if edge:
                t_id = edge.id
                t_start = edge.start.title
                t_end = edge.end.title
                self.liststore_edges.append([t_id, t_start, t_end])
                
            self.add_state()
            self.area.queue_draw()

    def remove_edge(self):
        selection = self.treeview_edges.get_selection()
        store, rows = selection.get_selected_rows()
        
        #Scamp way to delete all selecteds rows =D
        rows_reference = [gtk.TreeRowReference(store, row) for row in rows]

        for row in rows_reference:
            row_iter = store.get_iter(row.get_path())
            edge_id = store.get_value(row_iter, 0)
            store.remove(row_iter)
            
            edge = self.graph.find_edge_from_vertex(self.vertex, edge_id)
            if edge:
                self.graph.remove_edge(edge)
    
        self.add_state()
        self.area.queue_draw()

    def edit_properties(self, cell, path, new_text, column):
        row_iter = self.liststore_properties.get_iter(path)
    
        identifier, value = self.liststore_properties.get(row_iter, 0, 1)

        if column == 0:
            # change attribue name
            t_value = getattr(self.vertex, "user_" + identifier)
            delattr(self.vertex, "user_" + identifier)
            setattr(self.vertex, "user_" + new_text, t_value)

        elif column == 1:
            # change attribute value
            setattr(self.vertex, "user_" + identifier, value)

        self.liststore_properties.set_value(row_iter, column, new_text)
        return

    def add_properties(self):
        t_identifier = "foo"
        t_value = "bar"
        self.liststore_properties.append([t_identifier, t_value])

        setattr(self.vertex, "user_" + t_identifier, t_value)
        
#        self.add_state()
#        self.area.queue_draw()

    def remove_properties(self):
        selection = self.treeview_properties.get_selection()
        store, rows = selection.get_selected_rows()
        
        #Scamp way to delete all selecteds rows =D
        rows_reference = [gtk.TreeRowReference(store, row) for row in rows]

        for row in rows_reference:
            row_iter = store.get_iter(row.get_path())
            properties_identifier = store.get_value(row_iter, 0)
            store.remove(row_iter)

            for attr in self.vertex.__dict__:
                if attr.startswith("user_"):
                    t_identifier = attr[5:]
                    if t_identifier == properties_identifier:
                        delattr(self.vertex, attr)
                        break

#        self.add_state()
#        self.area.queue_draw()
    
    def title_changed(self, widget):
        self.vertex.title = self.text_title.get_text()
        self.area.queue_draw()
        self.set_changed(True)
        
    def positionx_changed(self, widget):
        self.vertex.position[0] = self.spin_posx.get_value()
        self.area.queue_draw()
        self.set_changed(True)
    
    def positiony_changed(self, widget):
        self.vertex.position[1] = self.spin_posy.get_value()
        self.area.queue_draw()
        self.set_changed(True)
    
    def color_vertex_changed(self, widget):
        self.vertex.fill_color = str(widget.get_color())
        self.area.queue_draw()
        self.set_changed(True)
        
    def color_border_changed(self, widget):
        self.vertex.border_color = str(widget.get_color())
        self.area.queue_draw()
        self.set_changed(True)
    
    def radius_scale_changed(self, widget):
        self.vertex.size = widget.value
        self.area.queue_draw()
        self.set_changed(True)
    
    def border_scale_changed(self, widget):
        self.vertex.border_size = widget.value
        self.area.queue_draw()
        self.set_changed(True)
    
    def close(self, widget):
        self.screen.destroy()


import gtk
import os
import sys
import locale
import gettext

from app.views.gtk.edge.edit import EdgeEdit

class VertexEdit(object):
    def __init__(self, graph_show, vertex):
        path = os.path.dirname(__file__)
        path = os.path.join(path, "edit.ui")

        self.graph_show = graph_show
        self.vertex = vertex
        self.area = graph_show.area
        self.set_changed = graph_show.set_changed
        self.graph = graph_show.graph
        self.controller = graph_show.controller
        self.add_state = graph_show.add_state
        self.builder = graph_show.builder

        self.menu = None

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

        self.treeview_edges = self.builder.get_object("treeview_edges")
        self.treeview_edges.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        
        self.liststore_edges = self.builder.get_object("liststore_edges")

        self.init_general_fields()
                
        self.builder.connect_signals(self)
        self.screen.show_all()

    def switch_page(self, notebook, page, page_num):
        if page_num == 0:
            self.init_general_fields()
        elif page_num == 1:
            self.init_edges_fields()

    def init_general_fields(self):
        self.label_id.set_label(str(self.vertex.id))
        self.text_title.set_text(self.vertex.title)
        self.spin_posx.set_value(self.vertex.position[0])
        self.spin_posy.set_value(self.vertex.position[1])
        
        self.color_vertex.set_color(self.cairo_to_spin(self.vertex.fill_color))
        self.color_border.set_color(self.cairo_to_spin(self.vertex.border_color))       
        
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
        selection = self.treeview_edges.get_selection()

        def execute_action(event, action):
            action()

        if not self.menu:
            self.menu = gtk.Menu()
            self.menu_add_edge = gtk.MenuItem(_("_Add edge"))
            self.menu_remove_edge = gtk.MenuItem(_("_Remove edge"))
            self.menu_edit_edge = gtk.MenuItem(_("_Edit edge settings"))

            self.menu_add_edge.connect("activate", execute_action, self.add_edge)
            self.menu_remove_edge.connect("activate", execute_action, self.remove_edge)
            self.menu_edit_edge.connect("activate", execute_action, self.edit_edge)

            self.menu.append(self.menu_add_edge)
            self.menu.append(self.menu_remove_edge)
            self.menu.append(self.menu_edit_edge)

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

        self.menu.show_all()
        self.menu.popup(None, None, None, event.button, event.time)

    def edit_edge(self):
        selection = self.treeview_edges.get_selection()
        store, rows = selection.get_selected_rows()

        row_iter = store.get_iter(rows[0])
        edge_id = store.get_value(row_iter, 0)
        
        edge = self.graph.find_edge_from_vertex(self.vertex, edge_id)
        if edge:
            edit_edge = EdgeEdit(self.graph_show, edge)
        
    def add_edge(self):
        idx = 0
        
        if self.vertex.id == 0:
            idx = len(self.graph.vertices) - 1
            
        vertex = self.graph.find(idx)
            
        if vertex:
            edge = self.controller.add_edge(self.graph, self.vertex, vertex)

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
                self.controller.remove_edge(self.graph, edge)
    
        self.add_state()
        self.area.queue_draw()

    def cairo_to_spin(self, color):
        return gtk.gdk.Color(color[0] * 65535, color[1] * 65535, color[2] * 65535)
        
    def spin_to_cairo(self, color):
        return [color.red / 65535.0, color.green / 65535.0, color.blue / 65535.0]

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
        self.vertex.fill_color = self.spin_to_cairo(widget.get_color())
        self.area.queue_draw()
        self.set_changed(True)
        
    def color_border_changed(self, widget):
        self.vertex.border_color = self.spin_to_cairo(widget.get_color())
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


from gtk import DrawingArea, EventBox, ScrolledWindow
from app.models.graph import Graph
from app.controllers.graphs_controller import GraphsController
from app.helpers.graph_helper import *
from app.views.gtk.graph.area import GraphArea
#from app.views.gtk.vertex.edit import VertexEdit
import gtk
import math

# TODO - Add scrollbars to graph
# TODO - (BUG) When one vertex (that have more than 2 edges with another vertex) is moved until the left top we have a float division by zero.

class GraphShow(ScrolledWindow):
    def __init__(self, changed_method):
        ScrolledWindow.__init__(self)

        self.event_box = EventBox()

        self.event_box.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.event_box.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.event_box.add_events(gtk.gdk.MOTION_NOTIFY)
        self.event_box.add_events(gtk.gdk.BUTTON1_MOTION_MASK)
        self.event_box.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.event_box.set_events(gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK)

        self.event_box.connect('button-press-event', self.mouse_press)
        self.event_box.connect('button-release-event', self.mouse_release)
        self.event_box.connect('motion-notify-event', self.mouse_motion)

        self.action = None
        self.menu = None

        self.last_vertex_clicked = None
        self.last_position_clicked = None

        self.changed = False
        self.changed_method = changed_method

        self.controller = GraphsController()

        self.graph = Graph()
        self.area = GraphArea(self.graph, self.controller)
        self.add_with_viewport(self.event_box)
        self.event_box.add(self.area)

    def centralize(self):
        w, h = self.area.get_size_request()
#        self.get_vscrollbar().set_range(2, w)

#IMPOSSIVEL.. PERDEMOS..
#VAMOS TROCAR DE TEMA DO TG..

#        self.get_vscrollbar().set_value(w / 2)
#        self.get_hscrollbar().set_value(h / 2)

#        print w / 2, h / 2
#        print self.get_vscrollbar().get_value(), self.get_hscrollbar().get_value()
        self.area.queue_draw()

    def set_changed(self, value):
        if self.changed != value:
            self.changed = value
            self.changed_method(self)

    def add_vertex(self):
        self.controller.add_vertex(self.graph, self.last_position_clicked)
        self.action = None
        self.area.queue_draw()

    def remove_vertex(self):
        for vertex in self.graph.selected_vertices():
            self.controller.remove_vertex(self.graph, vertex)

        self.action = None
        self.area.queue_draw()

    def add_edge(self):
        if len(self.graph.selected_vertices()) == 1:
            vertex = self.graph.find_by_position(self.last_position_clicked)

            if vertex != None:
                self.controller.add_edge(self.graph, self.graph.selected_vertices()[0], vertex)
                self.controller.deselect_vertex(self.graph, self.graph.selected_vertices()[0])
                self.action = None
                self.area.queue_draw()
                return True

        if len(self.graph.selected_vertices()) > 1:
            # TODO - Check if the edges are birectionals or dont
            for vertex1 in self.graph.selected_vertices():
                for vertex2 in self.graph.selected_vertices():
                    if vertex1 != vertex2:
                        self.controller.add_edge(self.graph, vertex1, vertex2)

            self.controller.clear_selection(self.graph)
            self.action = None
            self.area.queue_draw()
            return True

        return False

    def remove_edge(self):
        # TODO - Handle multiple edges
        if len(self.graph.selected_vertices()) == 1:
            vertex = self.graph.find_by_position(self.last_position_clicked)

            if vertex != None:
                edge = self.graph.find_edge(self.graph.selected_vertices()[0], vertex)
                self.controller.remove_edge(self.graph, edge[0])
                self.controller.deselect_vertex(self.graph, self.graph.selected_vertices()[0])
                self.action = None
                self.area.queue_draw()
                return True

        elif len(self.graph.selected_vertices()) > 1:
            for vertex1 in self.graph.selected_vertices():
                for vertex2 in self.graph.selected_vertices():
                    if vertex1 != vertex2:
                        edge = self.graph.find_edge(vertex1, vertex2)
                        self.controller.remove_edge(self.graph, edge[0])

            self.controller.clear_selection(self.graph)
            self.action = None
            self.area.queue_draw()
            return True

        return False

    def select_vertex(self, event):
        vertex = self.graph.find_by_position(self.last_position_clicked)

        from gtk.gdk import CONTROL_MASK, SHIFT_MASK

        if not (event.state & CONTROL_MASK or event.state & SHIFT_MASK) and (len(self.graph.selected_vertices()) > 0):
            if not vertex or not vertex.selected:
                self.controller.clear_selection(self.graph)

        if vertex:
            if vertex.selected and (event.state & CONTROL_MASK or event.state & SHIFT_MASK):
                self.controller.deselect_vertex(self.graph, vertex)
            else:
                self.controller.select_vertex(self.graph, vertex)

            self.last_vertex_clicked = vertex
        else:
            self.controller.clear_selection(self.graph)

    def mouse_press(self, widget, event):
        self.last_position_clicked = event.get_coords()

        if event.button == 1:
            if self.action != None:
                self.set_changed(True)
            if self.action == None:
                self.select_vertex(event)
            elif self.action == "add_vertex":
                self.add_vertex()
            elif self.action == "remove_vertex":
                self.remove_vertex()
            elif self.action == "add_edge":
                if not self.add_edge():
                    self.select_vertex(event)
            elif self.action == "remove_edge":
                if not self.remove_edge():
                    self.select_vertex(event)
        elif event.button == 2:
            pass
        elif event.button == 3:
            self.open_settings(event)

        self.area.queue_draw()
        self.mouse_motion(widget, event)

    def open_settings(self, event):
        vertex = self.graph.find_by_position(self.last_position_clicked)

        if not self.menu:
            self.menu = gtk.Menu()
            self.menu_add_edge = gtk.MenuItem(_("_Add edge"))
            self.menu_remove_edge = gtk.MenuItem(_("_Remove edge"))
            self.menu_add_vertex = gtk.MenuItem(_("_Add vertex"))
            self.menu_remove_vertex = gtk.MenuItem(_("_Remove vertex"))
            self.menu_edit_vertex = gtk.MenuItem(_("_Edit vertex settings"))
            self.menu_edit_edge = gtk.MenuItem(_("_Edit edge settings"))

            self.menu_add_edge.connect("activate", lambda event: self.add_edge())
            self.menu_remove_edge.connect("activate", lambda event: self.remove_edge())
            self.menu_add_vertex.connect("activate", lambda event: self.add_vertex())
            self.menu_remove_vertex.connect("activate", lambda event: self.remove_vertex())
#            self.menu_edit_vertex.connect("activate", )
#            self.menu_edit_edge.connect("activate", )

            self.menu.append(self.menu_add_vertex)
            self.menu.append(self.menu_remove_vertex)
            self.menu.append(gtk.SeparatorMenuItem())
            self.menu.append(self.menu_add_edge)
            self.menu.append(self.menu_remove_edge)
            self.menu.append(gtk.SeparatorMenuItem())
            self.menu.append(self.menu_edit_vertex)
            self.menu.append(self.menu_edit_edge)

        if vertex:
            self.select_vertex(event)
            self.menu_add_vertex.set_sensitive(False)
            self.menu_edit_edge.set_sensitive(False)
        else:
            self.menu_add_vertex.set_sensitive(True)
            self.menu_edit_edge.set_sensitive(True)

        self.menu.show_all()
        self.menu.popup(None, None, None, event.button, event.time)

    def mouse_release(self, widget, event):
        self.last_vertex_clicked = None

    def mouse_motion(self, widget, event):
        selected_vertices = self.graph.selected_vertices()

        if self.action == "add_edge" and len(selected_vertices) == 1:
            start = selected_vertices[0].position
            end = event.get_coords()
            self.area.adding_edge = (start, end)
            self.area.queue_draw()
        else:
            self.area.adding_edge = None

        if len(selected_vertices) > 0 and self.last_vertex_clicked:
            end_position = event.get_coords()
            start_position = self.last_vertex_clicked.position

            delta_x = end_position[0] - start_position[0]
            delta_y = end_position[1] - start_position[1]

            self.set_changed(True)

            for vertex in selected_vertices:
                new_position = [vertex.position[0] + delta_x, vertex.position[1] + delta_y]
                vertex.position = new_position

            self.area.queue_draw()


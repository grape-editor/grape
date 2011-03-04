from gtk import DrawingArea, EventBox
from app.models.graph import Graph
from app.controllers.graphs_controller import GraphsController
from app.helpers.graph_helper import *
from app.views.gtk.graph.area import GraphArea
import gtk
import math

# TODO - Add scrollbars to graph

class GraphShow(EventBox):
    def __init__(self, changed_method):
        EventBox.__init__(self)

        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.MOTION_NOTIFY)
        self.add_events(gtk.gdk.BUTTON1_MOTION_MASK)
        self.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.set_events(gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK)

        self.connect('button-press-event', self.mouse_press)
        self.connect('button-release-event', self.mouse_release)
        self.connect('motion-notify-event', self.mouse_motion)

        self.action = None

        self.last_clicked = None
        self.changed = False
        self.changed_method = changed_method

        self.controller = GraphsController()

        self.graph = Graph()
        self.area = GraphArea(self.graph, self.controller)
        self.add(self.area)

    def set_changed(self, value):
        if self.changed != value:
            self.changed = value
            self.changed_method(self)

    def add_vertex(self, event):
        position = event.get_coords()
        self.controller.add_vertex(self.graph, position)
        self.action = None

    def remove_vertex(self, event):
        position = event.get_coords()
        vertex = self.graph.find_by_position(position)
        self.controller.remove_vertex(self.graph, vertex)
        self.action = None

    def add_edge(self, event):
        if len(self.graph.selected_vertices()) == 1:
            position = event.get_coords()
            vertex = self.graph.find_by_position(position)

            if vertex != None:
                self.controller.add_edge(self.graph, self.graph.selected_vertices()[0], vertex)
                self.controller.deselect_vertex(self.graph, self.graph.selected_vertices()[0])
                self.action = None

                return True
        else:
            self.select_vertex(event)

        return False

    def remove_edge(self, event):
        if len(self.graph.selected_vertices()) == 1:
            position = event.get_coords()
            vertex = self.graph.find_by_position(position)

            if vertex != None:
                # TODO - Handle multiple edges
                edge = self.graph.find_edge(self.graph.selected_vertices()[0], vertex)
                self.controller.remove_edge(self.graph, edge[0])
                self.controller.deselect_vertex(self.graph, self.graph.selected_vertices()[0])
                self.action = None

                return True
        else:
            self.select_vertex(event)

        return False

    def select_vertex(self, event):
        position = event.get_coords()
        vertex = self.graph.find_by_position(position)

        from gtk.gdk import CONTROL_MASK, SHIFT_MASK

        if not (event.state & CONTROL_MASK or event.state & SHIFT_MASK) and (len(self.graph.selected_vertices()) > 0):
            if not vertex or not vertex.selected:
                self.controller.clear_selection(self.graph)

        if vertex:
            if vertex.selected and (event.state & CONTROL_MASK or event.state & SHIFT_MASK):
                self.controller.deselect_vertex(self.graph, vertex)
            else:
                self.controller.select_vertex(self.graph, vertex)

            self.last_clicked = vertex
        else:
            self.controller.clear_selection(self.graph)

    def mouse_press(self, widget, event):
        if self.action != None:
            self.set_changed(True)
        if self.action == None:
            self.select_vertex(event)
        elif self.action == "add_vertex":
            self.add_vertex(event)
        elif self.action == "remove_vertex":
            self.remove_vertex(event)
        elif self.action == "add_edge":
            self.add_edge(event)
        elif self.action == "remove_edge":
            self.remove_edge(event)

        self.area.draw()

    def mouse_release(self, widget, event):
        self.last_clicked = None

    def mouse_motion(self, widget, event):
        selected_vertices = self.graph.selected_vertices()

        if self.action == "add_edge" and len(selected_vertices) == 1:
            start = selected_vertices[0].position
            end = event.get_coords()
            self.area.adding_edge = (start, end)
            self.area.queue_draw()
        else:
            self.area.adding_edge = None

        if len(selected_vertices) > 0 and self.last_clicked:
            end_position = event.get_coords()
            start_position = self.last_clicked.position

            delta_x = end_position[0] - start_position[0]
            delta_y = end_position[1] - start_position[1]

            self.set_changed(True)

            for vertex in selected_vertices:
                new_position = [vertex.position[0] + delta_x, vertex.position[1] + delta_y]
                vertex.position = new_position

            self.area.queue_draw()


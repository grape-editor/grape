import gtk
import math
import pickle
from gtk import DrawingArea, EventBox, ScrolledWindow

from lib.graph import Graph as GraphModel
from lib.graphs_controller import GraphsController
from lib.mathemathical import *
from gui.area import GraphArea
from gui.scrollable_graph import ScrollableGraph
from gui.vertex import Vertex

class Graph(ScrollableGraph):

    def __init__(self, builder, changed_method):
        ScrollableGraph.__init__(self)
        
        self.builder = builder

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
        self.event_box.connect('scroll-event', self.mouse_scroll)

        self.action = None
        self.menu = None

        self.box = None

        self.last_vertex_clicked = None
        self.last_position_clicked = None

        self.box_selecting = None

        self.changed = False
        self.changed_method = changed_method

        self.controller = GraphsController()

        self.graph = GraphModel()
        self.area = GraphArea(self.graph, self.controller)
        self.event_box.add(self.area)

        self.states= []
        self.state_index = None
        self.add_state()

        self.viewport = gtk.Viewport()
        self.viewport.add(self.event_box)

        self.add_scrollable_widget(self.viewport)

    def zoom_in(self, center=None):
        if self.area.zoom < 20:
            self.area.zoom *= 1.1
        self.do_zoom(center)

    def zoom_out(self, center=None):
        if self.area.zoom > 0.1:
            self.area.zoom /= 1.1
        self.do_zoom(center)

    def zoom_default(self):
        self.area.zoom = 1
        self.do_zoom()

    def do_zoom(self, center=None):
        w, h = self.area.get_size_request()
        w *= self.area.zoom
        h *= self.area.zoom

        x = w * self.hadjustment.value / self.hadjustment.upper
        y = h * self.vadjustment.value / self.vadjustment.upper

        self.hadjustment.upper = w
        self.vadjustment.upper = h

        self.hadjustment.value = x
        self.vadjustment.value = y

        self.area.queue_draw()

    def mouse_scroll(self, widget, event):
        if not (event.state & gtk.gdk.CONTROL_MASK):
            return

        center = map(lambda v: v / self.area.zoom,event.get_coords())

        if event.direction == gtk.gdk.SCROLL_UP:
            self.zoom_in(center)
        else:
            self.zoom_out(center)

    def set_changed(self, value):
        if self.changed != value:
            self.changed = value
            self.changed_method(self)

    def add_vertex(self):
        self.controller.add_vertex(self.graph, self.last_position_clicked)
        self.add_state()
        self.action = None
        self.area.queue_draw()

    def remove_vertex(self):
        to_be_removed = list(self.graph.selected_vertices())
        map(lambda vertex: self.controller.remove_vertex(self.graph, vertex), to_be_removed)
        self.add_state()

        self.action = None
        self.area.queue_draw()

    def edit_vertex(self):
        if len(self.graph.selected_vertices()) == 1:
            vertex = self.graph.selected_vertices()[0]
            self.controller.deselect_vertex(self.graph, vertex)
            vertex_edit = VertexEdit(self, vertex)

    def add_edge(self):
        if len(self.graph.selected_vertices()) == 1:
            vertex = self.graph.find_by_position(self.last_position_clicked)

            if vertex != None and vertex != self.graph.selected_vertices()[0]:
                self.controller.add_edge(self.graph, self.graph.selected_vertices()[0], vertex)
                self.controller.deselect_vertex(self.graph, self.graph.selected_vertices()[0])
                self.add_state()
                self.action = None
                self.area.queue_draw()
                return True

        if len(self.graph.selected_vertices()) > 1:
            for i in range(len(self.graph.selected_vertices())):
                for j in range(i, len(self.graph.selected_vertices())):
                    vertex1 = self.graph.selected_vertices()[i]
                    vertex2 = self.graph.selected_vertices()[j]
                    
                    if vertex1 != vertex2:
                        self.controller.add_edge(self.graph, vertex1, vertex2)
    
                        if self.graph.directed:
                            self.controller.add_edge(self.graph, vertex2, vertex1)

            selected_vertices = list(self.graph.selected_vertices())
            if len(selected_vertices):
                self.controller.clear_selection(self.graph)
                self.add_state()
                for vertex in selected_vertices:
                    self.controller.select_vertex(self.graph, vertex)

            self.action = None
            self.area.queue_draw()

            return True

        self.action = "add_edge"
        return False

    def remove_edge(self):
        # TODO - Handle multiple edges
        if len(self.graph.selected_vertices()) == 1:
            vertex = self.graph.find_by_position(self.last_position_clicked)

            if vertex != None:
                edge = self.graph.find_edge(self.graph.selected_vertices()[0], vertex)
                if len(edge) > 0:
                    self.controller.remove_edge(self.graph, edge[0])
                    self.controller.deselect_vertex(self.graph, self.graph.selected_vertices()[0])
                    self.add_state()
                    self.action = None
                    self.area.queue_draw()
                return True

        elif len(self.graph.selected_vertices()) > 1:
            for vertex1 in self.graph.selected_vertices():
                for vertex2 in self.graph.selected_vertices():
                    if vertex1 != vertex2:
                        edge = self.graph.find_edge(vertex1, vertex2)
                        if len(edge) > 0:
                            self.controller.remove_edge(self.graph, edge[0])

            self.controller.clear_selection(self.graph)
            self.add_state()
            self.action = None
            self.area.queue_draw()
            return True

        return False

    def edit_edge(self):
        pass

    def select_area(self, event, area):
        if not area: return

        x, y, w, h = area
        vertices = self.graph.find_in_area(x, y, w, h)

        from gtk.gdk import CONTROL_MASK, SHIFT_MASK

        if not (event.state & CONTROL_MASK or event.state & SHIFT_MASK):
            self.controller.clear_selection(self.graph)

        method = self.controller.select_vertex

        if (event.state & CONTROL_MASK):
            method = self.controller.toggle_vertex_selection

        map(lambda vertex: method(self.graph, vertex), vertices)

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
            self.box_selecting = self.last_position_clicked
            self.action = None

    def add_state(self):
        import pickle
        state = pickle.dumps(self.graph)
        
        if not self.state_index:
            self.state_index = 0            

        if (self.state_index < len(self.states) - 1):
            self.states = self.states[:self.state_index + 1]

        self.states.append(state)

        if len(self.states) == 1:
            self.state_index = 0
        else:
            self.state_index += 1

    def prev_state(self):
        import pickle
        if (self.state_index > 0 and len(self.states) > 0):
            self.state_index -= 1
            graph = self.states[self.state_index]
            state = pickle.loads(graph)
            return state
        return None

    def next_state(self):
        import pickle
        if (self.state_index < len(self.states) - 1):
            self.state_index += 1
            graph = self.states[self.state_index]
            state = pickle.loads(graph)
            return state
        return None

    def undo(self):     
        graph = self.prev_state()
        if graph:        
            graph.path = self.graph.path
            graph.title = self.graph.title
            
            self.area.graph = graph
            self.graph = graph
            self.set_changed(True)
            
        self.queue_draw()

    def redo(self):
        graph = self.next_state()
        if graph:            
            self.area.graph = graph
            self.graph = graph
            self.set_changed(True)
            
        self.queue_draw()

    def mouse_press(self, widget, event):
        self.last_position_clicked = map(lambda v: v / self.area.zoom,event.get_coords())

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
            self.right_click_menu(event)

        self.area.queue_draw()
        self.mouse_motion(widget, event)

    def right_click_menu(self, event):
        vertex = self.graph.find_by_position(self.last_position_clicked)

        if len(self.graph.selected_vertices()) == 0 and vertex:
            self.controller.select_vertex(self.graph, vertex)

        def execute_action(event, action):
            action()

        if not self.menu:
            self.menu = gtk.Menu()
            self.menu_add_edge = gtk.MenuItem(_("_Add edge"))
            self.menu_remove_edge = gtk.MenuItem(_("_Remove edge"))
            self.menu_add_vertex = gtk.MenuItem(_("_Add vertex"))
            self.menu_remove_vertex = gtk.MenuItem(_("_Remove vertex"))
            self.menu_edit_vertex = gtk.MenuItem(_("_Edit vertex settings"))
            self.menu_edit_edge = gtk.MenuItem(_("_Edit edge settings"))

            self.menu_add_edge.connect("activate", execute_action, self.add_edge)
            self.menu_remove_edge.connect("activate", execute_action, self.remove_edge)
            self.menu_add_vertex.connect("activate", execute_action, self.add_vertex)
            self.menu_remove_vertex.connect("activate", execute_action, self.remove_vertex)
            self.menu_edit_vertex.connect("activate", execute_action, self.edit_vertex)
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
            self.menu_add_vertex.set_sensitive(False)
            self.menu_edit_vertex.set_sensitive(True)
            self.menu_remove_vertex.set_sensitive(True)
            self.menu_add_edge.set_sensitive(True)
            self.menu_remove_edge.set_sensitive(True)
            self.menu_edit_edge.set_sensitive(False)
        else:
            self.menu_add_vertex.set_sensitive(True)
            self.menu_edit_vertex.set_sensitive(False)
            self.menu_remove_vertex.set_sensitive(False)
            self.menu_add_edge.set_sensitive(len(self.graph.selected_vertices()) > 0)
            self.menu_remove_edge.set_sensitive(False)
            self.menu_edit_edge.set_sensitive(False)

        self.menu.show_all()
        self.menu.popup(None, None, None, event.button, event.time)

    def mouse_release(self, widget, event):
        selected_vertices = list(self.graph.selected_vertices())

        if len(selected_vertices) > 0 and self.last_vertex_clicked:
            self.controller.clear_selection(self.graph)
            self.add_state()
            for vertex in selected_vertices:
                self.controller.select_vertex(self.graph, vertex)
       
        self.last_vertex_clicked = None
        self.box_selecting = None
        self.select_area(event, self.area.selected_area)
        self.area.selected_area = None
        self.area.queue_draw()

    def mouse_motion(self, widget, event):
        coords = map(lambda v: v / self.area.zoom,event.get_coords())

        if self.box_selecting:
            x, y = self.box_selecting
            w, h = [e - s for e, s in zip(coords, self.box_selecting)]
            self.area.selected_area = (x, y, w, h)
            self.area.queue_draw()
            return

        selected_vertices = self.graph.selected_vertices()

        if self.action == "add_edge" and len(selected_vertices) == 1:
            start = selected_vertices[0].position
            end = coords
            self.area.adding_edge = (start, end)
            self.area.queue_draw()
        else:
            self.area.adding_edge = None

        if len(selected_vertices) > 0 and self.last_vertex_clicked:
            end_position = coords
            start_position = self.last_vertex_clicked.position

            delta_x = end_position[0] - start_position[0]
            delta_y = end_position[1] - start_position[1]

            self.set_changed(True)

            for vertex in selected_vertices:
                new_position = [vertex.position[0] + delta_x, vertex.position[1] + delta_y]
                vertex.position = new_position

            self.area.queue_draw()


import gtk
import math
import pickle
from gtk import DrawingArea, EventBox, ScrolledWindow

from lib.graph import Graph as GraphController
from lib.mathemathical import *
from gui.area import GraphArea
from gui.vertex import Vertex

class Graph(gtk.ScrolledWindow):
    def __init__(self, changed_method):
        gtk.ScrolledWindow.__init__(self)

#        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.builder = gtk.Builder()
        self.event_box = EventBox()

        self.event_box.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.event_box.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.event_box.add_events(gtk.gdk.MOTION_NOTIFY)
        self.event_box.add_events(gtk.gdk.BUTTON1_MOTION_MASK)
        self.event_box.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.event_box.set_events(gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK)

        self.event_box.connect('motion-notify-event', self.mouse_motion)
        self.event_box.connect('button-press-event', self.mouse_press)
        self.event_box.connect('button-release-event', self.mouse_release)
        self.event_box.connect('scroll-event', self.mouse_scroll)

        self.action = None
        self.menu = None
        self.box = None
        self.last_vertex_clicked = None
        self.last_position_clicked = None
        self.box_selecting = None
        self.changed = False

        self.changed_method = changed_method

        self.graph = GraphController()
        self.area = GraphArea(self.graph)

        self.event_box.add(self.area)
        self.add_with_viewport(self.event_box)
        
        self.area.show()
        self.event_box.show()
        self.show()

        # To UNDO and REDO actions
        self.states= []
        self.state_index = None
        self.add_state()

        # Algorithm stuff
        self.algorithm_runner = None
        self.algorithm_states = []

    def centralize_scroll(self, position=None):
        """Put both scrolls in center"""
        vadj = self.get_vadjustment()
        hadj = self.get_hadjustment()

        if not position:
            position = [(vadj.upper / 2), (hadj.upper / 2)]

        print map(lambda x: int(x), position)
        hadj.set_value(position[0] - (hadj.page_size / 2))
        vadj.set_value(position[1] - (vadj.page_size / 2))

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
        width, height = self.area.get_size_request()
        vadj = self.get_vadjustment()
        hadj = self.get_hadjustment()

        width *= self.area.zoom
        height *= self.area.zoom


        if not center:
            x = (hadj.get_value() + hadj.get_page_size() / 2) / self.area.zoom
            y = (vadj.get_value() + vadj.get_page_size() / 2) / self.area.zoom
            center = [x, y]

        hadj.set_upper(width)
        vadj.set_upper(height)


        self.centralize_scroll(center)
#        vadj.set_value(self.area.zoom * hadj.value)
#        hadj.set_value(self.area.zoom * vadj.value)

        self.area.queue_draw()

    def mouse_scroll(self, widget, event):
        width, height = self.area.get_size_request()
        vadj = self.get_vadjustment()
        hadj = self.get_hadjustment()

        print int(vadj.value), int(vadj.upper), int(vadj.page_size)
        print int(hadj.value), int(hadj.upper), int(hadj.page_size)
        print int(width), int(height)

        if not (event.state & gtk.gdk.CONTROL_MASK):
            return

        center = map(lambda v: v / self.area.zoom, event.get_coords())

        if event.direction == gtk.gdk.SCROLL_UP:
            self.zoom_in(center)
        elif event.direction == gtk.gdk.SCROLL_DOWN:
            self.zoom_out(center)

        width, height = self.area.get_size_request()
        vadj = self.get_vadjustment()
        hadj = self.get_hadjustment()

        print int(vadj.value), int(vadj.upper), int(vadj.page_size)
        print int(hadj.value), int(hadj.upper), int(hadj.page_size)

    def set_changed(self, value):
        if self.changed != value:
            self.changed = value
            self.changed_method(self)

    def add_vertex(self):
        self.graph.add_vertex(self.last_position_clicked)
        self.add_state()
        self.action = None
        self.area.queue_draw()

    def remove_vertex(self):
        to_be_removed = list(self.graph.selected_vertices())
        map(lambda vertex: self.graph.remove_vertex(vertex), to_be_removed)
        self.add_state()

        self.action = None
        self.area.queue_draw()

    def edit_vertex(self):
        if len(self.graph.selected_vertices()) == 1:
            vertex = self.graph.selected_vertices()[0]
            self.graph.deselect_vertex(vertex)
            vertex_edit = Vertex(self, vertex)

    def add_edge(self):
        if len(self.graph.selected_vertices()) == 1:
            vertex = self.graph.find_by_position(self.last_position_clicked)

            if vertex != None and vertex != self.graph.selected_vertices()[0]:
                self.graph.add_edge(self.graph.selected_vertices()[0], vertex)
                self.graph.deselect_vertex(self.graph.selected_vertices()[0])
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
                        self.graph.add_edge(vertex1, vertex2)
    
                        if self.graph.directed:
                            self.graph.add_edge(vertex2, vertex1)

            selected_vertices = list(self.graph.selected_vertices())
            if len(selected_vertices):
                self.graph.clear_selection()
                self.add_state()
                for vertex in selected_vertices:
                    self.graph.select_vertex(vertex)

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
                    self.graph.remove_edge(edge[0])
                    self.graph.deselect_vertex(self.graph.selected_vertices()[0])
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
                            self.graph.remove_edge(edge[0])

            self.graph.clear_selection()
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
            self.graph.clear_selection()
        method = self.graph.select_vertex
        if (event.state & CONTROL_MASK):
            method = self.graph.toggle_vertex_selection
        map(lambda vertex: method(vertex), vertices)

    def select_vertex(self, event):
        vertex = self.graph.find_by_position(self.last_position_clicked)

        from gtk.gdk import CONTROL_MASK, SHIFT_MASK
        if not (event.state & CONTROL_MASK or event.state & SHIFT_MASK) and (len(self.graph.selected_vertices()) > 0):
            if not vertex or not vertex.selected:
                self.graph.clear_selection()
        if vertex:
            if vertex.selected and (event.state & CONTROL_MASK or event.state & SHIFT_MASK):
                self.graph.deselect_vertex(vertex)
            else:
                self.graph.select_vertex(vertex)
            self.last_vertex_clicked = vertex
        else:
            self.box_selecting = self.last_position_clicked
            self.action = None

    def algorithm_play(self, Algorithm):
        if self.algorithm_runner:
                self.algorithm_runner.stop()
        self.algorithm_runner = Algorithm(self.graph)
        self.algorithm_runner.play()
        self.queue_draw()
        
    def algorithm_next(self):
        if self.algorithm_runner:
            self.algorithm_runner.next()
            self.queue_draw()

    def algorithm_prev(self):
        if self.algorithm_runner:
            self.algorithm_runner.prev()
            self.queue_draw()

    def algorithm_stop(self):
        if self.algorithm_runner:
            self.algorithm_runner.stop()
            self.algorithm_runner = None
            self.queue_draw()

    def add_state(self):
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
        if (self.state_index > 0 and len(self.states) > 0):
            self.state_index -= 1
            graph = self.states[self.state_index]
            state = pickle.loads(graph)
            return state
        return None

    def next_state(self):
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
        print event.get_coords()
        self.last_position_clicked = map(lambda v: v / self.area.zoom, event.get_coords())

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
            self.graph.select_vertex(vertex)

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
            self.graph.clear_selection()
            self.add_state()
            for vertex in selected_vertices:
                self.graph.select_vertex(vertex)
       
        self.last_vertex_clicked = None
        self.box_selecting = None
        self.select_area(event, self.area.selected_area)
        self.area.selected_area = None
        self.area.queue_draw()

    def mouse_motion(self, widget, event):
        coords = map(lambda v: v / self.area.zoom, event.get_coords())

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


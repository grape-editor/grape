import gtk
import math
import pickle
from gtk import DrawingArea, EventBox, ScrolledWindow

from app.models.graph import Graph
from app.controllers.graphs_controller import GraphsController
from app.helpers.graph_helper import *
from app.views.gtk.graph.area import GraphArea
from app.views.gtk.graph.scrollable_graph import ScrollableGraph
from app.views.gtk.node.edit import NodeEdit

class GraphShow(ScrollableGraph):

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

        self.last_node_clicked = None
        self.last_position_clicked = None

        self.box_selecting = None

        self.changed = False
        self.changed_method = changed_method

        self.controller = GraphsController()

        self.graph = Graph()
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

        center = map(lambda node: node / self.area.zoom,event.get_coords())

        if event.direction == gtk.gdk.SCROLL_UP:
            self.zoom_in(center)
        else:
            self.zoom_out(center)

    def set_changed(self, value):
        if self.changed != value:
            self.changed = value
            self.changed_method(self)

    def add_node(self):
        self.controller.add_node(self.graph, self.last_position_clicked)
        self.add_state()
        self.action = None
        self.area.queue_draw()

    def remove_node(self):
        to_be_removed = list(self.graph.selected_nodes())
        map(lambda node: self.controller.remove_node(self.graph, node), to_be_removed)
        self.add_state()

        self.action = None
        self.area.queue_draw()

    def edit_node(self):
        if len(self.graph.selected_nodes()) == 1:
            node = self.graph.selected_nodes()[0]
            self.controller.deselect_node(self.graph, node)
            node_edit = NodeEdit(self, node)

    def add_edge(self):
        if len(self.graph.selected_nodes()) == 1:
            node = self.graph.find_by_position(self.last_position_clicked)

            if node != None and node != self.graph.selected_nodes()[0]:
                self.controller.add_edge(self.graph, self.graph.selected_nodes()[0], node)
                self.controller.deselect_node(self.graph, self.graph.selected_nodes()[0])
                self.add_state()
                self.action = None
                self.area.queue_draw()
                return True

        if len(self.graph.selected_nodes()) > 1:
            for i in range(len(self.graph.selected_nodes())):
                for j in range(i, len(self.graph.selected_nodes())):
                    node1 = self.graph.selected_nodes()[i]
                    node2 = self.graph.selected_nodes()[j]
                    
                    if node1 != node2:
                        self.controller.add_edge(self.graph, node1, node2)
    
                        if self.graph.directed:
                            self.controller.add_edge(self.graph, node2, node1)

            selected_nodes = list(self.graph.selected_nodes())
            if len(selected_nodes):
                self.controller.clear_selection(self.graph)
                self.add_state()
                for node in selected_nodes:
                    self.controller.select_node(self.graph, node)

            self.action = None
            self.area.queue_draw()

            return True

        self.action = "add_edge"
        return False

    def remove_edge(self):
        # TODO - Handle multiple edges
        if len(self.graph.selected_nodes()) == 1:
            node = self.graph.find_by_position(self.last_position_clicked)

            if node != None:
                edge = self.graph.find_edge(self.graph.selected_nodes()[0], node)
                if len(edge) > 0:
                    self.controller.remove_edge(self.graph, edge[0])
                    self.controller.deselect_node(self.graph, self.graph.selected_nodes()[0])
                    self.add_state()
                    self.action = None
                    self.area.queue_draw()
                return True

        elif len(self.graph.selected_nodes()) > 1:
            for node1 in self.graph.selected_nodes():
                for node2 in self.graph.selected_nodes():
                    if node1 != node2:
                        edge = self.graph.find_edge(node1, node2)
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
        nodes = self.graph.find_in_area(x, y, w, h)

        from gtk.gdk import CONTROL_MASK, SHIFT_MASK

        if not (event.state & CONTROL_MASK or event.state & SHIFT_MASK):
            self.controller.clear_selection(self.graph)

        method = self.controller.select_node

        if (event.state & CONTROL_MASK):
            method = self.controller.toggle_node_selection

        map(lambda node: method(self.graph, node), nodes)

    def select_node(self, event):
        node = self.graph.find_by_position(self.last_position_clicked)

        from gtk.gdk import CONTROL_MASK, SHIFT_MASK

        if not (event.state & CONTROL_MASK or event.state & SHIFT_MASK) and (len(self.graph.selected_nodes()) > 0):
            if not node or not node.selected:
                self.controller.clear_selection(self.graph)

        if node:
            if node.selected and (event.state & CONTROL_MASK or event.state & SHIFT_MASK):
                self.controller.deselect_node(self.graph, node)
            else:
                self.controller.select_node(self.graph, node)
            self.last_node_clicked = node
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
        self.last_position_clicked = map(lambda node: node / self.area.zoom,event.get_coords())

        if event.button == 1:
            if self.action != None:
                self.set_changed(True)
            if self.action == None:
                self.select_node(event)
            elif self.action == "add_node":
                self.add_node()
            elif self.action == "remove_node":
                self.remove_node()
            elif self.action == "add_edge":
                if not self.add_edge():
                    self.select_node(event)
            elif self.action == "remove_edge":
                if not self.remove_edge():
                    self.select_node(event)
        elif event.button == 2:
            pass
        elif event.button == 3:
            self.right_click_menu(event)

        self.area.queue_draw()
        self.mouse_motion(widget, event)

    def right_click_menu(self, event):
        node = self.graph.find_by_position(self.last_position_clicked)

        if len(self.graph.selected_nodes()) == 0 and node:
            self.controller.select_node(self.graph, node)

        def execute_action(event, action):
            action()

        if not self.menu:
            self.menu = gtk.Menu()
            self.menu_add_edge = gtk.MenuItem(_("_Add edge"))
            self.menu_remove_edge = gtk.MenuItem(_("_Remove edge"))
            self.menu_add_node = gtk.MenuItem(_("_Add node"))
            self.menu_remove_node = gtk.MenuItem(_("_Remove node"))
            self.menu_edit_node = gtk.MenuItem(_("_Edit node settings"))
            self.menu_edit_edge = gtk.MenuItem(_("_Edit edge settings"))

            self.menu_add_edge.connect("activate", execute_action, self.add_edge)
            self.menu_remove_edge.connect("activate", execute_action, self.remove_edge)
            self.menu_add_node.connect("activate", execute_action, self.add_node)
            self.menu_remove_node.connect("activate", execute_action, self.remove_node)
            self.menu_edit_node.connect("activate", execute_action, self.edit_node)
#            self.menu_edit_edge.connect("activate", )

            self.menu.append(self.menu_add_node)
            self.menu.append(self.menu_remove_node)
            self.menu.append(gtk.SeparatorMenuItem())
            self.menu.append(self.menu_add_edge)
            self.menu.append(self.menu_remove_edge)
            self.menu.append(gtk.SeparatorMenuItem())
            self.menu.append(self.menu_edit_node)
            self.menu.append(self.menu_edit_edge)

        if node:
            self.menu_add_node.set_sensitive(False)
            self.menu_edit_node.set_sensitive(True)
            self.menu_remove_node.set_sensitive(True)
            self.menu_add_edge.set_sensitive(True)
            self.menu_remove_edge.set_sensitive(True)
            self.menu_edit_edge.set_sensitive(False)
        else:
            self.menu_add_node.set_sensitive(True)
            self.menu_edit_node.set_sensitive(False)
            self.menu_remove_node.set_sensitive(False)
            self.menu_add_edge.set_sensitive(len(self.graph.selected_nodes()) > 0)
            self.menu_remove_edge.set_sensitive(False)
            self.menu_edit_edge.set_sensitive(False)

        self.menu.show_all()
        self.menu.popup(None, None, None, event.button, event.time)

    def mouse_release(self, widget, event):
        selected_nodes = list(self.graph.selected_nodes())

        if len(selected_nodes) > 0 and self.last_node_clicked:
            self.controller.clear_selection(self.graph)
            self.add_state()
            for node in selected_nodes:
                self.controller.select_node(self.graph, node)
       
        self.last_node_clicked = None
        self.box_selecting = None
        self.select_area(event, self.area.selected_area)
        self.area.selected_area = None
        self.area.queue_draw()

    def mouse_motion(self, widget, event):
        coords = map(lambda node: node / self.area.zoom,event.get_coords())

        if self.box_selecting:
            x, y = self.box_selecting
            w, h = [e - s for e, s in zip(coords, self.box_selecting)]
            self.area.selected_area = (x, y, w, h)
            self.area.queue_draw()
            return

        selected_nodes = self.graph.selected_nodes()

        if self.action == "add_edge" and len(selected_nodes) == 1:
            start = selected_nodes[0].position
            end = coords
            self.area.adding_edge = (start, end)
            self.area.queue_draw()
        else:
            self.area.adding_edge = None

        if len(selected_nodes) > 0 and self.last_node_clicked:
            end_position = coords
            start_position = self.last_node_clicked.position

            delta_x = end_position[0] - start_position[0]
            delta_y = end_position[1] - start_position[1]

            self.set_changed(True)

            for node in selected_nodes:
                new_position = [node.position[0] + delta_x, node.position[1] + delta_y]
                node.position = new_position

            self.area.queue_draw()


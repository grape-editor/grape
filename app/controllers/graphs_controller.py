from app.controllers.action_controller import ActionController
from app.controllers.vertices_controller import VericesController
from app.controllers.edges_controller import EdgesController
from app.models.vertex import Vertex
from app.models.edge import Edge


class GraphsController(ActionController):

    def __init__(self):
        self.vertices_cotroller = VericesController()
        self.edges_controller = EdgesController()
        
    def add_vertex(self, graph, position):
        params = {'id': graph.vertex_id, 'title': str(graph.vertex_id)}
        vertex = self.vertices_controller.create(params)
        graph.vertices.append(vertex)
        graph.vertex_id += 1

        return vertex

    def remove_vertex(self, graph, vertex):
        if vertex:
            to_be_removed = list(vertex.touching_edges)
            map(lambda e: self.remove_edge(graph, e), to_be_removed)
            graph.vertices.remove(vertex)

    def add_edge(self, graph, start, end):
        edge = Edge(graph.edge_id, start, end, not graph.directed)
        graph.edges.append(edge)
        graph.edge_id += 1

        return edge

    def remove_edge(self, graph, edge):
        if not graph.has_edge(edge):
            return

        self.edges_controller.destroy(edge)

        graph.edges.remove(edge)

    def toggle_vertex_selection(self, graph, vertex):
        graph.selected_vertices_cache = None

        self.vertices_controller.toggle_selection(vertex)

    def select_all(self, graph):
        graph.selected_vertices_cache = None
        
        for vertex in graph.vertices:
            self.vertices_controller.select(vertex)

    def select_vertex(self, graph, vertex):
        graph.selected_vertices_cache = None
        self.vertices_controller.select(vertex)

    def deselect_vertex(self, graph, vertex):
        graph.selected_vertices_cache = None
        self.vertices_controller.deselect(vertex)

    def clear_selection(self, graph):
        if len(graph.selected_vertices()) > 0:
            selected_vertices = graph.selected_vertices()

            for vertex in selected_vertices:
                self.vertices_controller.deselect(vertex)

    def move_selection(self, graph, direction):
        selected = graph.selected_vertices()

        if len(selected) == 1:
            if direction == 'up':
                sort_index = 1
                slice = lambda arr, index: arr[:index - 1]
            elif direction == 'down':
                sort_index = 1
                slice = lambda arr, index: arr[index + 1:]
            elif direction == 'left':
                sort_index = 0
                slice = lambda arr, index: arr[:index - 1]
            elif direction == 'right':
                sort_index = 0
                slice = lambda arr, index: arr[index + 1:]
            else:
                return None

            ordered = sorted(graph.vertices, key=lambda vertex: vertex.position[sort_index])
            index = ordered.index(selected[0])
            ordered = slice(ordered, index)

            vertex = selected[0].nearest_vertices(ordered, int(not sort_index))

            if vertex:
                self.vertices_controller.deselect(selected[0])
                self.vertices_controller.select(vertex)

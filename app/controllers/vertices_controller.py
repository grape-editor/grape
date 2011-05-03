from app.controllers.action_controller import ActionController
from app.models.vertex import Vertex


class VertexController(ActionController):

    def create(self, params):
        vertex = Vertex(params)
        return vertex
        
    def toggle_selection(self, vertex):
        self.selected = not self.selected

    def select(self, graph, vertex):
        self.selected = True

    def deselect(self, graph, vertex):
        self.selected = False
        
    def add_edge(self, vertex, edge):
        if not vertex.has_edge(edge):
            vertex.adjacencies.append(edge)

    def remove_edge(self, vertex, edge):
        if vertex.has_edge(edge):
            if edge.start.touches_edge(edge):
                edge.start.touching_edges.remove(edge)

            if edge.end.touches_edge(edge):
                edge.end.touching_edges.remove(edge)

            vertex.adjacencies.remove(edge)

    def clear_adjacencies(self, vertex):
        for e in vertex.adjacencies:
            start = e.start
            end = e.end
            
            if start != vertex:
                self.remove_edge(start, e)
            if end != vertex:
                self.remove_edge(end, e)

        del(vertex.adjacencies[:])
        

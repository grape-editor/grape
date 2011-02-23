from app.models.vertex import Vertex
from app.models.edge import Edge

class GraphsController(object):
    def add_vertex(self, graph, position):
        vertex = Vertex(graph.vertex_id, position)
        graph.vertices.append(vertex)
        graph.vertex_id += 1
        
        return vertex

    def remove_vertex(self, graph, vertex):
        if vertex:
            vertex.clear_adjacencies()
            graph.vertices.remove(vertex)
            
    def add_edge(self, graph, start, end, bidirectional=True):
        edge = Edge(graph.edge_id, start, end, bidirectional)
        graph.edges.append(edge)
        graph.edge_id += 1
        
        return edge

    def remove_edge(self, graph, edge):
        # TODO - Figure out how to handle multiple edges
        edge.start.remove_edge(edge)

        if edge.bidirectional:
            edge.end.remove_edge(edge)

        graph.edges.remove(edge)
    
    def select_vertex(self, graph, vertex):
        graph.selected_vertices_cache = None
        vertex.select()
        
    def deselect_vertex(self, graph, vertex):
        graph.selected_vertices_cache = None
        vertex.deselect()
        
    def clear_selection(self, graph):
        if len(graph.selected_vertices()) > 0:
            selected_vertices = graph.selected_vertices()
            
            for vertex in selected_vertices:
                self.deselect_vertex(graph, vertex)
    
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
                self.deselect_vertex(graph, selected[0])
                self.select_vertex(graph, vertex)
            
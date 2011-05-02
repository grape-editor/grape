from app.models.active_model import ActiveModel


class Vertex(ActiveModel):

    def __init__(self, params):
        self.id = None
        self.position = [0 ,0]
        
        # TODO - Configuration file
        self.title = ""
        self.fill_color = [1, 1, 1]
        self.border_color = [0, 0, 0]
        self.border_size = 2
        self.size = 30
        
        self.adjacencies = []
        self.touching_edges = []
        
        self.selected = False

        ActiveModel.__init__(self, params)        
        
    def has_edge(self, edge):
        return edge in self.adjacencies

    def touches_edge(self, edge):
        return edge in self.touching_edges

    def nearest_vertices(self, neighbor, axis):
        next_vertex = None

        if len(neighbor) > 0:
            point_max = self.position[axis]
            point_min = self.position[axis]

            while not next_vertex:
                for current in neighbor:
                    if current.position[axis] == point_max:
                        next_vertex = current
                        break
                    elif current.position[axis] == point_min:
                        next_vertex = current
                        break

                point_max = point_max + 1
                point_min = point_min - 1
        return next_vertex


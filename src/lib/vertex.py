from lib.config import Config

class Vertex(object):

    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.adjacencies = []

        config = Config()

        self.title = str(id)
        self.fill_color = config.get("vertex", "fill-color")
        self.border_color = config.get("vertex", "border-color")
        self.border_size = float(config.get("vertex", "border-size"))
        self.size = float(config.get("vertex", "size"))
        self.font_size = float(config.get("vertex", "font-size"))

        self.selected = False
        self.touching_edges = []

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def has_edge(self, edge):
        return edge in self.adjacencies

    def touches_edge(self, edge):
        return edge in self.touching_edges

    def add_edge(self, edge):
        if not self.has_edge(edge):
            self.adjacencies.append(edge)

    def remove_edge(self, edge):
        if self.has_edge(edge):
            if edge.start.touches_edge(edge):
                edge.start.touching_edges.remove(edge)

            if edge.end.touches_edge(edge):
                edge.end.touching_edges.remove(edge)

            self.adjacencies.remove(edge)
            del edge

    def clear_adjacencies(self):
        for e in self.adjacencies:
            start = e.start
            end = e.end
            if start != self:
                start.remove_edge(e)
            if end != self:
                end.remove_edge(e)

        del self.adjacencies[:]

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


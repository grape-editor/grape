class Vertex(object):

    def __init__(self, id, position):
        self.id = id
        self.position = position
        self.adjacencies = []
        # TODO - Configuration file
        self.title = "Untitled"
        self.color = [0, 0, 0]
        self.size = 10
        self.selected = False

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def has_edge(self, edge):
        for e in self.adjacencies:
            if e == edge:
                return True

        return False

    def add_edge(self, edge):
        if not self.has_edge(edge):
            self.adjacencies.append(edge)

    def remove_edge(self, edge):
        if self.has_edge(edge):
            self.adjacencies.remove(edge)

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
        # if neighbor.count(vertex) == 1:
        #     neighbor.remove(vertex)
        # shortest_vertex = vertex
        # shortest_distance = None
        # for vertex in neighbor:
        #     delta_x = self.select[0].position[0] - vertex.position[0]
        #     delta_y = self.select[0].position[1] - vertex.position[1]
        #     distance = ((delta_x ** 2) + (delta_y ** 2)) ** 0.5
        #     if not shortest_distance or distance < shortest_distance:
        #         shortest_distance = distance
        #         shortest_vertex = vertex
        #
        # return shortest_vertex

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


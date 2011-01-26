class Vertex(object):
    name = None
    color = [0, 0, 0]
    position = [0, 0]
    neighborhood = [] 
    size = 10

    def __init__(self, name):
        self.name = name
      
    def is_neighbor(self, vertex):
        for v in self.neighborhood:
            if v == vertex:
                return True
        return False
    
    def add_neighbor(self, vertex):
        if isinstance(vertex, Vertex):
            self.neighborhood.append(vertex)
        
    def remove_neighbor(self, vertex):
        for v in self.neighborhood:
            if v == vertex:
                self.neighborhood.remove(v)

    def remove_all_neighbor(self):
        for v in self.neighborhood:
            self.neighborhood.remove(v)
            v.remove_neighbor(self)

    def draw(self, cairo, area):
        import math
        x = self.position[0]
        y = self.position[1]
        radius = self.size / 2
        cairo.arc(x, y, radius, 0, 2 * math.pi)
        cairo.close_path()
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        cairo.fill_preserve()

class Graph(object):
    
    def __init__(self, title):
        self.graph_title = title
        self.vertex_title = 0
        self.vertex = []

    def add_vertex(self, position):
        vertex = Vertex(self.vertex_title)        
        vertex.position = position
        self.vertex_title = self.vertex_title + 1
        self.vertex.append(vertex)
        print "ok"
    
    def remove_vertex(self, position):
        current_x = position[0]
        current_y = position[1]
        for v in self.vertex:
            r = v.size / 2
            x = v.position[0]
            y = v.position[1]
            if (x - r) <= current_x and (x + r) >= current_x :
                if (y - r) <= current_y and (y + r) >= current_y:
                    self.vertex.remove(v)
                    v.remove_all_neighbor()
                    print "ok"
                    break

    def add_edge(self, vertex1, vertex2):
        vertex1.add_neighbor(vertex2)
        vertex2.add_neighbor(vertex1)
        print "ok"

    def remove_edge(self, vertex1, vertex2):
        vertex1.remove_neighbor(vertex2)
        vertex2.remove_neighbor(vertex1)
        print "ok"
        
    def draw(self, cairo, area):
        for v in self.vertex:
            v.draw(cairo, area)
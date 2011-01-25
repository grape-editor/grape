class Vertex(object):
    name = None
    color = [0, 0, 0]
    position = [0, 0]
    neighborhood = [] 
    size = 10

    def __init__(self, name):
        self.name = name
    
    def set_position(self, posx, posy):
        self.position = [posx, posy]
    
    def set_color(self, r, g, b):
        self.color = [r, g, b]
    
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
            x = self.position[0]
            y = self.position[1]
            radius = self.size / 2
            #cairo.arc(x, y, radius, 0, 2 * math.pi)
            
            cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
            cairo.fill_preserve()

class Graph(object):
    
    def __init__(self, name):
        self.name = name

    def add_vertex(self, vertex):
        print "Adicionando um vertice"
        self.vertex.append(vertex)
    
    def remove_vertex(self,vertex):
        self.vertex.remove(vertex)
        vertex.remove_all_neighbor()

    def add_edge(self, vertex1, vertex2):
        vertex1.add_neighbor(vertex2)
        vertex2.add_neighbor(vertex1)
        print "Edge added"

    def remove_edge(self, vertex1, vertex2):
        vertex1.remove_neighbor(vertex2)
        vertex2.remove_neighbor(vertex1)
        print "Edge removed"
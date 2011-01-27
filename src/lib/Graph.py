class Vertex(object):

    def __init__(self, name, position):
        self.name = name
        self.color = [0, 0, 0]
        self.position = position
        self.neighborhood = []
        self.size = 10
        self.marked = False      
      
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
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        radius = self.size / 2
        cairo.arc(x, y, radius, 0, 2 * math.pi)
        cairo.close_path()        


class Graph(object):
    
    def __init__(self, title):
        self.graph_title = title
        self.vertex_title = 0
        self.vertex = []

    def get_vertex(self, position):
        current_x = position[0]
        current_y = position[1]
        for v in self.vertex:
            r = v.size / 2
            x = v.position[0]
            y = v.position[1]
            if (x - r) <= current_x and (x + r) >= current_x :
                if (y - r) <= current_y and (y + r) >= current_y:
                    return v
        return None
    
    def add_vertex(self, position):
        vertex = Vertex(self.vertex_title, position)        
        vertex.position = position
        self.vertex_title = self.vertex_title + 1
        self.vertex.append(vertex)
        print "ok"
    
    def remove_vertex(self, position):
        vertex = self.get_vertex(position) 
        if  vertex != None:
            self.vertex.remove(vertex)
            vertex.remove_all_neighbor()
            print "ok"
            
        

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
            v.marked = 1
            
            cairo.set_source_rgb(0, 0, 0)
            
            for n in v.neighborhood:
                if v.marked == 0:
                    n.marked = 1
                    cairo.move_to(v.position[0], v.position[1])
                    cairo.line_to(n.position[0], n.position[1])

        
        for v in self.vertex:
            v.marked = 0
        cairo.fill_preserve()

class Vertex(object):

    def __init__(self, id, position):
        self.id = id
        self.name = "Noname"
        self.color = [0, 0, 0]
        self.position = position
        self.neighborhood = []
        self.size = 10
      
    def is_neighbor(self, vertex):
        for v in self.neighborhood:
            if v == vertex:
                return True
        return False
    
    def add_neighbor(self, vertex):
        if isinstance(vertex, Vertex):
            if self.is_neighbor(vertex) == False:
                self.neighborhood.append(vertex)
        
    def remove_neighbor(self, vertex):
        self.neighborhood.remove(vertex)

    def remove_all_neighbor(self): 
        for v in self.neighborhood:
            v.remove_neighbor(self)
        #Free all neighbothood's position list to the collector
        del self.neighborhood[:]
                    
    def select(self, bool):
        if bool:
            self.color = [1, 0, 0]
        else:
            self.color = [0, 0, 0]
        
    def draw(self, cairo, area):
        import math
        x = self.position[0]
        y = self.position[1]
        cairo.set_source_rgb(self.color[0], self.color[1], self.color[2])
        radius = self.size / 2
        cairo.arc(x, y, radius, 0, 2 * math.pi)
        cairo.fill_preserve()
        cairo.stroke()

#Is needed think about this class. Because it will be useful after
#Inside object Vertex put a Edge list. (Replace neighbor list)
#
#class Edge(object):
#    def __init__(self, vertex1, vertex2):
#        self.start = vertex1
#        self.end = vertex2


class Graph(object):
    def __init__(self, title, complete=False):
        self.graph_title = title
        self.vertex_id = 0
        self.vertex = []
        self.complete = complete

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
        vertex = Vertex(self.vertex_id, position)  
        vertex.position = position
        self.vertex_id = self.vertex_id + 1
        if self.complete:
            vertex.visited = False
            for v in self.vertex:
                self.add_edge(vertex, v)
        self.vertex.append(vertex)
        print "ok"
    
    def remove_vertex(self, position):
        vertex = self.get_vertex(position) 
        if  vertex != None:
            vertex.remove_all_neighbor()
            self.vertex.remove(vertex)
            print "ok"

    def add_edge(self, vertex1, vertex2):
        vertex1.add_neighbor(vertex2)
        vertex2.add_neighbor(vertex1)
        print "ok"

    def remove_edge(self, vertex1, vertex2):
        vertex1.remove_neighbor(vertex2)
        vertex2.remove_neighbor(vertex1)
        print "ok"
    
    def draw_vertex(self, cairo, area, vertex):
        vertex.draw(cairo, area)
    
    def draw_edge(self, cairo, area, vertex1, vertex2):
        cairo.set_source_rgb(0, 0, 0)
        cairo.set_line_width(1)
        cairo.move_to(vertex1.position[0], vertex1.position[1])
        cairo.line_to(vertex2.position[0], vertex2.position[1])
        cairo.stroke()
    
    def draw(self, cairo, area):
        for v in self.vertex:
            self.draw_vertex(cairo, area, v)
            v.visited = True
            for n in v.neighborhood:
                if n.visited != True:
                    self.draw_edge(cairo, area, v, n)
               
        for v in self.vertex:
            v.visited = None
        
        

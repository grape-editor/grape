

class Algorithm(object):
    def __init__(self):
        self.name = "Algorithm"
        self.category = "Blah"

        self.vertex_list = []
        
    def march_vertex(self, vertex):
        print "Maching vertex:" , vertex

    def march_edge(self, edge):
        print "Marcing edge:", edge

    def run(self):
        print self.name
        print self.category


from lib.algorithm import Algorithm

class Dijkstra(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

    def run(self):
        for v in self.vertex_list:
            self.check(v)
            self.show()
            self.uncheck(v)


        for e in self.edge_list:
            self.check(e)
            self.show()
            self.uncheck(e)


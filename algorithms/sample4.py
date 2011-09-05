from lib.algorithm import Algorithm

class Sample4(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

        self.category = "Examples"

    def run(self):
        from random import choice
        
        for v in self.vertex_list:
            self.check_vertex(v)
            self.show()
            self.uncheck_vertex(v)

        for e in self.edge_list:
            self.check_edge(e)
            self.check_vertex(e.start)
            self.check_vertex(e.end)

            self.show()

            self.uncheck_edge(e)
            self.uncheck_vertex(e.start)
            self.uncheck_vertex(e.end)


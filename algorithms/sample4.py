from lib.algorithm import Algorithm

class Sample4(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

        self.category = "Examples"

    def run(self):
        from random import choice
        
        for v in self.vertex_list:
            self.check(v)
            self.show()
            self.uncheck(v)

        self.show()
        
        for e in self.edge_list:
            self.check(e)
            self.check(e.start)
            self.check(e.end)

            self.show()

            self.uncheck(e)
            self.uncheck(e.start)
            self.uncheck(e.end)

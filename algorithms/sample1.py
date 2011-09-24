from lib.algorithm import Algorithm

class Sample1(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

        self.category = "Examples"

    def run(self):
#        super(Sample1, self).run(graph)

        if not len(self.vertex_list) > 0:
            return
        
        from time import sleep
        from random import choice
        
        for vertex in range(50):
            v = choice(self.vertex_list)

            self.check(v)
            self.show()
            self.uncheck(v)

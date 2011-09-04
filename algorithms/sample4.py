from lib.algorithm import Algorithm

class Sample4(Algorithm):
    def __init__(self):
        Algorithm.__init__(self)

        self.name = "Sample4"
        self.category = "Examples"

    def run(self):
        if not len(self.vertex_list) > 0:
            return
        
        from random import choice
        
        for vertex in range(10):
            v = choice(self.vertex_list)

            self.check_vertex(v)
            self.show()
            self.uncheck_vertex(v)

from lib.algorithm import Algorithm

class Sample4(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

        self.category = "Examples"

    def run(self):
        from random import choice
        
        first = self.vertex_list[0]
        goal = self.vertex_list[-1]

        current = first
                
        fringe = []
        not_visited = []

        while current != goal:
            self.check(current)
            self.show()
            fringe.append(current)

            if len(current.vertex_list) > 0:
                for v in current.vertex_list:
                    not_visited.append(v)
            else:
                fringe.remove(current)
                self.uncheck(current)
            current = not_visited.pop()

        self.show()

from lib.algorithm import Algorithm
import math

class Cicle(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

        self.category = "Examples"
    
    def run(self):

        dest = [0,2,7,16,5,0]
        
        for i in range(len(dest)):
            v = self.find(dest[i])
            for e in v.edge_list:
                if e.end.id == dest[i+1] or e.start.id == dest[i+1]:
                    self.check(e)
                    break
            self.check(v)
            self.show()
        

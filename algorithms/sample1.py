from lib.algorithm import Algorithm

class Sample1(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

        self.category = "Examples"

    def run(self):
        
        from random import choice
        
        
        first = self.vertex_list[0]
        goal = 30
        
        queue = [(first, None)]

        for v in self.vertex_list:
            for e in v.edge_list:
                e.__visited = False

        rtn = None

        while len(queue) > 0:
            node = queue[0]
            queue = queue[1:]
            self.check(node[0])
            self.check(node[1])
            self.show()
            
            if node[0].id == goal:
                rtn = node[0]
                break
            for edge in node[0].edge_list:
                if not edge.__visited:
                    edge.__visited = True
                    if edge.start == node[0]:
                        queue.append((edge.end, edge))
                    else:
                        queue.append((edge.start,edge))

            self.uncheck(node[0])
            self.uncheck(node[1])
        
        print rtn



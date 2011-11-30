from lib.algorithm import Algorithm

class Dijkstra(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

        self.first = int(self.input_box("", "Origem"))
        self.goal = int(self.input_box("", "Destino"))

    def run(self):
        
        first = self.vertex_list[0]
        goal = 30
        
        stack = [first]

        for v in self.vertex_list:
            for e in v.edge_list:
                e.__visited = False

        while len(stack) > 0:
            node = stack.pop()
            self.check(node)
            self.show()
            if node.id == goal:
                rtn = node
                break

            for edge in node.edge_list:
                if not edge.__visited:
                    edge.__visited = True
                    if edge.start == node:
                        stack.append(edge.end)
                    else:
                        stack.append(edge.start)


            self.uncheck(node)


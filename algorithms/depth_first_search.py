# coding=utf-8

class DepthFirstSearch(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)
	
    def run(self):
        first = self.vertex_list[0] # consideremos o primeiro vértice criado como origem, por enquanto
        goal = self.vertex_list[-1]  # consideremos o último vértice criado como origem, por enquanto

        stack = [] # utlizaremos uma pilha para nossa busca em profundidade

        # adicionamos nosso inicio na pilha
        stack.append((first, None)) # uma tupla (vertice, aresta). Como este é o inicio não utilizamos nenhuma aresta para alcançá-lo

		# marcamos todos os vértices como não visitados
        for e in self.edge_list:
            set_attribute(e, 'visited', False)

        while len(stack) > 0:
            pop = True
            
            node = stack[-1]
            set_attribute(node[1], 'visited', True)
            self.check(node[0])
            self.check(node[1])
            self.show()
            
            if node[0].id == goal.id:
                rtn = node[0]
                break
            else:
                for edge in node[0].edge_list:
                    if not get_attribute(v, 'visited'):
                        break
                
                self.uncheck(node[0])
                self.uncheck(node[1])
                stack.pop()
                
            for edge in node[0].edge_list:
                if not edge.__visited:
                    if edge.start == node[0]:
                        stack.append((edge.end, edge))
                    else:
                        stack.append((edge.start,edge))

# coding=utf-8

from lib.algorithm import Algorithm

class DepthFirstSearch(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)
        # input box para capturarmos o vértice origem
        self.first_id = int(self.input_box('Escreva o número do vértice origem', 'Origem'))
        # input box para capturarmos o vértice destino
        self.goal_id = int(self.input_box('Escreva o número do vértice destino', 'Destino'))
    
    def run(self):
        first = self.find(self.first_id)
        goal = self.find(self.goal_id)

        stack = [] # utlizaremos uma pilha para nossa busca em profundidade

        # adicionamos nosso inicio na pilha
        stack.append((first, None)) # uma tupla (vertice, aresta). Como este é o inicio não utilizamos nenhuma aresta para alcançá-lo

        # marcamos todas as arestas como não visitados
        for e in self.edge_list:
            self.set_attribute(e, 'visited', 'no')

        while len(stack) > 0:
            node = stack[-1]
            if node[1]:
                self.set_attribute(node[1], 'visited', 'yes')
            self.check(node[0])
            self.check(node[1])
            self.show()

            if node[0].id == goal.id:
                rtn = node[0]
                break
            else:
                pop = True
                for edge in node[0].edge_list:
                    if self.get_attribute(edge, 'visited') == 'no':
                        pop = False
                        break

                if pop:
                    self.uncheck(node[0])
                    self.uncheck(node[1])
                    stack.pop()
                    continue

            for edge in node[0].edge_list:
                if self.get_attribute(edge, 'visited') == 'yes':
                    if edge.start == node[0]:
                        stack.append((edge.end, edge))
                    else:
                        stack.append((edge.start,edge))

from lib.algorithm import Algorithm
import math

class Astar(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

        self.category = "Examples"
        self.first = self.find(int(self.input_box("", "Origem")))
        self.goal = self.find(int(self.input_box("", "Destino")))
    
    def distance(self, v1, v2):
        return math.sqrt((v1.position[0] - v2.position[0]) ** 2 + (v1.position[1] - v2.position[1]) ** 2)
        
    def draw_path(self, came_from, x, start):
        self.uncheck_all()
        self.check(x)
        
        while x.id != start.id:
            map(self.check, came_from[x])
            x = came_from[x][0]
        
        self.show()
    
    def run(self):
        closedset = []
        openset = [self.first]
        came_from = {}
        g_score = {}
        h_score = {}
        f_score = {}
        
        g_score[self.first] = 0
        h_score[self.first] = self.distance(self.first, self.goal)
        f_score[self.first] = g_score[self.first] + h_score[self.first]
        
        self.check(self.first)
        self.show()
        
        while len(openset) > 0:
            lesser = None
            x = None
            
            for k, v in f_score.iteritems():
                if k in openset and (lesser == None or v < lesser):
                    lesser = v
                    x = k
                    
            self.draw_path(came_from, x, self.first)
            
            if x.id == self.goal.id:
                return # caminho
            openset.remove(x)
            closedset.append(x)
            
            for edge in x.edge_list:
                if edge.start == x:
                    y = edge.end
                else:
                    y = edge.start
                
                if y in closedset:
                    continue
                
                tentative_g_score = g_score[x] + self.distance(x, y)
                
                if y not in openset:
                    openset.append(y)
                    tentative_is_better = True
                elif tentative_g_score < g_score[y]:
                    tentative_is_better = True
                else:
                    tentative_is_better = False
                
                if tentative_is_better:
                    came_from[y] = (x, edge)
                    self.draw_path(came_from, x, self.first)
                    g_score[y] = tentative_g_score
                    h_score[y] = self.distance(y, self.goal)
                    f_score[y] = g_score[y] + h_score[y]
        

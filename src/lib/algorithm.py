from threading import Thread
from threading import Semaphore
from time import sleep

from lib.vertex import Vertex
from lib.edge import Edge

class Algorithm(Thread):

    def __init__(self, graph):
        Thread.__init__(self)

        self.__states = []
        self.__checks = {}

        self.__semaphore = Semaphore()

        self.__graph = graph
        self.__history = History()
        
        self.graph = graph.graph_to_networkx()
        self.vertex_list = graph.vertices
        self.edge_list = graph.edges

    def check(self, what):
        """Checks vertex or checks a edge"""
        self.checks[what] = what
            
    def uncheck(self, what):
        """Unchecks vertex or unchecks a edge"""
        self.checks.pop(what)
        
    def next(self):
        if not self.redo():
            self.__signal()
        
    def prev(self):
        self.undo()
        
    def play(self):
        pass

    def stop(self):
        pass

    def save_state(self):
        self.states.append(())        

    def __wait(self):
        """Stop thread until receive release signal"""
        self.save_state()
        self.__semaphore.acquire()

    def __signal(self):
        """Sets free the thread to continue"""
        self.__semaphore.release()

    def __operation(method):
        def decorated(self):
            saved = [self.__vertex_copy, self.__edge_copy]
            perform = (method, (self,))
            revert = (self.__set_value, (saved,))
            self.__history.add(perform, revert)
        return decorated

    def __set_value(self, n):
        self.__vertex_copy = n[0]
        self.__edge_copy = n[1]

    def show(self):
        self.__wait()

    def run(self):
        print self.name
        print self.category


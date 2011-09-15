from threading import Thread
from threading import Semaphore
from time import sleep

from lib.vertex import Vertex
from lib.edge import Edge

class Algorithm(Thread):

    def __init__(self, graph):
        Thread.__init__(self)
        self.category = "Blah"

        self.vertex_list = graph.vertices
        self.edge_list = graph.edges

        self.__edge_copy__ = {}
        self.__vertex_copy__ = {}
        self.__semaphore = Semaphore()

        self.__graph__ = graph
        self.graph = graph.graph_to_networkx()

    def check(self, what):
        """Checks vertex or checks a edge"""
        if isinstance(what, Vertex):
            vertex = what
            self.__vertex_copy__[vertex] = [vertex.fill_color, vertex.border_color,
                                            vertex.border_size, vertex.size,
                                            vertex.font_size]
            # TODO - Config file
            vertex.fill_color = "#FF0000"
            vertex.border_color = "#FF0000"
            vertex.border_size = float(10)
            # vertex.size = ??
            # vertex.font_size = ??
        
        elif isinstance(what, Edge):
            edge = what
            self.__edge_copy__[edge] = [edge.color, edge.width]
            # TODO - Config file
            edge.color = "#FF0000"
            edge.width = float(10)

    def uncheck(self, what):
        """Unchecks vertex or unchecks a edge"""
        if isinstance(what, Vertex):
            vertex = what
            config = self.__vertex_copy__[vertex]

            vertex.fill_color = config[0]
            vertex.border_color = config[1]
            vertex.border_size = config[2]
            vertex.size = config[3]
            vertex.font_size  = config[4]
        elif isinstance(what, Edge):
            edge = what
            config = self.__edge_copy__[edge]

            edge.color = config[0]
            edge.width  = config[1]

    def __wait__(self):
        """Stop thread until receive release signal"""
        self.__semaphore.acquire()

    def __signal__(self):
        """Sets free the thread to continue"""
        self.__semaphore.release()

    def show(self):
        self.__wait__()

    def run(self):
        print self.name
        print self.category


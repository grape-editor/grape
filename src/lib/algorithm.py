from threading import Thread
from time import sleep

class Algorithm(Thread):

    def __init__(self, graph):
        Thread.__init__(self)
        self.category = "Blah"

        self.vertex_list = graph.vertices
        self.edge_list = graph.edges

        self.__edge_copy__ = {}
        self.__vertex_copy__ = {}

        self.__graph__ = graph
        self.graph = graph.graph_to_networkx()

    def check_vertex(self, vertex):
        """Checks vertex"""
        self.__vertex_copy__[vertex] = [vertex.fill_color, vertex.border_color,
                                        vertex.border_size, vertex.size,
                                        vertex.font_size]
        # TODO - Config file
        vertex.fill_color = "#FF0000"
        vertex.border_color = "#FF0000"
        vertex.border_size = float(10)
        # vertex.size = ??
        # vertex.font_size = ??

    def uncheck_vertex(self, vertex):
        """Unchecks vertex"""
        config = self.__vertex_copy__[vertex]

        vertex.fill_color = config[0]
        vertex.border_color = config[1]
        vertex.border_size = config[2]
        vertex.size = config[3]
        vertex.font_size  = config[4]

    def uncheck_edge(self, edge):
        """Unchecks a edge"""
        config = self.__edge_copy__[edge]

        edge.color = config[0]
        edge.width  = config[1]
        
    def check_edge(self, edge):
        """Checks a edge"""
        self.__edge_copy__[edge] = [edge.color, edge.width]

        # TODO - Config file
        edge.color = "#FF0000"
        edge.width = float(10)

    def show(self):
        sleep(1)

    def run(self):
        print self.name
        print self.category


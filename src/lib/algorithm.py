
from threading import Thread
from time import sleep


class Algorithm(Thread):

    def __init__(self, graph):
        Thread.__init__(self)
        self.category = "Blah"

        self.graph = graph
        self.vertex_list = graph.vertices

    def uncheck_vertex(self, vertex):
        print "Uncheck vertex:" , vertex
        config = self.__vertex_copy__[vertex]

        vertex.fill_color = config[0]
        vertex.border_color = config[1]
        vertex.border_size = config[2]
        vertex.size = config[3]
        vertex.font_size  = config[4]
        
    def check_vertex(self, vertex):
        print "Check vertex:" , vertex

        self.__vertex_copy__ = {}
        self.__vertex_copy__[vertex] = [vertex.fill_color, vertex.border_color,
                                        vertex.border_size, vertex.size,
                                        vertex.font_size]

        # TODO - Config file
        vertex.fill_color = "#FF0000"
        vertex.border_color = "#FF0000"
        vertex.border_size = float(10)
        # vertex.size = ??
        # vertex.font_size = ??

    def show(self):
        sleep(1)

    def march_edge(self, edge):
        print "Marcing edge:", edge

    def run(self):
        print self.name
        print self.category


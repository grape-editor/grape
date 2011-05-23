import lib.networkx as nx

class Graph(nx.Graph):
    
    def __init__(self, *args):
        nx.Graph.__init__(self, *args)

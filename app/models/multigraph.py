import lib.networkx as nx

class MultiGraph(nx.MultiGraph):
    
    def __init__(self, *args):
        nx.MultiGraph.__init__(self, *args)

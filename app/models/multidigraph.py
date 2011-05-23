import lib.networkx as nx

class MultiDiGraph(nx.MultiDiGraph):
    
    def __init__(self, *args):
        nx.MultiDiGraph.__init__(self, *args)

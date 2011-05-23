import lib.networkx as nx

class DiGraph(nx.DiGraph):
    
    def __init__(self, *args):
        nx.DiGraph.__init__(self, *args)

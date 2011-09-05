from lib.config import Config

class Edge(object):
    """ Edge class"""
    def __new__(self, *args, **kwargs):
        """Check if is possible adde edge"""
        config = Config()
        graph_type = config.get("graph", "type")
        self.directed = graph_type in ['DiGraph', 'MultiDiGraph']
        self.multiple = graph_type in ['MultiGraph', 'MultiDiGraph']

        id, start, end = args

        digraph = self.directed and not end in start.adjacencies
        graph = not self.directed and not end in start.adjacencies and not start in end.adjacencies

        if (self.multiple) or digraph or graph:
            instance = super(Edge, self).__new__(self, *args, **kwargs)
            return instance
        else:
            return None

    def __init__(self, id, start, end):
        self.id = id
        self.start = start
        self.end = end

        config = Config()
        self.title = str(id)
        graph_type = config.get("graph", "type")
        self.directed = graph_type in ['DiGraph', 'MultiDiGraph']
        self.color = config.get("edge", "color")
        self.width = float(config.get("edge", "width"))

        start.touching_edges.append(self)
        end.touching_edges.append(self)

        self.selected = False
        start.add_edge(self)

        if not self.directed:
            end.add_edge(self)

    def __str__(self):
        """Print a formated edge"""
        value = self.title + " " + str(start)
        if self.directed:
            value += " -> "
        else:
            value += " -- "
        value += str(end)
        return value

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def touches(self, vertex):
        return vertex == self.start or vertex == self.end



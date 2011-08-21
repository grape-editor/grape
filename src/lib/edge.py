from lib.config import Config

class Edge(object):
    def __init__(self, id, start, end, bidirectional):
        self.id = id
        self.start = start
        self.end = end
        self.bidirectional = bidirectional

        config = Config()
        self.title = str(id)
        self.color = config.get("edge", "color")
        self.width = float(config.get("edge", "width"))

        start.touching_edges.append(self)
        end.touching_edges.append(self)

        start.add_edge(self)

        if self.bidirectional:
            end.add_edge(self)

    def touches(self, vertex):
        return vertex == self.start or vertex == self.end


import gzip
import base64
import pickle
import os


class Graph(object):

    def __init__(self, title="Untitled"):
        self.vertex_id = 0
        self.edge_id = 0
        self.vertices = []
        self.edges = []
        self.title = title
        self.selected_vertices_cache = None
        self.path = None
        self.directed = False

    def find_by_position(self, position):
        current_x = position[0]
        current_y = position[1]

        for v in self.vertices:
            r = v.size / 2
            x = v.position[0]
            y = v.position[1]

            if (x - r) <= current_x and (x + r) >= current_x:
                if (y - r) <= current_y and (y + r) >= current_y:
                    return v

        return None

    def find(self, id):
        lo = 0
        hi = len(self.vertices)

        while lo < hi:
            mid = (lo + hi) // 2
            midval = self.vertices[mid].id

            if midval < id:
                lo = mid + 1
            elif midval > id:
                hi = mid
            else:
                return self.vertices[mid]

        return None

    def find_edge(self, start, end):
        edges = []

        for e in self.edges:
            if e.start == start and e.end == end:
                edges.append(e)
            elif e.bidirectional and e.start == end and e.end == start:
                edges.append(e)

        return edges

    def selected_vertices(self):
        if self.selected_vertices_cache:
            return self.selected_vertices_cache

        selected = []

        for v in self.vertices:
            if v.selected:
                selected.append(v)

        return selected

    def has_edge(self, edge):
        return edge in self.edges

    # TODO - Header

    def open(self, name):
        f = open(name, 'rb')
        encoded = f.read()
        compressed = base64.b64decode(encoded)
        data = gzip.zlib.decompress(compressed)
        graph = pickle.loads(data)
        f.close()

        graph.path = name

        return graph

    def save(self, name):
        if not name.endswith('.cgf'):
            name += '.cgf'

        self.path = name
        self.title = os.path.basename(name)

        f = open(name, 'wb')
        data = pickle.dumps(self)
        compress = gzip.zlib.compress(data)
        encoded = base64.b64encode(compress)
        f.write(encoded)
        f.close()


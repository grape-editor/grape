import gzip
import base64
import pickle
import os

from lib.config import Config
from lib.vertex import Vertex
from lib.edge import Edge

class Graph(object):
    def __init__(self, title=""):
#       Cant stay here, cause splode stack in pickle dump
#        self.config = Config()

        self.vertex_id = 0
        self.edge_id = 0
        self.vertices = []
        self.edges = []
        self.title = title
        self.selected_vertices_cache = None
        self.path = None

        config = Config()
        if not title:
            self.title = config.get("graph", "title")
        self.type = config.get("graph", "type")

        self.directed = self.type in ['DiGraph', 'MultiDiGraph' ]
        self.multiple = self.type in ['MultiGraph', 'MultiDiGraph']

        self.background_color = config.get("graph", "background-color")

    def __str__(self):
        """Prints all verticies and your adjacncies lists"""
        value = ""
        for v in self.vertices:
            value += str(v) + ": "
            for n in v.adjacencies:
                value += str(n) + " "
            value += "\n"
        return value

    def find_in_area(self, x, y, w, h):
        vertices = []
        for v in self.vertices:
            vx = v.position[0]
            vy = v.position[1]
            def in_range(position, p, r):
                if r > 0:
                    return (position >= p and position <= (p + r))
                else:
                    return (position <= p and position >= (p + r))
            in_x = in_range(vx, x, w)
            in_y = in_range(vy, y, h)
            if in_x and in_y:
                vertices.append(v)
        return vertices

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

    def find_edge_from_vertex(self, vertex, id):
        for edge in vertex.edge_list:
            if int(id) == edge.id:
                return edge
        return None

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

    def add_vertex(self, position):
        vertex = Vertex(self.vertex_id, position)
        self.vertices.append(vertex)
        self.vertex_id += 1

        return vertex

    def remove_vertex(self, vertex):
        if vertex:
            to_be_removed = list(vertex.touching_edges)
            map(lambda e: self.remove_edge(e), to_be_removed)
            self.vertices.remove(vertex)

    def add_edge(self, start, end):
        edge = Edge(self.edge_id, start, end)
        if edge:
            self.edges.append(edge)
            self.edge_id += 1

        return edge

    def remove_edge(self, edge):
        if not self.has_edge(edge):
            return
        # TODO - Figure out how to handle multiple edges
        edge.start.remove_edge(edge)
        if not edge.directed:
            edge.end.remove_edge(edge)
        self.edges.remove(edge)

    def toggle_vertex_selection(self, vertex):
        self.selected_vertices_cache = None

        if vertex.selected:
            vertex.deselect()
        else:
            vertex.select()

    def select_all(self):
        self.selected_vertices_cache = None
        for vertex in self.vertices:
            vertex.select()

    def select_vertex(self, vertex):
        self.selected_vertices_cache = None
        vertex.select()

    def deselect_vertex(self, vertex):
        self.selected_vertices_cache = None
        vertex.deselect()

    def clear_selection(self):
        if len(self.selected_vertices()) > 0:
            selected_vertices = self.selected_vertices()

            for vertex in selected_vertices:
                self.deselect_vertex(vertex)

    def move_selection(self, direction):
        selected = self.selected_vertices()

        if len(selected) == 1:
            if direction == 'up':
                sort_index = 1
                slice = lambda arr, index: arr[:index - 1]
            elif direction == 'down':
                sort_index = 1
                slice = lambda arr, index: arr[index + 1:]
            elif direction == 'left':
                sort_index = 0
                slice = lambda arr, index: arr[:index - 1]
            elif direction == 'right':
                sort_index = 0
                slice = lambda arr, index: arr[index + 1:]
            else:
                return None

            ordered = sorted(self.vertices, key=lambda vertex: vertex.position[sort_index])
            index = ordered.index(selected[0])
            ordered = slice(ordered, index)

            vertex = selected[0].nearest_vertices(ordered, int(not sort_index))

            if vertex:
                self.deselect_vertex(selected[0])
                self.select_vertex(vertex)

    def graph_to_networkx(self):
        import networkx as nx

        g = None

        print self.type
        if self.type == 'Graph':
            print "AQUI"
            g = nx.Graph(title=self.title)
        elif self.type == 'DiGraph':
            g = nx.DiGraph(title=self.title)
        elif self.type == 'MultiGraph':
            g = nx.MultiGraph(title=self.title)
        elif self.type == 'MultiDiGraph':
            g = nx.MultiDiGraph(title=self.title)

        if g == None:
            return

        for v in self.vertices:
            g.add_node(v.id, id=v.id)

            for attr in v.__dict__:
                if attr.startswith("user_"):
                    t_identifier = attr[5:]
                    t_value = getattr(self.vertex, attr)
                    self.liststore_properties.append([t_identifier, t_value])
                    g.node[v.id][t_identifier] = t_value

        for e in self.edges:
            g.add_edge(e.start.id, e.end.id, id=e.id)
            for attr in e.__dict__:
                if attr.startswith("user_"):
                    t_identifier = attr[5:]
                    t_value = getattr(self.vertex, attr)
                    self.liststore_properties.append([t_identifier, t_value])
                    for s in g[e.start.id][e.end.id]:
                        if g[e.start.id][e.end.id][s]['id'] == e.id:
                            g[e.start.id][e.end.id][s][t_identifier] = t_value

        print g.nodes(data=True)
        print g.edges(data=True)
        return g


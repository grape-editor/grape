import lib.networkx as nx

from app.models import *


class GraphsController(object):

    def add_node(self, graph, position):
        if 'node_id' not in graph.graph:
            graph.graph['node_id'] = 0
            
        params = {
            'id': graph.graph['node_id'],
            'title': str(graph.graph['node_id']),
            'position': position,
            # TODO: configuration file
            'size': 30,
            'border_size': 2,
            'fill_color': (1, 1, 1),
            'border_color': (0, 0, 0)
        }
            
        graph.add_node(graph.graph['node_id'], params)
        node = graph.node[graph.graph['node_id']]
        graph.graph['node_id'] += 1
        
        return node

    def remove_node(self, graph, node):
        if graph.has_node(node):
            graph.remove_node(node)

    def add_edge(self, graph, n1, n2):
        if n1 not in graph.nodes() or n2 not in graph.nodes():
            return
        
        params = {
            'directed': False,
            'title': '',
            'color': (0, 0, 0),
            'width': 1
        }
        
        if isinstance(graph, DiGraph) or isinstance(graph, MultiDiGraph):
            params['directed'] = True
        
        if isinstance(graph, MultiGraph) or isinstance(graph, MultiDiGraph):
            params['id'] = 0

            if graph.has_edge(n1, n2):
                params['id'] = len(graph.edge[n1][n2])

            graph.add_edge(n1, n2, attr_dict=params)
            edge = graph.edge[n1][n2][params['id']]
            
            return edge
        else:
            if graph.has_edge(n1, n2):
                return None
            
            graph.add_edge(n1, n2, attr_dict=params)
            edge = graph.edge[n1][n2]
            
            return edge

    def remove_edge(self, graph, edge):
        if graph.has_edge(*edge):
            graph.remove_edge(*edge)
         
    def open(self, path):
        format = path.split(".")[-1]

        if format == "pickle":
            return nx.read_gpickle(path)
        elif format == "yml":
            return nx.read_yaml(path)
        else:
            return nx.read_yaml(path)
            
    def save(self, graph, path):
        graph.graph['path'] = path

        format = path.split(".")[-1]
        
       if format == "pickle":
            nx.write_gpickle(graph, path)
        elif format == "yml":
            nx.write_yaml(graph, path)
        else:
            path += ".yml"
            graph.graph['path'] = path
            nx.write_yaml(graph, path)


    def solve_imports(self, possible_formats):
        formats = []
        for format in possible_formats:
            imported = False
            
            if 'dependencies' in format:
                for dep in format['dependencies']:
                    try:
                        __import__(dep)
                    except:
                        continue
                    else:
                        imported = True    
                        break
            else:
                imported = True

            if imported:
                formats.append(format['name'])

        return formats


    def formats_default(self):
        return [
            {
                'name': "YAML (*.yml)",
                'dependencies': ['yaml']
            },
            {
                'name': "Pickle (*.pickle)",
                'dependencies': ['cPickle', 'pickle']
            }
        ]

    def formats_to_save(self):
        possible_formats = self.formats_default()
        return self.solve_imports(possible_formats)

    def formats_to_open(self):
        possible_formats = self.formats_default()
        return self.solve_imports(possible_formats)    
        

    # NEVER REMOVE THIS CODE
    # 
    # def move_selection(self, graph, direction):
    #     selected = graph.selected_nodes()
    # 
    #     if len(selected) == 1:
    #         if direction == 'up':
    #             sort_index = 1
    #             slice = lambda arr, index: arr[:index - 1]
    #         elif direction == 'down':
    #             sort_index = 1
    #             slice = lambda arr, index: arr[index + 1:]
    #         elif direction == 'left':
    #             sort_index = 0
    #             slice = lambda arr, index: arr[:index - 1]
    #         elif direction == 'right':
    #             sort_index = 0
    #             slice = lambda arr, index: arr[index + 1:]
    #         else:
    #             return None
    # 
    #         ordered = sorted(graph.nodes, key=lambda node: node.position[sort_index])
    #         index = ordered.index(selected[0])
    #         ordered = slice(ordered, index)
    # 
    #         node = selected[0].nearest_nodes(ordered, int(not sort_index))
    # 
    #         if node:
    #             self.nodes_controller.deselect(selected[0])
    #             self.nodes_controller.select(node)

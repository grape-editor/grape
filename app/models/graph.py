class Graph(object):
    def __init__(self, title="Untitle"):
        self.vertex_id = 0
        self.edge_id = 0
        self.vertices = []
        self.edges = []
        self.title = title
        self.selected_vertices_cache = None

    def find_by_position(self, position):
         current_x = position[0]
         current_y = position[1]
         
         for v in self.vertices:
             r = v.size / 2
             x = v.position[0]
             y = v.position[1]
             
             if (x - r) <= current_x and (x + r) >= current_x :
                 if (y - r) <= current_y and (y + r) >= current_y:
                     return v
                     
         return None   
        
    def find(self, id):
        # TODO - Enchace search performace (Binary Search)
        for v in self.vertices:
            if v.id == id:
                return v
                
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

                
    def open_file(self, name):
        import gzip
        import base64

        #Open, Read, Decode, Descompress file
        f = open(name, 'rb')
        file_encoded = f.read()
        file_compressed = base64.b64decode(file_encoded)
        file_content = gzip.zlib.decompress(file_compressed)
        f.close()

        #Get general informations about graph
        grape = ElementTree.fromstring(file_content)
        head = grape.find("head")
        title = head.find("title")
        self.drawarea.graph.title = title.text

        #Get vertexes list and create vertex in graph with yours settings    
        vertex = grape.findall("vertex")
        for v in vertex:
            vertex_id = v.find("id")
            id = int(vertex_id.text)
            vertex_options = v.find("options")
            position = []
            position.append(float(vertex_options.get("x")))
            position.append(float(vertex_options.get("y")))
            size = int(vertex_options.get("size"))
            color = Util.hex_to_rgb(vertex_options.get("color"))
            name = vertex_options.text
            new_vertex = self.drawarea.graph.add_vertex(position)
            new_vertex.set_options(id, position, name, color, size)

        #For each vertex now is building yours adjacency list or yours neighborhood
        for v in vertex:
            vertex_id = v.find("id")
            id = int(vertex_id.text)
            vertex1 = self.drawarea.graph.get_vertex_id(id)
            neighborhood = v.find("neighborhood")
            neighbor_id = neighborhood.findall("neighbor_id")
            for neighbor in neighbor_id:
                id = int(neighbor.text)
                vertex2 = self.drawarea.graph.get_vertex_id(id)
                self.drawarea.graph.add_edge(vertex1, vertex2)

        self.drawarea.set_changed(False)



        def save_file(self, name):
            import gzip
            import base64

            #Put general info about graph in xml file
            grape = ElementTree.Element("grape")
            head = ElementTree.SubElement(grape, "head")      
            title = ElementTree.SubElement(head, "title")
            self.graph.graph_title = os.path.basename(name)
            title.text = self.graph.title

            #Put all vertexes with your settings in xml file 
            for v in self.graph.vertex:
                vertex = ElementTree.SubElement(grape, "vertex")
                vertex_id = ElementTree.SubElement(vertex, "id")
                vertex_id.text = str(v.id)
                vertex_options = ElementTree.SubElement(vertex, "options")
                vertex_options.set("color", Util.rgb_to_hex(v.color))
                vertex_options.set("size", str(v.size))
                vertex_options.set("x", str(v.position[0]))
                vertex_options.set("y", str(v.position[1]))
                vertex_options.text = v.name

                #Here is put all adjacency list into of  xml file
                vertex_neighbors = ElementTree.SubElement(vertex, "neighborhood")
                for neighbor in v.neighborhood:
                    neighbor_id = ElementTree.SubElement(vertex_neighbors, "neighbor_id")
                    neighbor_id.text = str(neighbor.id) 

            #Verify extension of file
            if not name.endswith('.cgf'):
                name += '.cgf'

            #Compress, encode, write the result on disc
            f = open(name, 'wb')
            data = ElementTree.tostring(grape)
            compress = gzip.zlib.compress(data)
            encoded = base64.b64encode(compress)
            f.write(encoded)
            f.close()

            self.drawarea.set_changed(False)

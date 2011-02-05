import lib.util.Util as Util

import os
import sys
import gtk

from xml.etree import ElementTree
from gzip import GzipFile

class FileChooserDialog(object):  
    
    def __init__(self, builder, drawarea):
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        path = os.path.join(path, "gui", "FileChooserDialog.ui")        
        self.builder = builder
        self.builder.add_from_file(path)
        self.builder.connect_signals(self)
        self.file_chooser = self.builder.get_object("file_chooser_dialog")
                
        self.drawarea = drawarea
        self.graph = drawarea.graph

    def file_chooser_dialog_file_activated(self, widget):
        if self.method == "save":
            self.file_chooser_dialog_save(widget)
        elif self.method == "open":
            self.file_chooser_dialog_open(widget)
            
    def open_file(self, name):
        import gzip
        import base64
        
        #Open, Read, Decode, Decompress file
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

    def file_chooser_dialog_show(self):
        self.file_chooser.show_all()
    
    def file_chooser_dialog_cancel(self, widget):
        self.file_chooser.destroy()
        
    def file_chooser_dialog_open(self, widget):
        name = self.file_chooser.get_filename()
        self.open_file(name)
        self.drawarea.path = name
        self.file_chooser.destroy()
        
    def file_chooser_dialog_save(self, widget):
        # build a tree structure
        name = self.file_chooser.get_filename()
        self.save_file(name)
        self.drawarea.path = name
        self.file_chooser.destroy()

    def file_chooser_dialog_method_open(self):
        self.method = "open"
        confirm = self.builder.get_object("button_confirm")
        confirm.set_label(_("Open"))
        confirm.connect('clicked', self.file_chooser_dialog_open)
        self.file_chooser.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        self.file_chooser.set_title(_("Open"))
        
    def file_chooser_dialog_method_save(self):
        self.method = "save"
        confirm = self.builder.get_object("button_confirm")
        confirm.set_label(_("Save"))
        confirm.connect('clicked', self.file_chooser_dialog_save)
        self.file_chooser.set_action(gtk.FILE_CHOOSER_ACTION_SAVE)
        self.file_chooser.set_title(_("Save as..."))

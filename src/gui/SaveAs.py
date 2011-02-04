import lib.elementtree.ElementTree as ElementTree
import lib.graph.Graph

import gobject
import gtk
import os
import sys


class SaveAs(object):  
    
    def __init__(self, builder, graph):
        #domain = self.translate()
        #builder = gtk.Builder()
        #builder.set_translation_domain(domain)          
        
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        path = os.path.join(path, "gui", "SaveAs.ui")        
        builder.add_from_file(path)
        builder.connect_signals(self)
        
        self.graph = graph
        self.file_chooser = builder.get_object("file_chooser_dialog")
        self.file_chooser.connect("response", self.about_dialog_response)
        self.file_chooser.show_all()        

    def about_dialog_response(self, widget, event):
        name = widget.get_filename()        
        if name:
            self.about_dialog_save(name)
        self.file_chooser.destroy()

        
    def about_dialog_save(self, name):
        # build a tree structure
        grape = ElementTree.Element("grape")
        
        head = ElementTree.SubElement(grape, "head")      
        title = ElementTree.SubElement(head, "title")

        self.graph.graph_title = os.path.basename(name)
        title.text = self.graph.graph_title
         
        for v in self.graph.vertex:
            vertex = ElementTree.SubElement(grape, "vertex")
            vertex_id = ElementTree.SubElement(vertex, "id")
            vertex_id.text = str(v.id)
            vertex_options = ElementTree.SubElement(vertex, "options")
            vertex_options.set("color", self.rgb_to_hex(v.color))
            vertex_options.set("size", str(v.size))
            vertex_options.set("x", str(v.position[0]))
            vertex_options.set("y", str(v.position[1]))
            vertex_options.text = v.name
            
            vertex_neighbors = ElementTree.SubElement(vertex, "neighborhood")
            for neighbor in v.neighborhood:
                neighbor_id = ElementTree.SubElement(vertex_neighbors, "neighbor_id")
                neighbor_id.text = str(neighbor.id) 
        
        tree = ElementTree.ElementTree(grape)
        print name
        tree.write(name)
    
    def rgb_to_hex(self, rgb):
        import struct
        
        r = rgb[0] * 255
        g = rgb[1] * 255
        b = rgb[2] * 255
        
        rgb = (r, g, b)      
        hex = struct.pack('BBB',*rgb).encode('hex')
        print hex
        return hex

    def hex_to_rgb(self, hex):
        import struct
        
        rgb = struct.unpack('BBB', hex.decode('hex'))
        return rgb


# import lib.elementtree.ElementTree as ElementTree
import lib.util.Util as Util

import os
import sys

import xml.etree.ElementTree as ElementTree

class SaveAs(object):  
    
    def __init__(self, builder, graph):   
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        path = os.path.join(path, "gui", "SaveAs.ui")        
        builder.add_from_file(path)
        builder.connect_signals(self)
        
        self.graph = graph
        self.file_chooser = builder.get_object("file_chooser_dialog")
        self.file_chooser.show_all()        

#    def file_chooser_dialog_response(self, widget, event):
#        print event
#        if event == -4:
#            self.file_chooser_dialog_close()

    def file_chooser_dialog_close(self):
        self.file_chooser.destroy()
        
    def file_chooser_dialog_cancel(self, widget):
        self.file_chooser_dialog_close()
        
    def file_chooser_dialog_save(self, widget):
        import gzip
        # build a tree structure
        name = self.file_chooser.get_filename()
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
            vertex_options.set("color", Util.rgb_to_hex(v.color))
            vertex_options.set("size", str(v.size))
            vertex_options.set("x", str(v.position[0]))
            vertex_options.set("y", str(v.position[1]))
            vertex_options.text = v.name
            
            vertex_neighbors = ElementTree.SubElement(vertex, "neighborhood")
            for neighbor in v.neighborhood:
                neighbor_id = ElementTree.SubElement(vertex_neighbors, "neighbor_id")
                neighbor_id.text = str(neighbor.id) 
        
        if not name.endswith('.grape'):
            name += '.grape'

        f = gzip.open(name, 'wb')
        f.write(ElementTree.tostring(grape))
        f.close()

        self.file_chooser_dialog_close()


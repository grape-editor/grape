import gtk
import os
import sys
import locale
import gettext

class VertexEdit(object):
    def __init__(self, builder, area, vertex, set_changed):
        path = os.path.dirname(__file__)
        path = os.path.join(path, "edit.ui")

        self.vertex = vertex
        self.area = area
        self.set_changed = set_changed

        self.builder = builder
        self.builder.add_from_file(path)

        self.screen = self.builder.get_object("vertex_edit")
        self.label_id = self.builder.get_object("label_id")
        self.text_title = self.builder.get_object("text_title")
        self.spin_posx = self.builder.get_object("spin_posx")
        self.spin_posy = self.builder.get_object("spin_posy")
        self.color_vertex = self.builder.get_object("color_vertex")
        self.color_border = self.builder.get_object("color_border")
        self.adjustment_radius = self.builder.get_object("adjustment_radius")
        self.adjustment_border = self.builder.get_object("adjustment_border")

        self.treeview_edges = self.builder.get_object("treeview_edges")
        self.liststore_edges = self.builder.get_object("liststore_edges")

        self.init_general_fields()
        self.init_edges_fields()
        
        self.builder.connect_signals(self) 
        self.screen.show_all()

    def init_general_fields(self):
        self.label_id.set_label(str(self.vertex.id))
        self.text_title.set_text(self.vertex.title)
        self.spin_posx.set_value(self.vertex.position[0])
        self.spin_posy.set_value(self.vertex.position[1])
        
        self.color_vertex.set_color(self.cairo_to_spin(self.vertex.fill_color))
        self.color_border.set_color(self.cairo_to_spin(self.vertex.border_color))       
        
        self.adjustment_radius.value = self.vertex.size
        self.adjustment_border.value = self.vertex.border_size

    def init_edges_fields(self):
        number_of_edges = len(self.vertex.adjacencies)
       
        for i in range(number_of_edges):
            t_id = self.vertex.adjacencies[i].id
            t_start = self.vertex.adjacencies[i].start.id
            t_end = self.vertex.adjacencies[i].end.id
            t_test = "teste"

            self.liststore_edges.append([t_id, t_start, t_end, t_test])



    def cairo_to_spin(self, color):
        return gtk.gdk.Color(color[0] * 65535, color[1] * 65535, color[2] * 65535)
        
    def spin_to_cairo(self, color):
        return [color.red / 65535.0, color.green / 65535.0, color.blue / 65535.0]

    def title_changed(self, widget):
        self.vertex.title = self.text_title.get_text()
        self.area.queue_draw()
        self.set_changed(True)
        
    def positionx_changed(self, widget):
        self.vertex.position[0] = self.spin_posx.get_value()
        self.area.queue_draw()
        self.set_changed(True)
    
    def positiony_changed(self, widget):
        self.vertex.position[1] = self.spin_posy.get_value()
        self.area.queue_draw()
        self.set_changed(True)
    
    def color_vertex_changed(self, widget):
        self.vertex.fill_color = self.spin_to_cairo(widget.get_color())
        self.area.queue_draw()
        self.set_changed(True)
        
    def color_border_changed(self, widget):
        self.vertex.border_color = self.spin_to_cairo(widget.get_color())
        self.area.queue_draw()
        self.set_changed(True)
    
    def radius_scale_changed(self, widget):
        self.vertex.size = widget.value
        self.area.queue_draw()
        self.set_changed(True)
    
    def border_scale_changed(self, widget):
        self.vertex.border_size = widget.value
        self.area.queue_draw()
        self.set_changed(True)
    
    def close(self, widget):
        self.screen.destroy()


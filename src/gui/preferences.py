import gtk
import os
import sys
import locale
import gettext


class Preferences(object):
    def __init__(self, config):
        path = os.path.dirname(__file__)
        path = os.path.join(path, "preferences.ui")

        self.logger = config.logger
        self.config = config

        self.builder = gtk.Builder()
        self.builder.add_from_file(path)

        self.logger.info("Creating preferences GUI")
        self.preferences = self.builder.get_object("preferences")

        self.builder.connect_signals(self)

        self.get_preferences()

        self.preferences.show_all()

    def get_preferences(self):
        self.liststore_types = gtk.ListStore(str)

        self.graph_type = self.builder.get_object("graph_type")
        self.graph_type.set_model(self.liststore_types)

        renderer = gtk.CellRendererText()
        self.graph_type.pack_start(renderer)
        self.graph_type.add_attribute(renderer, "text", 0)

        self.liststore_types.append([_('Graph')])
        self.liststore_types.append([_('DiGraph')])
        self.liststore_types.append([_('MultiGraph')])
        self.liststore_types.append([_('MultiDiGraph')])

        self.graph_color = self.builder.get_object("graph_color")
        self.graph_title = self.builder.get_object("graph_title")
        self.vertex_color = self.builder.get_object("vertex_color")
        self.vertex_border_color = self.builder.get_object("vertex_color_border")
        self.vertex_adjustment_radious = self.builder.get_object("adjustment_vertex_radious")
        self.vertex_adjustment_border = self.builder.get_object("adjustment_vertex_border")
        self.edge_color = self.builder.get_object("edge_color")
        self.edge_adjustment_width = self.builder.get_object("adjustment_edge_width")

        graph_color = self.config.get('graph', 'background-color', '#000000')
        graph_title = self.config.get('graph', 'title', 'Untitled')

        vertex_color = self.config.get('vertex', 'color', '#FFFFFF')
        vertex_border_color = self.config.get('vertex', 'border-color', '#000000')
        vertex_radious = self.config.get('vertex', 'radious', 30)

    def vertex_radious_changed(self, widget):
        self.config.set('vertex', 'radious', widget.value)

    def vertex_border_changed(self, widget):







        self.graph_color.set_color(gtk.gdk.color_parse(graph_color))
        self.graph_title.set_text(graph_title)
        self.vertex_color.set_color(gtk.gdk.color_parse(vertex_color))
        self.vertex_border_color.set_color(gtk.gdk.color_parse(vertex_border_color))
        self.vertex_radious.value = vertex_radious
 









    def graph_type_changed(self, widget):
        self.liststore_types.get_value(widget.get_active_iter(), 0)
        self.config.set('graph', 'type', text)

    def graph_color_changed(self, widget):
        self.config.set('graph', 'background-color', widget.get_color())

    def graph_title_changed(self, widget):
        self.config.set('graph', 'title', widget.get_text())

    def vertex_color_changed(self, widget):
        self.config.set('vertex', 'color', widget.get_color())

    def vertex_border_color_changed(self, widget):
        self.config.set('vertex', 'border-color', widget.get_color())

    def vertex_radious_changed(self, widget):
        self.config.set('vertex', 'radious', widget.value)

    def vertex_border_changed(self, widget):
        self.config.set('vertex', 'border', widget.value)

    def edge_color_changed(self, widget):
        self.config.set('edge', 'color', widget.get_color())

    def edge_width_changed(self, widget):
        self.config.set('edge', 'width', widget.value)

    def confirm(self, widget):
        self.config.save()
        self.preferences.destroy()





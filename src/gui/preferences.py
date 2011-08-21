from lib.config import Config
from lib.logger import Logger

import gtk
import os
import sys
import locale
import gettext

class Preferences(object):
    """Global preferences"""
    def __init__(self):
        """Create a interface to manipulate preferences"""
        path = os.path.dirname(__file__)
        path = os.path.join(path, "preferences.ui")

        # Get singleton from both classes
        self.config = Config()
        self.logger = Logger()

        self.builder = gtk.Builder()
        self.builder.add_from_file(path)

        self.logger.info("Creating preferences GUI")
        self.preferences = self.builder.get_object("preferences")
        self.builder.connect_signals(self)
        self.get_preferences()
        self.preferences.show_all()

    def get_preferences(self):
        """Getting preferences from a config file"""
        self.liststore_types = gtk.ListStore(str)
        self.graph_type = self.builder.get_object("graph_type")
        self.graph_type.set_model(self.liststore_types)
        renderer = gtk.CellRendererText()
        self.graph_type.pack_start(renderer)
        self.graph_type.add_attribute(renderer, "text", 0)
        self.liststore_types.append([_("Graph")])
        self.liststore_types.append([_("DiGraph")])
        self.liststore_types.append([_("MultiGraph")])
        self.liststore_types.append([_("MultiDiGraph")])

        self.graph_title = self.builder.get_object("graph_title")
        self.graph_color = self.builder.get_object("graph_color")
        self.vertex_color = self.builder.get_object("vertex_color")
        self.vertex_border_color = self.builder.get_object("vertex_border_color")
        self.vertex_adjustment_radious = self.builder.get_object("adjustment_vertex_radious")
        self.vertex_adjustment_border = self.builder.get_object("adjustment_vertex_border")
        self.edge_color = self.builder.get_object("edge_color")
        self.edge_adjustment_width = self.builder.get_object("adjustment_edge_width")

        # Setting attributes that was got above to set in interface objects
        self.graph_title.set_text(self.config.get("graph", "title"))
        possibles_types = [_("Graph"), _("DiGraph"), _("MultiGraph"), _("MultiDiGraph")]
        graph_type = self.config.get("graph", "type")
        for current in possibles_types:
            if graph_type == current:
                self.graph_type.set_active(possibles_types.index(current))
                break
        self.graph_color.set_color(gtk.gdk.Color(self.config.get("graph", "background-color")))
        self.vertex_color.set_color(gtk.gdk.Color(self.config.get("vertex", "fill-color")))
        self.vertex_border_color.set_color(gtk.gdk.Color(self.config.get("vertex", "border-color")))
        self.vertex_adjustment_radious.set_value(float(self.config.get("vertex", "size")))
        self.vertex_adjustment_border.set_value(float(self.config.get("vertex", "border-size")))
        self.edge_color.set_color(gtk.gdk.Color(self.config.get("edge", "color")))
        self.edge_adjustment_width.set_value(float(self.config.get("edge", "width")))

    def graph_type_changed(self, widget):
        text = self.liststore_types.get_value(widget.get_active_iter(), 0)
        self.config.set("graph", "type", text)

    def graph_color_changed(self, widget):
        self.config.set("graph", "background-color", widget.get_color())

    def graph_title_changed(self, widget):
        self.config.set("graph", "title", widget.get_text())

    def vertex_color_changed(self, widget):
        self.config.set("vertex", "fill-color", widget.get_color())

    def vertex_border_color_changed(self, widget):
        self.config.set("vertex", "border-color", widget.get_color())

    def vertex_radious_changed(self, widget):
        self.config.set("vertex", "size", widget.value)

    def vertex_border_changed(self, widget):
        self.config.set("vertex", "border-size", widget.value)

    def edge_color_changed(self, widget):
        self.config.set("edge", "color", widget.get_color())

    def edge_width_changed(self, widget):
        self.config.set("edge", "width", widget.value)

    def confirm(self, widget):
        self.config.save()
        self.preferences.destroy()


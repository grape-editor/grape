import gtk.gdk
import os


class AboutShow(object):

    def __init__(self, builder):
        current_path = os.path.dirname(__file__)
        path = os.path.join(current_path, "show.ui")
        builder.add_from_file(path)
        builder.connect_signals(self)

        self.about_show = builder.get_object("about_show")
        path = os.path.join(current_path, "..", "..", "..", "..")
        path = os.path.join(path, "resources", "images", "logo.png")
        logo = gtk.gdk.pixbuf_new_from_file(path)

        self.about_show.set_logo(logo)

        self.about_show.show_all()

    def response(self, widget, event):
        self.about_show.destroy()


import gtk.gdk
import os


class About(object):

    def __init__(self):
        self.builder = gtk.Builder()
        current_path = os.path.dirname(__file__)
        path = os.path.join(current_path, "about.ui")
        self.builder.add_from_file(path)
        self.builder.connect_signals(self)

        self.about_show = self.builder.get_object("about_show")
        path = os.path.join(current_path, "..", "..")
        print path
        path = os.path.join(path, "resources", "images", "logo.png")
        logo = gtk.gdk.pixbuf_new_from_file(path)

        self.about_show.set_logo(logo)
        self.about_show.show_all()

    def response(self, widget, event):
        self.about_show.destroy()


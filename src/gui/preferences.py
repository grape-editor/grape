import gtk
import os
import sys
import locale
import gettext


class Preferences(object):
    def __init__(self, builder):
        path = os.path.dirname(__file__)
        path = os.path.join(path, "preferences.ui")

        self.builder = builder
        self.builder.add_from_file(path)

        self.preferences = self.builder.get_object("preferences")

        self.preferences.show_all()

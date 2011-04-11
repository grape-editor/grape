import gtk
import os
import sys
import locale
import gettext

class VertexEdit(object):
    def __init__(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, "edit.ui")
        
        self.builder = gtk.Builder()
        self.domain = self.translate()
        self.builder.set_translation_domain(self.domain)
        
        self.builder.add_from_file(path)
        self.builder.connect_signals(self)

        self.screen = self.builder.get_object("vertex_edit")
        self.screen.show_all()
        
    def translate(self):
        domain = "grape"
        current_path = os.path.dirname(__file__)
        locale_path = os.path.join(current_path, "..", "..", "..", "config", "locale")

        langs = []
        lc, encoding = locale.getdefaultlocale()

        if (lc):
            langs = [lc]

        language = os.environ.get('LANGUAGE', None)

        if (language):
            langs += language.split(":")

        # TODO - Configuration file
        langs += ["pt_BR", "en_US"]

        gettext.bindtextdomain(domain, locale_path)
        gettext.textdomain(domain)
        lang = gettext.translation(domain, locale_path, languages=langs, fallback = True)

        gettext.install(domain, locale_path)

        return domain
    
    def close(self, widget):
        self.screen.destroy()


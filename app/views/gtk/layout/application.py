from app.views.gtk.screen.show import ScreenShow
import gtk
import os
import sys
import locale
import gettext

class ApplicationLayout(object):

    def __init__(self):
        self.screens = []
        self.builder = gtk.Builder()
        self.domain = self.translate()
        self.builder.set_translation_domain(self.domain)

        gtk.notebook_set_window_creation_hook(self.screen_create, None)
        self.screen_create()
        gtk.main()

    def screen_create(self, source=None, page=None, x=None, y=None, user_data=None):
        screen = ScreenShow(self.builder, page != None)
        if x and y:
            screen.move_screen(x, y)

        screen.screen.connect('destroy', self.screen_deleted)
        self.screens.append(screen.screen)

        return screen.notebook

    def screen_deleted(self, widget):
        self.screens.remove(widget)

        if len(self.screens) == 0:
            gtk.main_quit()

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


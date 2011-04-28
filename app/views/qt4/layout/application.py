from app.views.qt4.screen.show_ui import Ui_ScreenShow

from PyQt4 import QtCore, QtGui
import os
import sys
import locale
import gettext

class ApplicationLayout(object):

    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)

        self.screens = []
        self.domain = self.translate()

        self.screen_create()
        
        sys.exit(self.app.exec_())

    def screen_create(self):
        screen = QtGui.QMainWindow()
        ui = Ui_ScreenShow()
        ui.setupUi(screen)
        screen.show()

        self.screens.append(screen)

        return screen

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



"""
    def screen_deleted(self, widget, event):
        screen = widget.parent_screen

        for i in range(screen.notebook.get_n_pages()):
            tab = screen.notebook.get_nth_page(0)
            if not screen.close_tab(tab):
                return True

        if screen.notebook.get_n_pages() > 0:
            return True

        self.screens.remove(widget)

        if len(self.screens) == 0:
            gtk.main_quit()

        return False
"""

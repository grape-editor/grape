from Window import Window
import gtk
import os
import sys
import locale
import gettext  

class MainScreen(object):
    windows = []
    dialogs = []
    
    def __init__(self):
    
        self.builder = gtk.Builder()
        self.domain = self.translate()
        self.builder.set_translation_domain(self.domain)
        
        gtk.notebook_set_window_creation_hook(self.window_create, None)   
        self.window_create()
        gtk.main()
        
    def window_create(self, source=None, page=None, x=None, y=None, user_data=None):
        new_window = Window(self.builder)
        if x and y:
            new_window.window_move_screen(x, y)
        new_window.window.connect('delete-event', self.window_deleted)
        self.windows.append(new_window.window)
        return new_window.notebook

    def window_deleted(self, window, event):
        self.windows.remove(window)
        if self.windows == []:
            gtk.main_quit()

    def translate(self):   
        domain = "grape"
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        language_path = os.path.join(base_path, "language")
         
        locale.setlocale(locale.LC_ALL, '')
        locale.bindtextdomain(domain, language_path)
         
        gettext.bindtextdomain(domain, language_path)
        gettext.textdomain(domain)
        gettext.translation(domain, language_path)
        gettext.install(domain, language_path)
        return domain



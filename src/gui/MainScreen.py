from Window import Window
import gtk

class MainScreen(object):
    windows = []
    dialogs = []
    
    def __init__(self):
        gtk.notebook_set_window_creation_hook(self.window_create, None)   
        self.window_create()
        gtk.main()
        
    def window_create(self, source=None, page=None, x=None, y=None, user_data=None):
        new_window = Window()
        if x and y:
            new_window.move_screen(x, y)
        new_window.window.connect('delete-event', self.window_deleted)
        self.windows.append(new_window.window)
        return new_window.notebook

    def window_deleted(self, window, event):
        self.windows.remove(window)
        if self.windows == []:
            gtk.main_quit()





import gtk.gdk
import os
import sys
import locale
import gettext    

class AboutDialog(object):  
    
    def __init__(self, builder):       
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        path = os.path.join(path, "gui", "AboutDialog.ui")        
        builder.add_from_file(path)

        builder.connect_signals(self)
        
        self.file_chooser = builder.get_object("file_chooser")
        
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        path = os.path.join(path, "images", "logo.png")
        logo = gtk.gdk.pixbuf_new_from_file(path)
        
        self.file_chooser.set_logo(logo)
        
        self.file_chooser.connect("response", self.about_dialog_response)
        self.file_chooser.show_all()

    def about_dialog_response(self, widget, event):
        self.about_dialog.destroy() 


import gtk.gdk
import os
import sys
import locale
import gettext    

class AboutDialog(object):  
    
    def __init__(self):
        #domain = self.translate()
        builder = gtk.Builder()
        #builder.set_translation_domain(domain)          
        
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
        self.file_chooser.destroy() 

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
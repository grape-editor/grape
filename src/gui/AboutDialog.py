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
        
        self.about_dialog = builder.get_object("about_dialog")
        
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        path = os.path.join(path, "images", "logo.png")
        logo = gtk.gdk.pixbuf_new_from_file(path)
        
        self.about_dialog.set_logo(logo)
        
        self.about_dialog.connect("response", self.about_dialog_response)
        self.about_dialog.show_all()

    def about_dialog_response(self, widget, event):
        self.about_dialog.destroy() 

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
import gobject
import gtk
import os
import sys
import locale
import gettext    

 
     


class SaveAs(object):  
    
    def __init__(self):
        #domain = self.translate()
        builder = gtk.Builder()
        #builder.set_translation_domain(domain)          
        
        path = os.path.abspath(os.path.dirname(sys.argv[0]))
        path = os.path.join(path, "gui", "SaveAs.ui")        
        builder.add_from_file(path)

        builder.connect_signals(self)
        
        self.file_chooser = builder.get_object("file_chooser_dialog")
        
        self.combo_box = builder.get_object("combo_box")
        
        model_scrit = gtk.ListStore(str)
        model_scrit.append(["Value 1"])
        model_scrit.append(["Value 2"])
        model_scrit.append(["Value 3"])
        model_scrit.append(["Value 4"])
        self.combo_box.set_model(model_scrit)
        
        cell = gtk.CellRendererText()
        self.combo_box.pack_start(cell)
        self.combo_box.add_attribute(cell,'text',0)
        self.combo_box.set_active(0)
        
        
        self.combo_box.set_row_span_column(10)
        self.combo_box.set_column_span_column(1)
        print self.combo_box.get_row_span_column()
        print self.combo_box.get_column_span_column()


        
        self.file_chooser.connect("response", self.about_dialog_response)
        self.file_chooser.show_all()

    def about_dialog_response(self, widget, event):
        print event
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
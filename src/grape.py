import gtk 
import pygtk

import sys
import getopt


def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    #for arg in args:
    #    process(arg) # process() is defined elsewhere

if __name__ == "__main__":
    main()
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    builder = gtk.Builder() 
    builder.add_from_file("gui/gtkui/main.ui") 
        
        
    window = builder.get_object("main")

    window.show_all()

    gtk.main()

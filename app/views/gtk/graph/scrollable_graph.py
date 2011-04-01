import gtk

class ScrollableGraph(gtk.Table):

    def __init__(self):
        gtk.Table.__init__(self)

        self.hadjustment = gtk.Adjustment(0, 0, 0, 0, 0, 0)
        self.vadjustment = gtk.Adjustment(0, 0, 0, 0, 0, 0)

        self.vbox = gtk.VBox(False, 0)
        self.hadjustment.connect('changed', self.on_hadjustment_changed)
        self.vadjustment.connect('changed', self.on_vadjustment_changed)
        self.hscrollbar = gtk.HScrollbar(self.hadjustment)
        self.vscrollbar = gtk.VScrollbar(self.vadjustment)
        self.attach(self.vbox, 0, 1, 0, 1, gtk.EXPAND|gtk.FILL, gtk.EXPAND|gtk.FILL, 0, 0)
        self.attach(self.hscrollbar, 0, 1, 1, 2, gtk.EXPAND|gtk.FILL, gtk.FILL, 0, 0)
        self.attach(self.vscrollbar, 1, 2, 0, 1, gtk.FILL, gtk.EXPAND|gtk.FILL, 0, 0)

    def add_scrollable_widget(self, widget):
        widget.set_scroll_adjustments(self.hadjustment, self.vadjustment)
        widget.connect('scroll_event', self.on_widget_scroll_event)
        widget.set_size_request(1, 1)
        self.vbox.pack_start(widget, True, True)

    def add_floating_widget(self, widget):
        self.vbox.pack_start(widget, True, True)
        self.vbox.reorder_child(widget, 0)

    def on_hadjustment_changed(self, event):
        # If the scrollbar is needed, show it, otherwise hide it
        if (self.hadjustment.page_size == self.hadjustment.upper):
            self.hscrollbar.hide()
        else:
            self.hscrollbar.show()

    def on_vadjustment_changed(self, event):
        # If the scrollbar is needed, show it, otherwise hide it
        if (self.vadjustment.page_size == self.vadjustment.upper):
            self.vscrollbar.hide()
        else:
            self.vscrollbar.show()

    def on_widget_scroll_event(self, widget, event):
        if ((event.direction == gtk.gdk.SCROLL_UP) or (event.direction == gtk.gdk.SCROLL_DOWN)):
            self.hadjustment.changed()
        elif ((event.direction == gtk.gdk.SCROLL_LEFT) or (event.direction == gtk.gdk.SCROLL_RIGHT)):
            self.vadjustment.changed()

        return True


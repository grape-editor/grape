from app.views.gtk.graph.show import GraphShow
from app.views.gtk.about.show import AboutShow
from app.views.gtk.file_chooser.show import FileChooserShow

import gtk
import os
import sys

class ScreenShow(object):

    def __init__(self, builder):
        path = os.path.dirname(__file__)
        path = os.path.join(path, "show.ui")

        self.builder = builder
        self.builder.add_from_file(path)
        self.builder.connect_signals(self)

        self.screen = builder.get_object("screen_show")
        self.notebook = builder.get_object("notebook")
        self.screen.connect('key_press_event', self.keyboard_press)

        self.notebook.set_scrollable(True)
        self.notebook.set_group_id(0)

        tab = GraphShow(self.tab_changed)
        self.add_notebook_tab(tab)

        self.name = 0
        self.screen.show_all()

    def current_tab(self):
        current_page_number = self.notebook.get_current_page()
        tab = self.notebook.get_nth_page(current_page_number)
        return tab, current_page_number

    def close_tab_clicked(self, widget):
        page_number = widget.get_parent().page_num(widget)
        widget.get_parent().remove_page(page_number)

    def add_notebook_tab(self, tab):
        hbox = gtk.HBox(False, 0)
        close_image = gtk.image_new_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)

        btn = gtk.Button()
        btn.set_relief(gtk.RELIEF_NONE)
        btn.set_focus_on_click(False)
        btn.add(close_image)

        style = gtk.RcStyle()
        style.xthickness = 0
        style.ythickness = 0
        btn.modify_style(style)

        hbox.pack_start(gtk.Label(tab.graph.title))
        hbox.pack_start(btn, False, False)

        self.notebook.append_page(tab, hbox)
        last_page = self.notebook.get_n_pages() - 1

        if last_page > 0:
            self.notebook.set_current_page(last_page)

        self.notebook.set_tab_reorderable(tab, True)
        self.notebook.set_tab_detachable(tab, True)

        n = self.notebook.page_num(tab)

        btn.connect_object('clicked', self.close_tab_clicked, tab)

        hbox.show_all()
        self.notebook.show_all()

        tab.close_button = btn
        self.notebook.set_current_page(n)

    def tab_changed(self, tab):
        box = self.notebook.get_tab_label(tab)
        label = box.get_children()[0]

        if tab.changed:
            label.set_label("* " + tab.graph.title)
        else:
            label.set_label(tab.graph.title)

    def menu_file_new(self, widget):
        tab = GraphShow(self.tab_changed)
        self.add_notebook_tab(tab)

    def menu_file_open(self, widget):
        tab = GraphShow(self.tab_changed)
        file_chooser = FileChooserShow(self.builder, "open")
        file_chooser.run()

        tab.graph = tab.graph.open(file_chooser.path)
        tab.changed = False

        self.add_notebook_tab(tab)

        self.tab_changed(tab)

    def menu_file_save(self, widget):
        tab, i = self.current_tab()

        if tab:
            if not tab.graph.path:
                self.menu_file_save_as(widget)
            else:
                tab.graph.save(tab.graph.path)
                tab.changed = False
                self.tab_changed(tab)

    def menu_file_save_as(self, widget):
        tab, i = self.current_tab()

        if tab and self.notebook.get_n_pages() > 0:
            file_chooser = FileChooserShow(self.builder, "save")
            file_chooser.run()

            if file_chooser.path:
                tab.graph.save(file_chooser.path)

                tab.changed = False
                self.tab_changed(tab)

    def menu_file_revert(self, widget):
        tab, i = self.current_tab()

        if tab and self.notebook.get_n_pages() > 0:
            print tab.graph.path
            tab.graph = tab.graph.open(tab.graph.path)
            tab.changed = False
            self.tab_changed(tab)

        tab.draw()

    def menu_file_close(self, widget):
        tab, i = self.current_tab()

        if tab and self.notebook.get_n_pages() > 0:
            self.notebook.remove_page(i)
            tab.destroy()

    def menu_file_quit(self, widget):
        self.main_quit(widget)

    def menu_edit_cut(self, widget):
        # TODO - Cut
        pass

    def menu_edit_copy(self, widget):
        # TODO - Copy
        pass

    def menu_edit_paste(self, widget):
        # TODO - Paste
        pass

    def menu_edit_add_vertex(self, widget):
        tab, i = self.current_tab()

        if tab:
            tab.action = "add_vertex"

    def menu_edit_remove_vertex(self, widget):
        tab, i = self.current_tab()

        if tab:
            tab.action = "remove_vertex"

    def menu_edit_add_edge(self, widget):
        tab, i = self.current_tab()

        if tab:
            tab.action = "add_edge"

    def menu_edit_remove_edge(self, widget):
        tab, i = self.current_tab()

        if tab:
            tab.action = "remove_edge"

    def menu_edit_delete(self, widget):
        # TODO - Handle delete keypress
        pass

    def menu_view_fullscreen_on(self, widget):
        # TODO - Fullscreen mode
        pass

    def menu_view_fullscreen_off(self, widget):
        # TODO - Fullscreen mode
        pass

    def menu_help_about(self, widget):
        AboutShow(self.builder)

    def keyboard_press(self, widget, event):
        tab, i = self.current_tab()

        key = event.keyval
        direction = None

        if key == gtk.keysyms.Right:
            direction = "right"
        elif key == gtk.keysyms.Left:
            direction = "left"
        elif key == gtk.keysyms.Up:
            direction = "up"
        elif key == gtk.keysyms.Down:
            direction = "down"

        if tab and direction:
            tab.controlelr.move_selection(tab.graph, direction)

    def move_screen(self, x, y):
        self.screen.move(x, y)

    def main_quit(self, widget):
        self.screen.destroy()


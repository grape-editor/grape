from app.views.gtk.graph.show import GraphShow
from app.views.gtk.about.show import AboutShow
from app.views.gtk.file_chooser.show import FileChooserShow

import gtk
import os
import sys

class ScreenShow(object):

    def __init__(self, builder, hook=False):
        path = os.path.dirname(__file__)
        path = os.path.join(path, "show.ui")

        self.builder = builder
        self.builder.add_from_file(path)
        self.builder.connect_signals(self)

        self.screen = builder.get_object("screen_show")
        self.notebook = builder.get_object("notebook")

        self.screen.connect('key_press_event', self.keyboard_press)
        self.screen.parent_screen = self

        self.notebook.set_scrollable(True)
        self.notebook.set_group_id(0)

        if not hook:
            tab = GraphShow(self.builder, self.tab_changed)
            self.add_notebook_tab(tab)

        self.name = 0
        self.screen.show_all()

    def close_tab(self, tab):
        page_number = tab.get_parent().page_num(tab)

        if tab.changed:
            self.notebook.set_current_page(page_number)
            title = _("Save changes?")
            message_prefix = _("Your file")
            message_suffix = _("has been changed.\nDo you save its changes?")
            message = message_prefix + " \"" + tab.graph.title + "\" " + message_suffix
            dialog = gtk.MessageDialog(parent=self.screen, flags=gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_MODAL, type=gtk.MESSAGE_WARNING, message_format=message)
            dialog.set_title(title)

            save = gtk.STOCK_SAVE_AS
            if tab.graph.path:
                save = gtk.STOCK_SAVE

            dialog.add_buttons(gtk.STOCK_NO, gtk.RESPONSE_NO)
            dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
            dialog.add_buttons(save, gtk.RESPONSE_YES)

            dialog.show_all()
            response = dialog.run()
            dialog.destroy()

            if response == gtk.RESPONSE_CANCEL:
                return False
            elif response == gtk.RESPONSE_YES:
                self.menu_file_save(None)

                if tab.changed:
                    return False

        tab.get_parent().remove_page(page_number)
        return True

        # number_of_pages = widget.get_parent().get_n_pages() - 1
        # if number_of_pages == 0:
        #    self.main_quit(widget)

    def current_tab(self):
        current_page_number = self.notebook.get_current_page()
        tab = self.notebook.get_nth_page(current_page_number)
        return tab, current_page_number

    def close_tab_clicked(self, widget):
        self.close_tab(widget)

    def tab_switched(self, widget, tab, page_number):
        menu_file_revert = self.builder.get_object("menu_file_revert")
        tab, page_number = self.current_tab()

        if tab.changed and tab.graph.path:
            menu_file_revert.set_sensitive(True)
        else:
            menu_file_revert.set_sensitive(False)

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
        tab.box = hbox
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
        box = tab.box
        label = box.get_children()[0]

        menu_file_revert = self.builder.get_object("menu_file_revert")

        if tab.changed:
            label.set_label("* " + tab.graph.title)

            if tab.graph.path:
                menu_file_revert.set_sensitive(True)
        else:
            label.set_label(tab.graph.title)
            menu_file_revert.set_sensitive(False)

    def menu_file_new(self, widget):
        tab = GraphShow(self.builder, self.tab_changed)
        self.add_notebook_tab(tab)

    def menu_file_open(self, widget):
        tab = GraphShow(self.builder, self.tab_changed)
        file_chooser = FileChooserShow(self.builder, "open")
        file_chooser.run()

        if file_chooser.path:
            tab.graph = tab.graph.open(file_chooser.path)
            tab.area.graph = tab.graph
            tab.changed = False

            self.add_notebook_tab(tab)

            self.tab_changed(tab)
        else:
            del tab

        del file_chooser

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

            del file_chooser

    def menu_file_revert(self, widget):
        tab, page_number = self.current_tab()

        if tab.changed:
            self.notebook.set_current_page(page_number)
            title = _("Revert changes?")
            message_prefix = _("Revert unsaved changes to document")
            message_suffix = _("?")
            message = message_prefix + " \"" + tab.graph.title + "\" " + message_suffix
            dialog = gtk.MessageDialog(parent=self.screen, flags=gtk.DIALOG_DESTROY_WITH_PARENT | gtk.DIALOG_MODAL, type=gtk.MESSAGE_QUESTION, message_format=message)
            dialog.set_title(title)

            dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
            dialog.add_buttons(gtk.STOCK_REVERT_TO_SAVED, gtk.RESPONSE_YES)

            dialog.show_all()
            response = dialog.run()
            dialog.destroy()

            if response == gtk.RESPONSE_CANCEL:
                return False
            elif response == gtk.RESPONSE_YES:
                if tab.graph.path:
                    tab.graph = tab.graph.open(tab.graph.path)
                    tab.area.graph = tab.graph
                    tab.changed = False
                    self.tab_changed(tab)
                    tab.queue_draw()

                return True


    def menu_file_close(self, widget):
        tab, i = self.current_tab()

        if tab and self.notebook.get_n_pages() > 0:
            self.close_tab(tab)

    def menu_file_quit(self, widget):
        self.screen.event(gtk.gdk.Event(gtk.gdk.DELETE))
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

    def menu_edit_delete(self, widget):
        # TODO - Handle delete keypress
        pass

    def menu_edit_undo(self, widget):
        tab, i = self.current_tab()
        tab.undo()
        
    def menu_edit_redo(self, widget):
        tab, i = self.current_tab()
        tab.redo()

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
            tab.add_edge()

    def menu_edit_remove_edge(self, widget):
        tab, i = self.current_tab()

        if tab:
            tab.action = "remove_edge"

    def menu_view_zoom_in(self, widget):
        tab, i = self.current_tab()
        tab.zoom_in()

    def menu_view_zoom_out(self, widget):
        tab, i = self.current_tab()
        tab.zoom_out()

    def menu_view_zoom_default(self, widget):
        tab, i = self.current_tab()
        tab.zoom_default()

    def menu_view_fullscreen(self, widget):
        if widget.get_active():
            self.screen.fullscreen()
        else:
            self.screen.unfullscreen()


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
        elif key == gtk.keysyms.Escape:
            if tab.action:
                tab.action = None
            else:
                tab.controller.clear_selection(tab.graph)

        if tab and direction:
            tab.controller.move_selection(tab.graph, direction)

        if tab:
            tab.queue_draw()

    def move_screen(self, x, y):
        self.screen.move(x, y)

    def main_quit(self, widget):
        self.screen.destroy()


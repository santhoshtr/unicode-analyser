#!/usr/bin/python3

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib
import unicodedata as ucd


class AnalyserWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_default_size(400, 400)

        grid = Gtk.Grid()
        self.add(grid)

        self.entry = Gtk.Entry()
        self.entry.set_text("മലയാളം")

        grid.attach(self.entry, 0, 0, 8, 1)
        button = Gtk.Button.new_with_label("Analyse")
        button.connect("clicked", self.on_click_me_clicked)

        grid.attach(button, 8, 0, 12, 1)
        self.liststore = Gtk.ListStore(str, str, str, str)


        treeview = Gtk.TreeView(model=self.liststore)

        char_text = Gtk.CellRendererText()
        char_column_text = Gtk.TreeViewColumn("Character",  char_text, text=0)
        treeview.append_column(char_column_text)

        renderer_text = Gtk.CellRendererText()
        codepoint_column_text = Gtk.TreeViewColumn("Codepoint", renderer_text, text=1)
        treeview.append_column(codepoint_column_text)

        renderer_text = Gtk.CellRendererText()
        category_column_text = Gtk.TreeViewColumn("Category", renderer_text, text=2)
        treeview.append_column(category_column_text)

        renderer_text = Gtk.CellRendererText()
        name_column_text = Gtk.TreeViewColumn("Name", renderer_text, text=3)
        treeview.append_column(name_column_text)

        grid.attach(treeview, 0, 1, 12, 2)
        grid.show()

    def on_click_me_clicked(self, button):
        self.liststore.clear()
        text = self.entry.get_text()
        for c in text:
            self.liststore.append([c, "%04x" % ord(c), ucd.category(c), ucd.name(c)])



class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        Gtk.Application.__init__(self,
                application_id="org.gnome.example",
                flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.window = None
        self.connect("activate", self.do_activate)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = AnalyserWindow(application=self, title="Unicode analyser")
        self.add_window(self.window)
        self.window.show_all()

    def on_quit(self, action, param):
        self.quit()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)

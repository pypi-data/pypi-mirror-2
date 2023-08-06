"""
Basic stuff for toplevel windows.
"""

import os.path
import pkg_resources

import gtk

from zope import interface
from interfaces import IUIComponent
from gaphor.core import inject


ICONS = (
    'gaphor-24x24.png',
    'gaphor-48x48.png',
    'gaphor-96x96.png',
    'gaphor-256x256.png',
)

class ToplevelWindow(object):

    interface.implements(IUIComponent)

    menubar_path = ''
    toolbar_path = ''
    resizable = True

    def __init__(self):
        self.window = None

    def construct(self):

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(self.title)
        self.window.set_size_request(*self.size)
        self.window.set_resizable(self.resizable)

        # set default icons of gaphor windows
        icon_dir = os.path.abspath(pkg_resources.resource_filename('gaphor.ui', 'pixmaps'))
        icons = (gtk.gdk.pixbuf_new_from_file(os.path.join(icon_dir, f)) for f in ICONS)
        self.window.set_icon_list(*icons)

        self.window.add_accel_group(self.ui_manager.get_accel_group())

        
        if self.menubar_path or self.toolbar_path:
            # Create a full featured window.
            vbox = gtk.VBox()
            self.window.add(vbox)
            vbox.show()

            menubar = self.ui_manager.get_widget(self.menubar_path)
            if menubar:
                vbox.pack_start(menubar, expand=False)
            
            toolbar = self.ui_manager.get_widget(self.toolbar_path)
            if toolbar:
                vbox.pack_start(toolbar, expand=False)

            vbox.pack_end(self.ui_component(), expand=self.resizable)
            vbox.show()
            # TODO: add statusbar
        else:
            # Create a simple window.
            self.window.add(self.ui_component())
        self.window.show()


class UtilityWindow(ToplevelWindow):

    gui_manager = inject('gui_manager')

    resizable = False

    def construct(self):
        super(UtilityWindow, self).construct()

        main_window = self.gui_manager.main_window.window
        self.window.set_transient_for(main_window)
        #self.window.set_keep_above(True)
        self.window.set_property('skip-taskbar-hint', True)
        self.window.set_position(gtk.WIN_POS_MOUSE)
        self.window.show()
       #self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)


# vim:sw=4:et:ai

"""
"""

import gtk
import gaphas


class DiagramView(gaphas.GtkView):
    """
    Displays a diagram (canvas) in a widget.

    See also: DiagramTab
    """

    TARGET_STRING = 0
    TARGET_ELEMENT_ID = 1
    TARGET_TOOLBOX_ACTION = 2
    DND_TARGETS = [
        ('gaphor/element-id', 0, TARGET_ELEMENT_ID),
        ('gaphor/toolbox-action', 0, TARGET_TOOLBOX_ACTION)]

    __gtype_name__ = 'GaphorDiagramView'

    def __init__(self, diagram=None):
        super(DiagramView, self).__init__(diagram and diagram.canvas)
        self.diagram = diagram
        self.canvas = diagram.canvas

        # Drop
        self.drag_dest_set (gtk.DEST_DEFAULT_ALL, DiagramView.DND_TARGETS,
                            gtk.gdk.ACTION_COPY | gtk.gdk.ACTION_LINK)


# vim: sw=4:et

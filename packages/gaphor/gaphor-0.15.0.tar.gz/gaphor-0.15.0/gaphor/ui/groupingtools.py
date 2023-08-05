from zope import component

import gtk

from gaphor.diagram.interfaces import IGroup
from gaphor.ui.diagramtools import PlacementTool
from gaphas.tool import ItemTool

# cursor to indicate grouping
IN_CURSOR = gtk.gdk.Cursor(gtk.gdk.DIAMOND_CROSS)

# cursor to indicate ungrouping
OUT_CURSOR = gtk.gdk.Cursor(gtk.gdk.SIZING)

class GroupPlacementTool(PlacementTool):
    """
    Try to group items when placing them on diagram.
    """

    def __init__(self, view, item_factory, after_handler=None, handle_index=-1):
        super(GroupPlacementTool, self).__init__(view,
                item_factory, after_handler, handle_index)
        self._parent = None
        self._adapter = None


    def on_motion_notify(self, event):
        """
        Change parent item to dropzone state if it can accept diagram item
        object to be created.
        """
        view = self.view
        parent = None
        self._adapter = None

        if view.focused_item:
            view.unselect_item(view.focused_item)
            view.focused_item = None

        try:
            parent = view.get_item_at_point((event.x, event.y))
        except KeyError:
            # No bounding box yet.
            return

        self._parent = parent

        if parent:
            adapter = component.queryMultiAdapter((parent, self._factory.item_class()), IGroup)
            if adapter and adapter.can_contain():
                view.dropzone_item = parent
                view.window.set_cursor(IN_CURSOR)
                self._adapter = adapter
            else:
                view.dropzone_item = None
                view.window.set_cursor(None)
                self._parent = None
            parent.request_update(matrix=False)
        else:
            if view.dropzone_item:
                view.dropzone_item.request_update(matrix=False)
            view.dropzone_item = None
            view.window.set_cursor(None)


    def _create_item(self, pos, **kw):
        """
        Create diagram item and place it within parent's boundaries.
        """
        parent = self._parent
        view = self.view
        try:
            if parent and self._adapter:
                kw['parent'] = parent

            item = super(GroupPlacementTool, self)._create_item(pos, **kw)

            if parent and item and self._adapter:
                self._adapter.item = item
                self._adapter.group()

                canvas = view.canvas
                parent.request_update(matrix=False)
        finally:
            self._parent = None
            view.dropzone_item = None
            view.window.set_cursor(None)
        return item


class GroupItemTool(ItemTool):
    """
    Group diagram item by dropping it on another item.

    Works only for one selected item, now.
    """

    def on_motion_notify(self, event):
        """
        Indicate possibility of grouping/ungrouping of selected item.
        """
        super(GroupItemTool, self).on_motion_notify(event)
        view = self.view

        if event.state & gtk.gdk.BUTTON_PRESS_MASK and len(view.selected_items) == 1:
            item = list(view.selected_items)[0]
            parent = view.canvas.get_parent(item)

            over = view.get_item_at_point((event.x, event.y), selected=False)
            assert over is not item

            if over is parent: # do nothing when item is over parent
                view.dropzone_item = None
                view.window.set_cursor(None)
                return

            if parent and not over:  # are we going to remove from parent?
                adapter = component.queryMultiAdapter((parent, item), IGroup)
                if adapter:
                    view.window.set_cursor(OUT_CURSOR)
                    view.dropzone_item = parent
                    parent.request_update(matrix=False)

            if over:       # are we going to add to parent?
                adapter = component.queryMultiAdapter((over, item), IGroup)
                if adapter and adapter.can_contain():
                    view.dropzone_item = over
                    view.window.set_cursor(IN_CURSOR)
                    over.request_update(matrix=False)


    def on_button_release(self, event):
        """
        Group item if it is dropped on parent's item. Ungroup item if it is
        moved out of its parent boundaries. Method also moves item from old
        parent to new one (regrouping).
        """
        super(GroupItemTool, self).on_button_release(event)
        view = self.view
        try:
            if event.button == 1 and len(view.selected_items) == 1:
                item = list(view.selected_items)[0]
                parent = view.canvas.get_parent(item)
                over = view.get_item_at_point((event.x, event.y), selected=False)
                assert over is not item

                if over is parent:
                    if parent is not None:
                        parent.request_update(matrix=False)
                    return

                if parent: # remove from parent
                    adapter = component.queryMultiAdapter((parent, item), IGroup)
                    if adapter:
                        adapter.ungroup()

                        canvas = view.canvas
                        canvas.reparent(item, None)

                        # reset item's position
                        px, py = canvas.get_matrix_c2i(parent).transform_point(0, 0)
                        item.matrix.translate(-px, -py)
                        parent.request_update()


                if over: # add to over (over becomes parent)
                    adapter = component.queryMultiAdapter((over, item), IGroup)
                    if adapter and adapter.can_contain():
                        adapter.group()

                        canvas = view.canvas
                        canvas.reparent(item, over)

                        # reset item's position
                        x, y = canvas.get_matrix_i2c(over).transform_point(0, 0)
                        item.matrix.translate(-x, -y)
                        over.request_update()
        finally:
            item = view.dropzone_item
            view.dropzone_item = None
            view.window.set_cursor(None)
            if item:
                item.request_update()


# vim:sw=4:et:ai

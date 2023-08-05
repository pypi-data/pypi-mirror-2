# Copyright (c) 2008-2009 Thomas Lotze
# See also LICENSE.txt

import gobject
import gtk
import gtk.gdk

import tl.geodrawing.controller


class GeoDrawingArea(gtk.DrawingArea):
    """A geographic pygtk drawing area.

    The drawing surface provides a geographic coordinate system and displays
    map images in the background.
    """

    __gsignals__ = {
        'viewport-changed': (gobject.SIGNAL_RUN_LAST, None, ()),
        }

    grip = None

    _immediate_update = True

    def __init__(self, *args, **kwargs):
        super(GeoDrawingArea, self).__init__(*args, **kwargs)
        self.set_size_request(64, 64)
        self.connect("expose-event", self.__expose)
        self.connect("configure-event", self.__configure)

        self.controller = tl.geodrawing.controller.GeoSurfaceController(
            self.update_rectangle)

        self.zoom = gtk.Adjustment(
            lower=0, upper=31, step_incr=1, page_incr=4)
        self.zoom.connect("value-changed", self.__zoom)

        self.longitude = gtk.Adjustment(
            lower=-180, upper=180, step_incr=1, page_incr=10)
        self.longitude.connect("value-changed", self.__longitude)

        self.latitude = gtk.Adjustment(
            lower=-90, upper=90, step_incr=1, page_incr=10)
        self.latitude.connect("value-changed", self.__latitude)

        self.add_events(gtk.gdk.SCROLL_MASK)
        self.connect('scroll-event', self.__zoom_on_scroll)

        self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.BUTTON1_MOTION_MASK |
                        gtk.gdk.POINTER_MOTION_HINT_MASK)
        self.connect('button-press-event', self.__button_press)
        self.connect('button-release-event', self.__button_release)
        self.connect('motion-notify-event', self.__motion)

    def update_rectangle(self, x0, y0, width, height):
        self.queue_draw_area(x0, y0, width, height)
        self.window.process_updates(update_children=True)

    def update_geo_bounds(self, left, bottom, right, top, margin=0):
        x0, y0 = self.controller.geo2px(left, top)
        x1, y1 = self.controller.geo2px(right, bottom)
        self.update_rectangle(
            x0-margin, y0-margin, x1-x0+2*margin, y1-y0+2*margin)

    def __zoom(self, zoom):
        self.controller.zoom = zoom.value
        if self.window and self._immediate_update:
            self.controller.update_surface()

    def __longitude(self, longitude):
        self.controller.center = (longitude.value, self.controller.center[1])
        if self.window and self._immediate_update:
            self.controller.update_surface()

    def __latitude(self, latitude):
        self.controller.center = (self.controller.center[0], latitude.value)
        if self.window and self._immediate_update:
            self.controller.update_surface()

    @staticmethod
    def __zoom_on_scroll(self, event):
        if event.direction == gtk.gdk.SCROLL_UP:
            delta = 1
        elif event.direction == gtk.gdk.SCROLL_DOWN:
            delta = -1
        else:
            return
        self.controller.zoom_rel(
            event.x, event.y, delta*self.zoom.step_increment)
        self.__update_adjustments()
        self.emit('viewport-changed')
        self.controller.update_surface()

    @staticmethod
    def __button_press(self, event):
        if event.button == 1:
            self.__grip(event)
            if event.type == gtk.gdk._2BUTTON_PRESS:
                self.__move_rel(
                    event.x, event.y,
                    self.controller.width/2, self.controller.height/2, 1)
        elif event.button == 3:
            if event.type == gtk.gdk._2BUTTON_PRESS:
                self.__move_rel(
                    event.x, event.y,
                    self.controller.width/2, self.controller.height/2, -1)

    def __grip(self, event):
        self.grip = (event.x, event.y)
        self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))

    @staticmethod
    def __button_release(self, event):
        if event.button == 1:
            return self.__release_grip(event)

    def __release_grip(self, event):
        self.grip = None
        self.window.set_cursor(None)

    @staticmethod
    def __motion(self, event):
        if event.is_hint:
            x, y, buttons = self.window.get_pointer()
        else:
            x, y = event.x, event.y
        if event.state & gtk.gdk.BUTTON1_MASK:
            return self.__move_by_grip(x, y)

    def __move_by_grip(self, x, y):
        old_x, old_y = self.grip
        self.__move_rel(old_x, old_y, x, y)

    def __move_rel(self, old_x, old_y, x, y, delta_zoom=0):
        self.controller.move_rel(x-old_x, old_y-y)
        if delta_zoom:
            self.controller.zoom_rel(
                x, y, delta_zoom*self.zoom.step_increment)
        self.grip = (x, y)
        self.__update_adjustments()
        self.emit('viewport-changed')
        self.controller.update_surface()

    @staticmethod
    def __configure(self, event):
        alloc = self.get_allocation()
        self.controller.width = alloc.width
        self.controller.height = alloc.height
        self.__update_adjustments()
        self.emit('viewport-changed')
        self.controller.update_surface()

    def __update_adjustments(self):
        self._immediate_update = False
        longitude, latitude = self.controller.center
        self.longitude.set_value(longitude)
        self.latitude.set_value(latitude)
        self.zoom.set_value(self.controller.zoom)
        self._immediate_update = True

    @staticmethod
    def __expose(self, event):
        """Redraw the cairo surface on an expose event.
        """
        self.controller.expose(self.window.cairo_create())

# Copyright (c) 2008-2009 Thomas Lotze
# See also LICENSE.txt

import gtk
import gtk.gdk
import tl.geodrawing.gtkwidget
import tl.geodrawing.tile


BLACK = gtk.gdk.Color(0, 0, 0)
RED = gtk.gdk.Color((1<<16)-1, 0, 0)


class LabeledWidget(gtk.VBox):

    def __init__(self, widget, text):
        super(LabeledWidget, self).__init__()
        label = gtk.Label(text)
        label.set_alignment(0, 0)
        self.add(label)
        self.add(widget)


class GtkDemo(object):

    def __init__(self):
        self.construct_window()

    def construct_window(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(640, 480)
        self.window.connect("delete-event", gtk.main_quit)

        hbox = gtk.HPaned()
        self.window.add(hbox)

        vbox = gtk.VBox()
        vbox.set_border_width(8)
        vbox.set_spacing(8)
        hbox.pack1(vbox, resize=False, shrink=False)
        self.geodrawingarea = tl.geodrawing.gtkwidget.GeoDrawingArea()
        hbox.pack2(self.geodrawingarea, resize=True, shrink=False)

        zoom = gtk.SpinButton(adjustment=self.geodrawingarea.zoom, digits=2)
        self.geodrawingarea.zoom.connect(
            'value-changed', self._update_widget_color, zoom,
            0, self.geodrawingarea.controller.max_zoom)
        zoom.set_width_chars(10)
        vbox.pack_start(LabeledWidget(zoom, u"Zoom level:"),
                        expand=False)

        longitude = gtk.SpinButton(adjustment=self.geodrawingarea.longitude,
                                   digits=3)
        longitude.set_width_chars(10)
        vbox.pack_start(LabeledWidget(longitude, u"Longitude of center:"),
                        expand=False)

        latitude = gtk.SpinButton(adjustment=self.geodrawingarea.latitude,
                                  digits=3)
        latitude.set_width_chars(10)
        vbox.pack_start(LabeledWidget(latitude, u"Latitude of center:"),
                        expand=False)

    def _update_widget_color(self, adjustment, widget, min_value, max_value):
        widget.style.text[gtk.STATE_NORMAL] = (
            BLACK if min_value <= adjustment.value <= max_value else RED)

    def run(self):
        self.window.show_all()
        gtk.main()


def gtkdemo(tile_cache=None):
    tl.geodrawing.tile.config['tile_cache'] = tile_cache
    GtkDemo().run()

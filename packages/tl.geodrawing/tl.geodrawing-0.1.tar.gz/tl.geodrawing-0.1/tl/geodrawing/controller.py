# Copyright (c) 2008-2010 Thomas Lotze
# See also LICENSE.txt

import cairo
import math
import tl.geodrawing.tile


class TransformSurfaceProperty(object):

    def __init__(self, func):
        self.func = func

    def __set__(self, obj, value):
        old_value = obj.__dict__[self.func.__name__]
        obj.__dict__[self.func.__name__] = value
        self.func(obj, old_value)


class GeoSurfaceController(object):
    """State and background controller for a geodrawing cairo surface.
    """

    @TransformSurfaceProperty
    def zoom(self, old_zoom):
        self.__dict__['center_xy'] = self.geo2abs(*self.center)
        scale = 2**(self.zoom - old_zoom)
        self.transform *= cairo.Matrix(xx=scale, yy=scale)
        self.transform *= cairo.Matrix(x0=self.width/2. * (1-scale),
                                       y0=self.height/2. * (1-scale))

    @TransformSurfaceProperty
    def width(self, old_width):
        self.transform *= cairo.Matrix(x0=self.width/2. - old_width/2.)

    @TransformSurfaceProperty
    def height(self, old_height):
        self.transform *= cairo.Matrix(y0=self.height/2. - old_height/2.)

    @TransformSurfaceProperty
    def center(self, old_center):
        old_x, old_y = self.center_xy
        x, y = self.geo2abs(*self.center)
        self.transform *= cairo.Matrix(x0=old_x - x, y0=y - old_y)
        self.__dict__['center_xy'] = x, y

    @TransformSurfaceProperty
    def center_xy(self, old_center_xy):
        old_x, old_y = old_center_xy
        x, y = self.center_xy
        self.transform *= cairo.Matrix(x0=old_x - x, y0=y - old_y)
        self.__dict__['center'] = self.abs2geo(x, y)

    @property
    def max_zoom(self):
        return self.tile_source.max_zoom

    def __init__(self, update_callback=lambda *args: None, tile_source=None):
        self.update_callback = update_callback
        self.__dict__.update(zoom=0,
                             width=0,
                             height=0,
                             center=(0, 0),
                             center_xy=(128, 128))
        self.transform = cairo.Matrix()
        self.surface = self.create_surface()
        self.visible_tiles = set()
        if tile_source:
            self.tile_source = tile_source
        else:
            self.tile_source = tl.geodrawing.tile.tile_source()

    def create_surface(self):
        surface = cairo.ImageSurface(
            cairo.FORMAT_RGB24, self.width, self.height)
        ctx = cairo.Context(surface)
        ctx.set_source_rgba(0.95, 0.95, 0.95, 1)
        ctx.paint()
        return surface

    def update_surface(self):
        new_surface = self.create_surface()
        ctx = cairo.Context(new_surface)
        ctx.set_matrix(self.transform)
        ctx.set_source_surface(self.surface)
        ctx.paint()
        ctx.identity_matrix()
        self.transform = cairo.Matrix()
        self.surface = new_surface
        self.update_callback(0, 0, self.width, self.height)
        for surface, x, y in self.tiles():
            ctx.set_source_surface(surface, x, y)
            ctx.paint()
            self.update_callback(x, y, 256, 256)

    def expose(self, ctx):
        ctx.set_source_surface(self.surface)
        ctx.paint()
        ctx.set_source_rgba(1, 1, 0, 0.25)
        with self.transformed_for_geo(ctx):
            for longitude in xrange(-180, 181, 45):
                ctx.move_to(longitude, -1)
                ctx.line_to(longitude, 1)
            for latitude in (-66.56, -23.44, 0, 23.44, 66.56):
                latitude = mercator(latitude)
                ctx.move_to(-180, latitude)
                ctx.line_to(180, latitude)
        ctx.stroke()
        self.draw_frame(ctx)

    def draw_frame(self, ctx):
        def center_number(x, y, number):
            text = str(number)
            text_width = ctx.text_extents(text)[4]
            ctx.move_to(x-text_width/2, y)
            ctx.show_text(text)

        ctx.save()
        ctx.identity_matrix()
        ctx.set_source_rgba(0, 0, 0, 0.25)
        ctx.rectangle(0, 0, self.width, self.height)
        ctx.stroke()
        left, top = self.px2geo(0, 0)
        right, bottom = self.px2geo(self.width-1, self.height-1)
        center_number(self.width/2., 10, top)
        center_number(self.width/2., self.height-3, bottom)
        ctx.transform(cairo.Matrix(xx=0, xy=1, yx=-1, yy=0, y0=self.height))
        center_number(self.height/2., 10, left)
        center_number(self.height/2., self.width-3, right)
        ctx.restore()

    def abs2geo(self, x, y):
        half_size = 128. * 2**self.zoom
        longitude = (x/half_size - 1) * 180
        latitude = inverse_mercator(y/half_size - 1)
        return longitude, latitude

    def px2geo(self, x, y):
        """Calculate geo coordinates at the center of a pixel.
        """
        xc, yc = self.center_xy
        x = xc + x + 0.5 - self.width/2.
        y = yc - y - 0.5 + self.height/2.
        return self.abs2geo(x, y)

    def geo2abs(self, longitude, latitude):
        half_size = 128 * 2**self.zoom
        x = half_size * (1 + longitude / 180.)
        y = half_size * (1 + mercator(latitude))
        return x, y

    def geo2px(self, longitude, latitude):
        """Calculate the pixel that contains a geo-coordinate pair.
        """
        xc, yc = self.center_xy
        x, y = self.geo2abs(longitude, latitude)
        x = self.width/2. + x - xc
        y = self.height/2. - y + yc
        return int(math.floor(x)), int(math.floor(y))

    def transform_for_geo(self, ctx):
        """Transform a cairo context to geo-coordinates.

        After this, the associated surface's pixels are addressed by an
        appropriate interval of Mercator-transformed geo-coordinates.

        """
        half_size = 128 * 2**self.zoom
        xc, yc = self.center_xy
        ctx.translate(self.width/2. - xc, self.height/2. + yc)
        ctx.scale(half_size/180., -half_size)
        ctx.translate(180, 1)

    def transformed_for_geo(self, ctx):
        """Return a GeoCoordinateCM applied to a cairo context.
        """
        return GeoCoordinateCM(self, ctx)

    def tiles(self):
        size = int(2**self.zoom)
        xc, yc = self.center_xy
        left = int(math.floor(xc - self.width/2.))
        top = int(math.floor(yc + self.height/2.))

        # assign this to self.visible_tiles only later so as not to release
        # references to tiles that remain visible too early
        visible_tiles = set()
        for i in xrange(max(left/256, 0),
                        min((left + self.width + 255)/256, size)):
            for j in xrange(max((top - self.height)/256, 0),
                            min((top + 255)/256, size)):
                try:
                    tile = self.tile_source[int(self.zoom), i, j]
                except KeyError:
                    continue
                visible_tiles.add(tile)
                # and in case the generator never finishes:
                self.visible_tiles.add(tile)
                yield (tile.surface, 256*i - left, top - 256*(j+1))
        self.visible_tiles = visible_tiles

    def view(self, x0, y0, x1, y1, padding=0):
        xc = (x0 + x1)/2.
        fraction_x = abs(x1 - x0)/360. if x0 != x1 else 1/200.
        zoom_x = math.log((self.width/256.) / fraction_x / (1 + padding), 2)

        if y0 == y1:
            yc = float(y0)
            fraction_y = 1/200.
        else:
            y0m, y1m = mercator(y0), mercator(y1)
            yc = inverse_mercator((y0m + y1m)/2.)
            fraction_y = abs(y1m - y0m)/2.
        zoom_y = math.log((self.height/256.) / fraction_y / (1 + padding), 2)

        self.center = (xc, yc)
        self.zoom = int(min(zoom_x, zoom_y))

    def move_rel(self, x, y):
        xc, yc = self.center_xy
        self.center_xy = xc - x, yc - y

    def zoom_rel(self, x, y, dz):
        xc, yc = self.width/2., self.height/2.
        self.move_rel(xc-x, y-yc)
        self.zoom += dz
        self.move_rel(x-xc, yc-y)


def mercator(latitude):
    """Mercator projection. mercator(85) is roughly 1.

    >>> abs(mercator(0)) < 1e-6
    True
    >>> mercator(85.05113)
    1.00000...
    >>> mercator(-85.05113)
    -1.00000...

    """
    return math.log(math.tan(math.pi/4 + math.radians(latitude)/2.))/math.pi


def inverse_mercator(y):
    """Inverse Mercator projection. inverse_mercator(1) is roughly 85.

    >>> abs(inverse_mercator(0)) < 1e-6
    True
    >>> inverse_mercator(1)
    85.05112...
    >>> inverse_mercator(-1)
    -85.05112...

    """
    return math.degrees(math.atan(math.sinh(y*math.pi)))


class GeoCoordinateCM(object):
    """Context manager that transforms a cairo context to geo-coordinates.

    A GeoSurfaceController applies a geo-coordinate transformation to a cairo
    context when the context manager is entered. Upon exit, the context's
    transformation matrix is reset to what it was before.

    """

    def __init__(self, controller, ctx):
        self.controller = controller
        self.ctx = ctx

    def __enter__(self):
        self.ctx.save()
        self.ctx.identity_matrix()
        self.controller.transform_for_geo(self.ctx)

    def __exit__(self, *exc_args):
        self.ctx.restore()

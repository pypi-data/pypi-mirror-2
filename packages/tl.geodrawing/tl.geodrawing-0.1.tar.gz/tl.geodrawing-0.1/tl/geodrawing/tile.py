# Copyright (c) 2008-2009 Thomas Lotze
# See also LICENSE.txt

import cairo
import os
import os.path
import tempfile
import weakref


config = dict(
    tile_cache=None,
    offline=False,
    )


# shared tile cache, hard references to the tiles used held by each client
tile_cache = weakref.WeakValueDictionary()


class Tile(object):
    """A map tile contained in a cairo image surface.

    The purpose of this wrapper class is to provide a weakly referenceable
    object to be stored in the tile cache since cairo surfaces cannot be
    weakly referenced themselves.
    """

    def __init__(self, surface):
        self.surface = surface


class TileSource(object):
    """Base class for tile sources."""

    def __init__(self, config=None, name=None):
        self.config = config
        self.name = name

    @property
    def cache(self):
        base = self.config.get('tile_cache')
        if base is None:
            base = self.config['tile_cache'] = tempfile.mkdtemp()
        cache = os.path.join(base, self.name)
        if not os.path.exists(cache):
            os.mkdir(cache)
        return cache

    def get_filename(self, zoom, x, y):
        raise NotImplementedError

    def __getitem__(self, (zoom, x, y)):
        filename = self.get_filename(zoom, x, y)
        if not filename:
            raise KeyError(zoom, x, y)
        try:
            tile = tile_cache[filename]
        except KeyError:
            surface = cairo.ImageSurface.create_from_png(filename)
            tile = tile_cache[filename] = Tile(surface)
        return tile


def tile_source():
    # XXX replace by entry-point discovery
    import tl.geodrawing.osm
    return tl.geodrawing.osm.TileSource(config=config, name='osm')

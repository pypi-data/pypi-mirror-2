# Copyright (c) 2008-2009 Thomas Lotze
# See also LICENSE.txt

from zope.testing import doctest
import manuel.codeblock
import os
import os.path
import pkg_resources
import tl.geodrawing.controller
import tl.geodrawing.tile
import tl.testing.cairo
import unittest


class TileSource(tl.geodrawing.tile.TileSource):
    """Tile source that provides some testing data."""

    max_zoom = 5

    def get_filename(self, zoom, x, y):
        filename = pkg_resources.resource_filename(
            'tl.geodrawing', 'testtiles/osm/%s-%s-%s.png' % (zoom, x, y))
        return filename if os.path.exists(filename) else None


flags = (doctest.ELLIPSIS |
         doctest.INTERPRET_FOOTNOTES |
         doctest.NORMALIZE_WHITESPACE |
         doctest.REPORT_NDIFF)


def test_suite():
    return unittest.TestSuite([
        doctest.DocTestSuite(module,
                             optionflags=flags,
                             )
        for module in (
            tl.geodrawing.controller,
            )
        ] + [
        tl.testing.cairo.DocFileSuite(filename,
                                      optionflags=flags,
                                      manuel=manuel.codeblock.Manuel()
                                      )
        for filename in sorted(os.listdir(os.path.dirname(__file__)))
        if filename.endswith(".txt")
        ])

# Copyright (c) 2008-2009 Thomas Lotze
# See also LICENSE.txt

import os.path
import tl.geodrawing.tile
import urllib2


url_opener = urllib2.build_opener()
url_opener.addheaders = [
    ("User-Agent", "Mozilla/5.0 (compatible; tl.geodrawing)")]


class TileSource(tl.geodrawing.tile.TileSource):
    """Download Mapnik-rendered Openstreetmap tiles."""

    max_zoom = 18

    url = 'http://tile.openstreetmap.org/%(z)s/%(x)s/%(y)s.png'

    over = False

    def download(self, zoom, x, y):
        if self.config.get('offline') or self.over:
            return
        try:
            return url_opener.open(
                self.url % dict(x=x, y=2**zoom-y-1, z=zoom)).read()
        except urllib2.HTTPError, e:
            if e.code == 404:
                return ""
            elif e.code != 200:
                self.over = True
        except urllib2.URLError:
            pass

    def get_filename(self, zoom, x, y):
        if zoom > self.max_zoom:
            return None

        filename = os.path.join(self.cache, "%s-%s-%s.png" % (zoom, x, y))
        if os.path.exists(filename):
            return filename if os.path.getsize(filename) else None

        image = self.download(zoom, x, y)
        if image is not None:
            target = open(filename, "w")
            target.write(image)
            target.close()

        if image:
            return filename

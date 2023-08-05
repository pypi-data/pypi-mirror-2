#!/usr/bin/env python
#
# Copyright (c) 2008-2009 Thomas Lotze
# See also LICENSE.txt

"""A geographic pygtk drawing area.

The drawing surface provides a geographic coordinate system and displays map
images in the background.
"""

import os.path
import glob
from setuptools import setup, find_packages


project_path = lambda *names: os.path.join(os.path.dirname(__file__), *names)

longdesc = "\n\n".join((open(project_path("README.txt")).read(),
                        open(project_path("ABOUT.txt")).read()))

root_files = glob.glob(project_path("*.txt"))
data_files = [("", [name for name in root_files
                    if os.path.split(name)[1] != "index.txt"])]

install_requires = [
    #"pycairo",
    #"pygtk",
    "setuptools",
    ]

tests_require = [
    "zope.testing",
    'tl.testing [cairo]',
    ]

extras_require = {
    "test": tests_require,
    }

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: X11 Applications",
    "Environment :: X11 Applications :: GTK",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Zope Public License",
    "Programming Language :: Python",
    "Topic :: Multimedia :: Graphics",
    ]

entry_points = """\
    [console_scripts]
    gtkdemo = tl.geodrawing.demo:gtkdemo
    """

setup(name="tl.geodrawing",
      version='0.1',
      description=__doc__.strip(),
      long_description=longdesc,
      keywords=("gtk widget drawingarea drawing geo coordinates map tile "
                "osm openstreetmap"),
      classifiers=classifiers,
      author="Thomas Lotze",
      author_email="thomas@thomas-lotze.de",
      url="http://packages.python.org/tl.geodrawing/",
      license="ZPL 2.1",
      packages=find_packages(),
      install_requires=install_requires,
      extras_require=extras_require,
      tests_require=tests_require,
      include_package_data=True,
      data_files=data_files,
      test_suite="tl.geodrawing.tests.test_suite",
      entry_points=entry_points,
      namespace_packages=["tl"],
      zip_safe=False,
      )

# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

# These are in a separate module so that symlinks can be made automatically.
scripts = [
    # gis
    'gis-bbox      = scripts.gis.bbox:main',
    'gis-copy-proj = scripts.gis.copy_proj:main',
    'gis-copy-ndv  = scripts.gis.copy_ndv:main',
    'gis-set-srs   = scripts.gis.set_srs:main',
    'gis-polygon   = scripts.gis.polygon:main',
    'gis-sum       = scripts.gis.sum:main',
    # gallery
    'gallery       = scripts.gallery:main',
    'gallery-html  = scripts.gallery.html:main',
    'gallery-meta  = scripts.gallery.meta:main',
    'gallery-index = scripts.gallery.index:main',
    'gallery-media = scripts.gallery.media:main',
    # various
    'dbf2csv       = scripts.dbf2csv:main',
    'garmin-graph  = scripts.garmin:main',
    'gcalendar     = scripts.calendar:main',
    'ln_scripts    = scripts.ln_scripts:main',
    'newpy         = scripts.newpy:main',
    'turn          = scripts.turn:main',
]

# Some extra commands to symlink
commands = [
    'flake8',
    'ipython',
    'python',
]

# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

# These are in a separate module so that symlinks can be made automatically.
scripts = [
    'dbf2csv       = scripts.dbf2csv:main',
    'garmin-graph  = scripts.garmin:main',
    'gcalendar     = scripts.calendar:main',
    'gis-bbox      = scripts.gis.bbox:main',
    'gis-copy-proj = scripts.gis.copy_proj:main',
    'gis-copy-ndv  = scripts.gis.copy_ndv:main',
    'gis-set-srs   = scripts.gis.set_srs:main',
    'gis-polygon   = scripts.gis.polygon:main',
    'gis-sum       = scripts.gis.sum:main',
    'ln_scripts    = scripts.link:main',
    'newpy         = scripts.newpy:main',
]

# Some extra commands to symlink
commands = [
    'flake8',
    'ipython',
]

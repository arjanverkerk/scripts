# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

# These are in a separate module so that symlinks can be made automatically.
scripts = [
    # gis
    'gis-bbox      = scripts.gis.bbox:main',
    'gis-polygon   = scripts.gis.polygon:main',
    'gis-sum       = scripts.gis.sum:main',
    # gallery
    'gallery       = scripts.gallery.gallery:main',
    # various
    'dbf2csv       = scripts.dbf2csv:main',
    'gcalendar     = scripts.calendar:main',
    'ln_scripts    = scripts.ln_scripts:main',
    'newpy         = scripts.newpy:main',
    'tstx         = scripts.tstx:main',
    'tst         = scripts.tst:main',
]

# Some extra commands to symlink
commands = [
    'flake8',
    'ipython',
    'turn',
    'naw',
]

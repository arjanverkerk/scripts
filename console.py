# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

# These are in a separate module so that symlinks can be made automatically.
scripts = [
    # symbolic linker
    'ln_scripts       = scripts.ln_scripts:main',
    # gis
    'gis-bbox         = scripts.gis.bbox:main',
    'gis-dbf2csv      = scripts.gis.dbf2csv:main',
    'gis-polygon      = scripts.gis.polygon:main',
    'gis-sum          = scripts.gis.sum:main',
    'gis-ogr-merge    = scripts.gis.ogr_merge:main',
    'gis-ogr-snap     = scripts.gis.ogr_snap:main',
    'gis-gdal-nan2ndv = scripts.gis.gdal_nan2ndv:nan2ndv',
    'gis-gdal-ndv2ndv = scripts.gis.gdal_ndv2ndv:main',
    'gis-gdal-cut2ndv = scripts.gis.gdal_cut2ndv:main',
    # various
    'annotate         = scripts.annotate:main',
    'enumerate        = scripts.enumerate:main',
    'gallery          = scripts.gallery.gallery:main',
    'gcalendar        = scripts.gcalendar:main',
    'newpy            = scripts.newpy:main',
    'track            = scripts.track:main',
    'tst-exif         = scripts.tst_exif:main',
]

# Some extra commands to symlink
commands = [
    'flake8',
    'ipython',
    'naw',
    'python',
    'turn',
]

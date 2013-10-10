# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

# These are in a separate module so that symlinks can be made automatically.
scripts = [
    'album         = scripts.album.server:main',
    'dbf2csv       = scripts.dbf2csv:main',
    'fz-mail       = scripts.fz.mail:main',
    'fz-pommo-move = scripts.fz.pommo_move:main',
    'gcalendar     = scripts.calendar:main',
    'gis-copy-proj = scripts.gis.copy_proj:main',
    'ln_scripts    = scripts.link:main',
    'newpy         = scripts.newpy:main',
]

# Some extra commands to symlink
commands = [
    'flake8',
    'ipython',
]

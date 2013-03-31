# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

# These are in a separate module so that symlinks can be made automatically.
scripts = [
    'fz-pommo-move = scripts.fz.pommo_move:main',
    'ln_scripts    = scripts.link:main',
    'newpy         = scripts.newpy:main',
]

# Some extra commands to symlink
commands = [
    'flake8',
    'ipython',
]

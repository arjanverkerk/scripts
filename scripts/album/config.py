# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import os
import re

# Content types
MIME = {
    '.jpg': 'image/jpeg',
    '.png': 'image/png',
    '.ogv': 'video/ogg',
    '.ogg': 'video/ogg',
    '.pdf': 'application/pdf',
}

# Paths
ROOT_DIR = '/'
HOME_DIR = os.getenv('HOME')

# Patterns and formats
RANGE_PATTERN = re.compile(
    '^bytes=(?P<start>[0-9]+)-(?P<stop>[0-9]*)'
)
RANGE = 'bytes {start}-{stop}/{size}'

class Config(object):
    DEBUG = True

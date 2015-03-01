# -*- coding: utf-8 -*-
""" 
Folder structure
----------------
base
    templates               # static
    www                     # static
        index.html          # by gallery index
        assets              # static
        year                # by gallery-index or gallery-media
            index.html      # by gallery-index, if at all
            album-title     # by gallery-index or gallery-media
                index.html  # by gallery-html
                media       # by gallery-media
                thumbnails  # by gallery-media
                posters     # by gallery-media

- Maybe merge media and and meta, for smooth handling of changed files.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

# album folders
IMAGES = 'images'
VIDEOS = 'videos'
POSTERS = 'posters'
THUMBNAILS = 'thumbnails'

# metafile with titles, etc
META_NAME = 'meta.json'


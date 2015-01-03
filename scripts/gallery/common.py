# -*- coding: utf-8 -*-
""" Common stuff to gallery framework. """

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import os

TITLES_NAME = 'titles.json'

VIDEO_EXTENSIONS = (
    'ogv',
    'avi',
    'mov',
)
IMAGE_EXTENSIONS = (
    'jpeg',
    'jpg',
    'png',
)


class PathMaker(object):
    """
    Used to find target paths for media placement (absolute) and html
    generation (relative).
    """

    def __init__(self, target_dir, relative=True):
        if relative:
            self.target_dir = os.path.relpath(target_dir)
        else:
            self.target_dir = target_dir

    def image(self, name):
        return os.path.join(self.target_dir, 'images', name)

    def poster(self, name):
        return os.path.join(self.target_dir, 'posters', name)

    def video(self, name):
        return os.path.join(self.target_dir, 'videos', name)

    def thumbnail(self, name):
        return os.path.join(self.target_dir, 'thumbnails', name)

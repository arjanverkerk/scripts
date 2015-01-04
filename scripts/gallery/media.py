# -*- coding: utf-8 -*-
"""
Copy and / or convert media files from source to target folder. Skip
media if target exists, but allways update titles in target folder. So,
always update any missing file, be it a thumbnail or a converted video.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import os
import sys

logger = logging.getLogger(__name__)


class Router(object):
    """
    Used to find target paths for media placement (absolute) and html
    generation (relative).
    """

    def __init__(self, target_dir):
        self.target = target_dir

    def build(self, sub, root, ext):
        return os.path.join(self.target, sub, '{}{}'.format(root, ext))

    def image(self, root, ext):
        return self.build('images', root, ext)

    def config(self, root, ext):
        return self.build('config', root, ext)

    def video(self, root, ext):
        return self.build('videos', root, '.ogv')

    def poster(self, root, ext):
        return self.build('posters', root, '.jpg')

    def thumbnail(self, root, ext):
        return self.build('thumbnails', root, '.jpg')


class Processor(object):
    videos = set([
        '.ogv',
        '.avi',
        '.mov',
        # '.sub',
    ])
    images = set([
        '.jpeg',
        '.jpg',
        '.png',
    ])

    def __init__(self, target_dir):
        self.router = Router(target_dir)

    def process(self, base, root, ext):
        if ext in self.images:
            return self.image(base, root, ext)
        if ext in self.videos:
            return self.video(base, root, ext)
        return self.config(base, root, ext)

    def image(self, base, root, ext):
        """
        Create resized image and thumbnail.
        """
        image_path = self.router.image(root, ext)
        thumbnail_path = self.router.thumbnail(root, ext)
        print(image_path)
        print(thumbnail_path)

    def video(self, base, root, ext):
        """
        Create video formats, poster and thumbnail.
        """
        video_path = self.router.video(root, ext)
        poster_path = self.router.poster(root, ext)
        thumbnail_path = self.router.thumbnail(root, ext)
        print(video_path)
        print(poster_path)
        print(thumbnail_path)

    def config(self, base, root, ext):
        """
        Copy config file.
        """
        config_path = self.router.config(root, ext)
        print(config_path)


def command(source_dir, target_dir):
    """
    """
    processor = Processor(target_dir)
    for name in os.listdir(source_dir):
        base = source_dir
        root, ext = os.path.splitext(name)
        processor.process(base, root, ext)
    return 0


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    # add arguments here
    parser.add_argument(
        'source_dir',
        metavar='SOURCE',
    )
    parser.add_argument(
        'target_dir',
        metavar='TARGET',
    )
    return parser


def main():
    """ Call command with args from parser. """
    kwargs = vars(get_parser().parse_args())

    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG,
                        format='%(message)s')

    try:
        return command(**kwargs)
    except:
        logger.exception('An exception has occurred.')

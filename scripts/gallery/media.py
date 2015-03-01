# -*- coding: utf-8 -*-
"""
Create media files
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import os
import sys

from scripts.gallery import common

from PIL import Image

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

    def config(self, root, ext):
        return self.build('config', root, ext)

    def image(self, root, ext):
        return self.build(common.IMAGES, root, ext)

    def video(self, root, ext):
        return self.build(common.VIDEOS, root, '.ogv')

    def poster(self, root, ext):
        return self.build(common.POSTERS, root, '.jpg')

    def thumbnail(self, root, ext):
        return self.build(common.THUMBNAILS, root, '.jpg')


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

    folders = (common.IMAGES,
               common.VIDEOS,
               common.POSTERS,
               common.THUMBNAILS)

    width = 1024
    height = 768

    def __init__(self, target_dir):
        """ Create folders and a router. """
        # create folders
        for folder in self.folders:
            try:
                os.makedirs(os.path.join(target_dir, folder))
            except OSError:
                pass  # it exists

        self.router = Router(target_dir)

    def process(self, base, root, ext):
        if ext.lower() in self.images:
            return self.image(base, root, ext)
        if ext.lower() in self.videos:
            return self.video(base, root, ext)
        return self.config(base, root, ext)

    def image(self, base, root, ext):
        """
        Create resized image and thumbnail.
        """
        source_path = os.path.join(base, root + ext)
        image_path = self.router.image(root, ext)
        thumbnail_path = self.router.thumbnail(root, ext)

        source = Image.open(source_path)
        width, height = source.size
        resample = Image.ANTIALIAS

        # image
        logger.debug('Create image {}'.format(image_path))
        image_ratio = min(self.width / width, self.height / height)
        image_size = (int(width * image_ratio),
                      int(height * image_ratio))
        image = source.resize(image_size, resample)
        image.save(image_path)

        # thumbnail
        logger.debug('Create thumbnail {}'.format(thumbnail_path))
        thumbnail_ratio = image_ratio / 8
        thumbnail_size = (int(width * thumbnail_ratio),
                          int(height * thumbnail_ratio))
        thumbnail = image.resize(thumbnail_size, resample)
        thumbnail.save(thumbnail_path)

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

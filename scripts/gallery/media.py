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

from scripts.gallery import common

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = ['.{}'.format(e) for e in common.IMAGE_EXTENSIONS]
VIDEO_EXTENSIONS = ['.{}'.format(e) for e in common.VIDEO_EXTENSIONS]


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


# the converters
def process_image(source_path, path_maker):
    """
    Create resized image and thumbnail.
    """
    source_name = os.path.basename(source_path)
    image_path = path_maker.image(source_name)
    thumbnail_path = path_maker.thumbnail(source_name)
    print(image_path)
    print(thumbnail_path)


def process_video(source_path, path_maker):
    """
    Create video formats, poster and thumbnail.
    """
    source_name = os.path.basename(source_path)
    image_path = path_maker.image(source_name)
    poster_path = path_maker.poster(source_name)
    thumbnail_path = path_maker.thumbnail(source_name)
    print(image_path)
    print(poster_path)
    print(thumbnail_path)


def command(source_dir, target_dir):
    """
    """
    path_maker = common.PathMaker(target_dir)
    for source_name in os.listdir(source_dir):
        if source_name == common.TITLES_NAME:
            continue
        source_path = os.path.join(source_dir, source_name)
        source_ext = os.path.splitext(source_name)[-1].lower()

        # the conversions
        if source_ext in IMAGE_EXTENSIONS:
            process_image(source_path=source_path, path_maker=path_maker)
        if source_ext in VIDEO_EXTENSIONS:
            process_video(source_path=source_path, path_maker=path_maker)

    return 0


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

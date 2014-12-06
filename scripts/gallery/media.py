# -*- coding: utf-8 -*-
"""
Copy and / or convert media files from source to target folder. Skip
media if target exists, but allways update titles in target folder. So,
always update any missing file, be at a thumbnail or a converted video.
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
def image(source_path, target_dir):
    """
    Create resized image and thumbnail.
    """


def video(source_path, target_dir):
    """
    Create video formats, poster and thumbnail.
    """


def command(source_dir, target_dir):
    names = [n for n in os.listdir(source_dir) if n != common.TITLES_NAME]
    print(names)
    return 0


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG,
                        format='%(message)s')
    return command(**vars(get_parser().parse_args()))

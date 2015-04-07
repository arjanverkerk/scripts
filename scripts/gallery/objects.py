# -*- coding: utf-8 -*-
"""
Create or update titles.json file for the files in the directory. Titles
already present will be preserved. Titles for nonexisting files will
be removed. Detects renamed files by md5 sum.

TODO:
- store the frame to dump as poster / thumbnail in videos

NEW PLAN:
- Each video or image is an object, optionally persisted in json file.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import sys

logger = logging.getLogger(__name__)


def command(path):
    """ Update the titles file in folder path. """
    return 0


class MediaObject(object):
    """ Common things like file locations. """
    pass


class Image(object):
    def __init__(self, source_path, target_dir):
        source_path = source_path
        target_dir = target_dir  # Or maybe already split and forget


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    # add arguments here
    parser.add_argument(
        'path',
        metavar='PATH',
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

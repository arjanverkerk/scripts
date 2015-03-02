# -*- coding: utf-8 -*-
"""
Run this module to sync
- The metadata file
- The images and videos
- The html
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import sys

logger = logging.getLogger(__name__)


def command():
    return 0


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    # add arguments here
    # parser.add_argument(
    #     'path',
    #     metavar='FILE',
    # )
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

# -*- coding: utf-8 -*-
"""
Regenerates index.html files in the target folderassuming assets in the
current directory. Regenerates the index page as well.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import sys

logger = logging.getLogger(__name__)


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    # add arguments here
    #parser.add_argument(
        #'path',
        #metavar='FILE',
    #)
    return parser


def command():
    return 0


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG,
                        format='%(message)s')
    return command(**vars(get_parser().parse_args()))

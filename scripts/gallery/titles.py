# -*- coding: utf-8 -*-
"""
Create or update titles.json file for the files in the directory.
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import json
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
        'path',
        metavar='PATH',
    )
    return parser


def command(path):
    """ Update the titles file in folder path. """
    titles_path = os.path.join(path, common.TITLES_NAME)
    tmp_path = '{}.in'.format(titles_path)

    # read
    try:
        original = json.load(open(titles_path))
    except IOError:
        original = {}

    # update
    titles = {n: original.get(n, "")
              for n in os.listdir(path) if n != common.TITLES_NAME}

    # write
    with open(tmp_path, 'w') as tmp_file:
        json.dump(titles, tmp_file, indent=2)
    os.rename(tmp_path, titles_path)

    return 0


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG,
                        format='%(message)s')
    return command(**vars(get_parser().parse_args()))

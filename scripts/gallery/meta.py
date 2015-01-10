# -*- coding: utf-8 -*-
"""
Create or update titles.json file for the files in the directory. Titles
already present will be preserved. Titles for nonexisting files will
be removed.

TODO
- compute and store sum to detect file changes
- store the frame to dump as poster / thumbnail in videos
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


class Meta(object):
    """
    """
    def __init__(path):
        """ Initialize the data. """
        self.path = path

    def load(self):
        path = os.path.join(self.path, common.META_NAME)
        try:
            data = json.load(open(self.meta_path))
        except IOError:
            data = {}
        self.description = data.get('description', '')
        self.titles = data.get('titles', {})
        self.sums = data.get('sums', {})

    def update(self, path):
        """ 
        list, see what titles are unknown
        calc sums for new files
        see if match by sum possible
        """
        pass
    
    def save(self):
        """ Write. """
        data = collections.OrderDict()
        data['description'] = self.description
        data['titles'] = self.titles
        data['sums'] = self.sums
        path = os.path.join(self.path, common.META_NAME)
        tmp_path = '{}.in'.format(path)
        with open(tmp_path, 'w') as tmp_file:
            json.dump(data, tmp_file, indent=2)
        os.rename(tmp_path, titles_path)


def command(path):
    """ Update the titles file in folder path. """
    meta = Meta(path)
    # update
    titles = {n: original.get(n, "")
              for n in os.listdir(path) if n != common.TITLES_NAME}

    # write

    return 0


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG,
                        format='%(message)s')
    return command(**vars(get_parser().parse_args()))

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
import hashlib
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
        """ Loads description, titles and sums. """
        path = os.path.join(self.path, common.META_NAME)
        try:
            data = json.load(open(path))
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
        names = os.listdir(path)
        names.remove(common.META_NAME)

        for n in names:
            if n not in self.sums:
                s = haslib.md5(
                    open(os.path.join(self.path, n)).read(),
                ).hexdigest()
                try:
                    # using existing sum, move title 
                    t = self.sums[s]
                    self.titles[n] = self.titles[t]
                    del self.titles[t]
                except KeyError:
                    # apparently a new file
                    self.titles[n] = ''
                finally:
                    self.sums[s] = n
        
        # Now deal with removed files?
        # titles = {n: self.original.get(n, "")
                  # for n in os.listdir(path) if n != common.TITLES_NAME}

    def save(self):
        """ Write. """
        data = collections.OrderedDict()
        data['description'] = self.description
        data['titles'] = collections.ordereddict(sorted(self.titles.items))
        data['sums'] = self.sums
        
        path = os.path.join(self.path, common.META_NAME)
        tmp_path = '{}.in'.format(path)
        with open(tmp_path, 'w') as tmp_file:
            json.dump(data, tmp_file, indent=2)
        os.rename(tmp_path, titles_path)


def command(path):
    """ Update the titles file in folder path. """
    meta = Meta(path)
    meta.update()
    meta.save()
    return 0


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG,
                        format='%(message)s')
    return command(**vars(get_parser().parse_args()))

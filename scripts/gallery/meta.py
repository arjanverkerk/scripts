# -*- coding: utf-8 -*-
"""
Create or update titles.json file for the files in the directory. Titles
already present will be preserved. Titles for nonexisting files will
be removed. Detects renamed files by md5 sum.

TODO:
- store the frame to dump as poster / thumbnail in videos
"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import collections
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
    def __init__(self, path):
        """ Initialize the data. """
        self.path = path

    def load(self):
        """ Loads description, titles and checksums. """
        path = os.path.join(self.path, common.META_NAME)
        try:
            data = json.load(open(path))
        except IOError:
            data = {}
        self.description = data.get('description', '')
        self.titles = data.get('titles', {})
        self.checksums = data.get('checksums', {})

    def update(self, path):
        """
        list, see what titles are unknown
        calc checksums for new files
        see if match by sum possible
        """
        checksums = {self.checksums[name]: name for name in self.checksums}

        names = set(os.listdir(path))
        try:
            names.remove(common.META_NAME)
        except KeyError:
            pass

        # handle new files
        create = names.difference(self.titles)
        for new in create:
            checksum = hashlib.md5(
                open(os.path.join(self.path, new)).read(),
            ).hexdigest()
            try:
                # change name for existing title
                update = checksums[checksum]
                self.titles[create] = self.titles[update]
                del self.titles[update]
            except KeyError:
                # add new name with dummy title
                self.titles[create] = ''
            finally:
                self.checksums[create] = checksum

        # now use the possibly changed titles to detect deleted files
        delete = set(self.titles).difference(names)
        for name in delete:
            del self.titles[name]
            del self.checksums[name]

    def save(self):
        """ Write. """
        data = collections.OrderedDict()
        data['description'] = self.description

        # sorted dicts for titles and checksums
        sorted_dict = lambda d: collections.ordereddict(sorted(d.items))

        data['titles'] = sorted_dict(self.titles)
        data['checksums'] = sorted_dict(self.checksums)

        # write indirect
        path = os.path.join(self.path, common.META_NAME)
        tmp_path = '{}.in'.format(path)
        with open(tmp_path, 'w') as tmp_file:
            json.dump(data, tmp_file, indent=2)
        os.rename(tmp_path, path)


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

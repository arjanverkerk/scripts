# -*- coding: utf-8 -*-
"""
Run this module to sync
- The metadata file
- The images and videos
- The html
Folder structure
----------------
base
    templates               # static
    www                     # static
        index.html          # by gallery index
        assets              # static
        year                # by gallery-index or gallery-media
            index.html      # by gallery-index, if at all
            album-title     # by gallery-index or gallery-media
                index.html  # by gallery-html
                media       # by gallery-media
                thumbnails  # by gallery-media
                posters     # by gallery-media

- Maybe merge media and and meta, for smooth handling of changed files.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import collections
import hashlib
import json
import logging
import os
import sys

logger = logging.getLogger(__name__)

# album folders
IMAGES = 'images'
VIDEOS = 'videos'
POSTERS = 'posters'
THUMBNAILS = 'thumbnails'

# metafile with titles, etc
CONFIG = 'gallery.json'



class Meta(object):
    """
    """
    def __init__(self, path):
        """ Initialize the data. """
        self.path = path

    def load(self):
        """ Loads description, titles and checksums. """
        path = os.path.join(self.path, CONFIG)
        try:
            data = json.load(open(path))
        except IOError:
            data = {}
        self.description = data.get('description', '')
        self.titles = data.get('titles', {})
        self.checksums = data.get('checksums', {})

    def update(self):
        """
        list, see what titles are unknown
        calc checksums for new files
        see if match by sum possible
        """
        checksums = {self.checksums[name]: name for name in self.checksums}

        names = set(os.listdir(self.path))
        try:
            names.remove(CONFIG)
        except KeyError:
            pass

        # handle new files
        create = names.difference(self.titles)
        for new in create:

            logger.debug('Calculate checksum for {}'.format(new))
            checksum = hashlib.md5(
                open(os.path.join(self.path, new)).read(),
            ).hexdigest()
            try:
                # change name for existing title
                old = checksums[checksum]
                self.titles[new] = self.titles[old]
                del self.titles[old]
            except KeyError:
                # add new name with dummy title
                self.titles[new] = new
            finally:
                self.checksums[new] = checksum

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
        sorted_dict = lambda d: collections.OrderedDict(sorted(d.items()))

        data['titles'] = sorted_dict(self.titles)
        data['checksums'] = sorted_dict(self.checksums)

        # write indirect
        path = os.path.join(self.path, CONFIG)
        tmp_path = '{}.in'.format(path)
        with open(tmp_path, 'w') as tmp_file:
            json.dump(data, tmp_file, indent=2)
        os.rename(tmp_path, path)



def gallery(source_dir, target_dir):
    """ Update the titles file in folder path. """
    print(os.path.abspath(source_dir))
    print(os.getcwd())
    print(os.path.abspath(target_dir))
    meta = Meta(source_dir)
    meta.load()
    meta.update()
    meta.save()
    return 0


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=__doc__
    )
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
        gallery(**kwargs)
        return 0
    except:
        logger.exception('An exception has occurred.')
        return 1

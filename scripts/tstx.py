#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Add a timestamp based on exif data. """

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from datetime import datetime as Datetime
import argparse
import logging
import os
import sys

from PIL import Image

logger = logging.getLogger(__name__)


def tstx(paths, verbose, dry_run):

    # logging
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(stream=sys.stderr, level=level, format='%(message)s')

    for path in paths:
        # path
        logger.debug('Processing: "{}"'.format(path))

        # exif
        try:
            image = Image.open(path)
        except IOError as error:
            logger.debug('    Error: "{}"'.format(error))
            continue
        try:
            exif = image._getexif()[36867]
        except AttributeError:
            logger.debug('    No EXIF attributes found.')
            continue
        exif_datetime = Datetime.strptime(exif, '%Y:%m:%d %H:%M:%S')
        logger.debug('    EXIF date: {}'.format(exif_datetime))


        # prepare
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        timestamp = exif_datetime.isoformat()
        
        newbasename = '{}_{}'.format(timestamp, basename)
        newpath = os.path.join(dirname, newbasename)
        logger.debug('    Old name: %s', basename)
        logger.debug('    New name: %s', newbasename)

        if dry_run:
            continue

        if basename.startswith(timestamp):
            logger.debug('    Timestamp %s already present.', timestamp)
            continue

        # rename
        os.rename(path, newpath)
        logger.debug('    Filename renamed.')


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='*', metavar='FILE')
    parser.add_argument('-d', '--dry-run', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser


def main():
    """ Call tstx with args from parser. """
    kwargs = vars(get_parser().parse_args())

    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG,
                        format='%(message)s')

    try:
        tstx(**kwargs)
        return 0
    except:
        logger.exception('An exception has occurred.')
        return 1

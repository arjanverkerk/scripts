#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import csv
import os

import ogr


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=""
    )
    parser.add_argument(
        'dbfpath',
        metavar='FILE',
    )
    return parser


def command(dbfpath):
    """
    Use ogr to convert a shapefile's dbf to csv.

    It may even work on other dbf's.
    """
    root, ext = os.path.splitext(dbfpath)
    csvpath = root + '.csv'

    shape = ogr.Open(dbfpath)
    layer = shape[0]
    feature = layer[0]
    with open(csvpath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, feature.items())
        writer.writeheader()
        for feature in layer:
            writer.writerow(feature.items())


def main():
    """ Call command with args from parser. """
    command(**vars(get_parser().parse_args()))

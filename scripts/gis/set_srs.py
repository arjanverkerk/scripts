# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import sys

from osgeo import gdal
from osgeo import osr

logger = logging.getLogger(__name__)


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=""
    )
    parser.add_argument(
        'projection',
        metavar='SRS',
    )
    parser.add_argument(
        'targetpaths',
        nargs='*',
        metavar='TARGET',
    )
    return parser


def command(projection, targetpaths):
    """ Do something spectacular. """
    wkt = osr.GetUserInputAsWKT(projection)
    for targetpath in targetpaths:
        target = gdal.Open(targetpath, gdal.GA_Update)
        target.SetProjection(wkt)


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    command(**vars(get_parser().parse_args()))

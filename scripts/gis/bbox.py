# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import sys

from osgeo import gdal

logger = logging.getLogger(__name__)


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=""
    )
    parser.add_argument(
        'sourcepath',
        metavar='SOURCE',
    )
    return parser


def command(sourcepath):
    """ Do something spectacular. """
    dataset = gdal.Open(sourcepath)
    width, height = dataset.RasterXSize, dataset.RasterYSize
    geotransform = dataset.GetGeoTransform()
    bbox = ','.join(map(str, [
        geotransform[0],
        geotransform[3] + height * geotransform[5],
        geotransform[0] + width * geotransform[1],
        geotransform[3],
    ]))
    print(bbox)


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    command(**vars(get_parser().parse_args()))

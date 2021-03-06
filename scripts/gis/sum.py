# -*- coding: utf-8 -*-

import argparse
import logging
import sys

from osgeo import gdal
import numpy as np

logger = logging.getLogger(__name__)


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=""
    )
    parser.add_argument(
        'sourcepaths',
        metavar='SOURCE',
        nargs='*',
    )
    return parser


def command(sourcepaths):
    """ Do something spectacular. """
    total = 0
    for sourcepath in sourcepaths:
        source = gdal.Open(sourcepath)
        band = source.GetRasterBand(1)
        array = np.ma.masked_equal(band.ReadAsArray(),
                                   band.GetNoDataValue())
        array_sum = array.sum()
        if np.ma.is_masked(array_sum):
            array_sum = 0
        print('{:>10.2f}'.format(array_sum), sourcepath)
        total += (array_sum)
    print('{:>10.2f} total.'.format(total))


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    command(**vars(get_parser().parse_args()))

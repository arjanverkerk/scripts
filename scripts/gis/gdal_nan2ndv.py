#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Copy file with nan values replaced with no data values. """

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import sys

from osgeo import gdal
import numpy as np

logger = logging.getLogger(__name__)


def replacenan(source_path, target_path):
    source = gdal.Open(source_path)
    array = source.GetRasterBand(1).ReadAsArray()
    array[np.isnan(array)] = source.GetRasterBand(1).GetNoDataValue()

    memory = gdal.GetDriverByName(b'mem').CreateCopy('', source)
    memory.GetRasterBand(1).WriteArray(array)

    options = ['compress=deflate', 'tiled=yes']
    gdal.GetDriverByName(b'gtiff').CreateCopy(
        target_path, memory, options=options,
    )


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('source_path', metavar='SOURCE_PATH')
    parser.add_argument('target_path', metavar='TARGET_PATH')
    return parser


def nan2ndv():
    """ Call replacenan with args from parser. """
    # logging
    kwargs = vars(get_parser().parse_args())
    if kwargs.pop('verbose'):
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(stream=sys.stderr, level=level, format='%(message)s')

    # run or fail
    replacenan(**kwargs)

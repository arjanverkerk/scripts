# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import sys

from osgeo import gdal
from osgeo import ogr

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
    x1 = geotransform[0]
    y1 = geotransform[3] + height * geotransform[5]
    x2 = geotransform[0] + width * geotransform[1]
    y2 = geotransform[3]

    # make a polygon
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for x, y in ((x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)):
        ring.AddPoint_2D(x, y)
    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ring)

    # print
    print(polygon.ExportToWkt())


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    command(**vars(get_parser().parse_args()))

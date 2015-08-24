#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" TODO Docstring. """

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import sys

from osgeo import ogr

logger = logging.getLogger(__name__)


def single(geometry):
    """ Return geometry with points rounded. """

    ring = ogr.Geometry(ogr.wkbLinearRing)
    for x, y in geometry.GetGeometryRef(0).GetPoints():
        ring.AddPoint_2D(round(x), round(y))

    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(ring)

    return polygon


def snap(source_path, target_path):
    # open source
    data_source1 = ogr.Open(source_path)
    layer1 = data_source1[0]

    # create target based on source
    driver = ogr.GetDriverByName(b'ESRI Shapefile')
    driver.DeleteDataSource(target_path)
    data_source2 = driver.CreateDataSource(target_path)
    layer2 = data_source2.CreateLayer(
        target_path,
        srs=layer1.GetSpatialRef(),
        geom_type=layer1.GetGeomType(),
    )
    layer_defn = layer1.GetLayerDefn()

    # copy field configuration
    for i in range(layer_defn.GetFieldCount()):
        field_defn = layer_defn.GetFieldDefn(i)
        layer2.CreateField(field_defn)

    # write (modified) data
    total = layer1.GetFeatureCount()
    for count, feature1 in enumerate(layer1, 1):
        feature1.SetGeometry(single(feature1.geometry()))
        layer2.CreateFeature(feature1)
        ogr.TermProgress_nocb(count / total)


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('source_path', metavar='SOURCE')
    parser.add_argument('target_path', metavar='TARGET')
    return parser


def main():
    """ Call snap with args from parser. """
    # logging
    kwargs = vars(get_parser().parse_args())
    if kwargs.pop('verbose'):
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(stream=sys.stderr, level=level, format='%(message)s')

    # run or fail
    try:
        snap(**kwargs)
        return 0
    except:
        logger.exception('An exception has occurred.')
        return 1

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


def merge(source_path, target_path):
    # read & merge
    data_source = ogr.Open(source_path)
    layer = data_source[0]
    sr = layer.GetSpatialRef()
    geometry = ogr.Geometry(ogr.wkbMultiPolygon)
    total = layer.GetFeatureCount()
    for count, feature in enumerate(layer, 1):
        geometry.AddGeometry(feature.geometry())
        ogr.TermProgress_nocb(count / total)
    union = geometry.UnionCascaded()

    # write
    driver = ogr.GetDriverByName(b'ESRI Shapefile')
    driver.DeleteDataSource(target_path)
    data_source = driver.CreateDataSource(target_path)
    layer = data_source.CreateLayer(target_path, sr)
    layer_defn = layer.GetLayerDefn()
    feature = ogr.Feature(layer_defn)
    feature.SetGeometry(union)
    layer.CreateFeature(feature)
    data_source.Destroy()


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('source_path', metavar='SOURCE')
    parser.add_argument('target_path', metavar='TARGET')
    return parser


def main():
    """ Call merge with args from parser. """
    # logging
    kwargs = vars(get_parser().parse_args())
    if kwargs.pop('verbose'):
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(stream=sys.stderr, level=level, format='%(message)s')

    # run or fail
    try:
        merge(**kwargs)
        return 0
    except:
        logger.exception('An exception has occurred.')
        return 1

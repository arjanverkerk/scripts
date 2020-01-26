#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import ogr
import os
import itertools


class ShapeFile(object):
    """ Convenicence wrapper for ogr shapefile operations. """
    TYPE = {
        'int': ogr.OFTInteger,
    }

    def __len__(self):
        """ Return featurecount according to current filter setting. """
        return self.layer.GetFeatureCount()

    def __init__(self, path, mode='r', geomtype=0, template=None):
        """ Store some attributes. """
        if mode == 'r':
            self.shape = ogr.Open(path)
            self.layer = self.shape[0]
            self.srs = self.layer.GetSpatialRef()
        elif mode == 'w':
            driver = ogr.GetDriverByName(b'ESRI Shapefile')
            if os.path.exists(path):
                logger.info('Replacing {}'.format(path))
                driver.DeleteDataSource(str(path))
            self.shape = driver.CreateDataSource(str(path))
            sr = osr.SpatialReference()
            sr.ImportFromEPSG(28992)
            self.layer = self.shape.CreateLayer(
                str(os.path.basename(path)),
                sr,
                geomtype
            )
        else:
            raise ValueError("Unsupported mode: '{}'".format(self.mode))

        if template is not None:
            layerdefinition = template.layer.GetLayerDefn()
            for i in range(layerdefinition.GetFieldCount()):
                fielddefinition = layerdefinition.GetFieldDefn(i)
                self.layer.CreateField(fielddefinition)

        self._definition = self.layer.GetLayerDefn()
        self.mode = mode
        self.path = os.path.abspath(path)

    def iterfeatures(self, progress=False, skip=False):
        """ Return feature generator. """
        if skip:
            logger.warn('Skipping the hard work!')
            return
        if progress:
            total = self.layer.GetFeatureCount()
            if total:
                indicator = progressindicator.Indicator(total)
        for feature in self.layer:
            yield feature
            if progress:
                indicator.update()

    def itergeometries(self, progress=False, skip=False):
        """ Return geometry generator. """
        for feature in self.iterfeatures(progress=progress, skip=skip):
            yield feature.geometry()

    def iterattributes(self, progress=False, skip=False):
        """ Return attribute generator. """
        for feature in self.iterfeatures(progress=progress, skip=skip):
            yield feature.items()

    def createfield(self, name, type):
        """ Create a field. """
        self.layer.CreateField(ogr.FieldDefn(str(name), self.TYPE[type]))
        self._definition = self.layer.GetLayerDefn()

    def addfeature(self, geom, attrs):
        """ Create a new feature. """
        feature = ogr.Feature(self._definition)
        feature.SetGeometry(geom)
        for k, v in attrs.iteritems():
            feature[str(k)] = v
        self.layer.CreateFeature(feature)

    def close(self):
        """ Close dataset. """
        self.layer = None
        self.shape = None

    @property
    def geomtype(self):
        return self.layer.GetGeomType()

    @property
    def extent(self):
        return self.layer.GetExtent()

    @property
    def fieldnames(self):
        return [self._definition.GetFieldDefn(i).GetName()
                for i in range(self._definition.GetFieldCount())]


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=""
    )
    parser.add_argument('sourcepath', metavar='SOURCE')
    parser.add_argument('targetpath', metavar='TARGET')
    return parser


def write_points(points, target, count):
    target.write('L{}\n'.format(count.next()))
    target.write('{} 2\n'.format(len(points)))
    for p in points:
        target.write('{} {}\n'.format(*p))
    

def command(sourcepath, targetpath):
    """ Do something spectacular. """
    shape = ShapeFile(sourcepath)
    with open(targetpath, 'w') as target:
        id = None
        count = itertools.count(1)
        points = []
        for a in shape.iterattributes():
            if a['IDENTIFICA'] != id:
                if id is not None:
                    write_points(points, target, count)
                    points = []
                id = a['IDENTIFICA']
            points.append((a['ET_X'], a['ET_Y']))
        write_points(points, target, count)
        


def main():
    """ Call command with args from parser. """
    command(**vars(get_parser().parse_args()))


if __name__ == '__main__':
    exit(main())

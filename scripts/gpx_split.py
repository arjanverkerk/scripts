# -*- coding: utf-8 -*-
""" Split gpx file into time-stamped files per track. """

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import sys

from xml.etree import ElementTree

uri = 'http://www.topografix.com/GPX/1/0'
ns = {'gpx': uri}                        # for find
ElementTree.register_namespace('', uri)  # for serialize


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    return parser


def split():
    """ Call gps_split with args from parser. """
    xml = sys.stdin.read()
    tree = ElementTree.fromstring(xml)

    trks = tree.findall('gpx:trk', ns)
    for trk in trks:
        tree.remove(trk)
    for trk in trks:
        tree.append(trk)
        time = trk.find('gpx:trkseg/gpx:trkpt/gpx:time', ns).text
        with open(time + '.gpx', 'w') as f:
            f.write(ElementTree.tostring(tree))
        tree.remove(trk)


def main():
    """ Call split with args from parser. """
    kwargs = vars(get_parser().parse_args())
    split(**kwargs)

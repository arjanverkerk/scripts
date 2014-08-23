# -*- coding: utf-8 -*-
""" Plot garmin xml file using Matplotlib. """

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import sys

from ciso8601 import parse_datetime

from pylab import gca
from pylab import plot
from pylab import show


logger = logging.getLogger(__name__)


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        'paths',
        nargs='+',
        metavar='FILE',
    )
    return parser


def splitter(part):
    key, value = part.split('=')
    return key, value.strip('"')


def make_dicts(path):
    head = '<point '
    tail = '/>\n'
    lines = open(path).readlines()
    for line in lines:
        if not line.startswith(head):
            continue
        parts = line.lstrip(head).rstrip(tail).split()
        yield dict(map(splitter, parts))


def plot_garmin_path(path):
    data = make_dicts(path)
    dist = []
    time = []
    for d in data:
        try:
            dist.append(float(d['distance']))
        except KeyError:
            continue
        time.append(parse_datetime(d['time']))
    pace = [(time[i] - time[i - 1]).total_seconds() /
            (dist[i] - dist[i - 1]) * 1000 / 60
            for i in range(1, len(dist))]
    plot(dist[1:], pace)
    axes = gca()
    axes.set_ylim((3, 7))
    show()


def command(paths):
    for path in paths:
        plot_garmin_path(path)
    return 0


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    return command(**vars(get_parser().parse_args()))

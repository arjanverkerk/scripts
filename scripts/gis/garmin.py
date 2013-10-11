#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import dateutil.parser
import json
import logging
import re
import sys

from pylab import plot
from pylab import show

logger = logging.getLogger(__name__)

POINT = re.compile('<point type="304" '
                   'time="(?P<time>.*)" '
                   'lat="(?P<lat>.*)" '
                   'lon="(?P<lon>.*)" '
                   'alt="(?P<alt>.*)" '
                   'distance="(?P<distance>.*)"/>')


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
    with open(sourcepath) as source:
        datetimes = []
        distances = []
        for line in source:
            match = POINT.match(line)
            if match:
                record = match.groupdict()
                datetimes.append(dateutil.parser.parse(record['time']))
                distances.append(float(record['distance']))
        dist = [d / 1000 for d in distances[1:]]
        pace = [(datetimes[i] - datetimes[i - 1]).total_seconds() /
                (distances[i] - distances[i - 1]) / 60 * 1000
                for i in range(1, len(distances))]
    return json.dumps(zip(dist, pace))


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    command(**vars(get_parser().parse_args()))

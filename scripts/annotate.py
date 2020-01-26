# -*- coding: utf-8 -*-
""" Prefix lines with ISO datetime timestamps. """

import argparse
from datetime import datetime as Datetime
import sys


def stamp():
    template = '{} {}'
    for line in sys.stdin:
        sys.stdout.write(template.format(Datetime.now().isoformat(), line))


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    return parser


def main():
    """ Call stamp with args from parser. """
    kwargs = vars(get_parser().parse_args())
    stamp(**kwargs)

# -*- coding: utf-8 -*-
""" Prefix lines with line numbers. """

import argparse
import sys


def enum(width, start):
    template = '{{: >{}d}} {{}}'.format(width) if width else '{:d} {}'
    for number, line in enumerate(sys.stdin, start=start):
        sys.stdout.write(template.format(number, line))


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-w', '--width', type=int)
    parser.add_argument('-s', '--start', default=0, type=int)
    return parser


def main():
    """ Call enum with args from parser. """
    kwargs = vars(get_parser().parse_args())
    enum(**kwargs)

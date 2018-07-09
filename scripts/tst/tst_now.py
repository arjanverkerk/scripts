# -*- coding: utf-8 -*-
""" Add a short timestamp based on system datetime. """

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from os.path import join, normpath, split
import argparse
import datetime
import os


def tst_now(paths):
    for path in paths:
        dirname, basename = split(normpath(path))
        prefix = datetime.datetime.now().strftime('%Y-%m-%d_')
        newpath = join(dirname, prefix + basename)
        os.rename(path, newpath)


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', metavar='FILE', nargs='*')
    return parser


def main():
    """ Call tst with args from parser. """
    tst_now(**vars(get_parser().parse_args()))

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import csv


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=""
    )
    parser.add_argument('sourcepath', metavar='SOURCE')
    parser.add_argument('targetpath', metavar='TARGET')
    return parser


def command(sourcepath, targetpath):
    """ Do something spectacular. """
    with open(sourcepath) as sourcefile:
        sourcereader = csv.DictReader(sourcefile)
        for sourcerecord in sourcereader:
            print(sourcerecord)



def main():
    """ Call command with args from parser. """
    command(**vars(get_parser().parse_args()))


if __name__ == '__main__':
    exit(main())

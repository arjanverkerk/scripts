# -*- coding: utf-8 -*-
""" Add a timestamp based on system datetime. """

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import sys

logger = logging.getLogger(__name__)


def tst(paths):
    for path in paths:
        basename = os.path.basename(source_file)
        dirname = os.path.dirname(source_file)
        prefix = datetime.datetime.now().strftime('%Y-%m-%d_')
        newpath = os.path.join(dirname, prefix + basename)
        os.rename(path, newpath)


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', metavar='FILE', nargs='*')
    return parser


def main():
    """ Call tst with args from parser. """
    kwargs = vars(get_parser().parse_args())

    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG,
                        format='%(message)s')

    try:
        tst(**kwargs)
        return 0
    except:
        logger.exception('An exception has occurred.')
        return 1

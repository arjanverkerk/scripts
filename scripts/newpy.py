#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import os
import argparse


INTERPRETER = '''#!/usr/bin/env python
'''

TEMPLATE = '''# -*- coding: utf-8 -*-
""" TODO Docstring. """

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import logging
import sys

logger = logging.getLogger(__name__)


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    # add arguments here
    # parser.add_argument(
    #     'path',
    #     metavar='FILE',
    # )
    return parser


def command():
    return 0


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG,
                        format='%(message)s')
    try:
        return command(**vars(get_parser().parse_args()))
    except SystemExit:
        raise  # argparse does this
    except:
        logger.exception('An exception has occurred.')
'''

RUNNER = '''

if __name__ == '__main__':
    exit(main())
'''


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description="Create an (executable) python module."
    )
    parser.add_argument(
        'target',
        metavar='target',
        help='Filepath for the module to create.',
    )
    parser.add_argument(
        '-e', '--executable',
        action='store_true',
        help="Make the module executable.""",
    )
    return parser


def create_module(target, executable):
    """ Create a module and set permissions if necessary. """

    if executable:
        content = INTERPRETER + TEMPLATE + RUNNER
    else:
        content = TEMPLATE

    with open(target, 'w') as newfile:
        newfile.write(content)

    if executable:
        os.chmod(target, 0755)


def main():
    """ Call command with args from parser. """
    create_module(**vars(get_parser().parse_args()))

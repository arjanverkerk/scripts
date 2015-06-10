#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import os
import sys


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


def {name}():
    pass


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    # add arguments here
    # parser.add_argument('path', metavar='FILE')
    return parser


def main():
    """ Call {name} with args from parser. """
    kwargs = vars(get_parser().parse_args())

    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG,
                        format='%(message)s')

    try:
        {name}(**kwargs)
        return 0
    except:
        logger.exception('An exception has occurred.')
        return 1
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
    parser.add_argument(
        '-p', '--print',
        action='store_true',
        dest='console',
        help="Write to stdout instead of file.""",
    )
    return parser


def newpy(target, executable, console):
    """ Create a module and set permissions if necessary. """
    name = os.path.splitext(os.path.basename(target))[0]

    if executable:
        content = INTERPRETER + TEMPLATE.format(name=name) + RUNNER
    else:
        content = TEMPLATE.format(name=name)

    if console:
        sys.stdout.write(content)
        return

    with open(target, 'w') as newfile:
        newfile.write(content)

    if executable:
        os.chmod(target, 0755)


def main():
    """ Call command with args from parser. """
    newpy(**vars(get_parser().parse_args()))

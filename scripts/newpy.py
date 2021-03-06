#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import sys


INTERPRETER = '''#!/usr/bin/env python
'''

TEMPLATE = '''# -*- coding: utf-8 -*-
""" TODO Docstring. """

import argparse


def {name}():
    pass


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    # parser.add_argument('path', metavar='FILE')
    return parser


def main():
    """ Call {name} with args from parser. """
    {name}(**vars(get_parser().parse_args()))
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
        os.chmod(target, 0o0755)


def main():
    """ Call command with args from parser. """
    newpy(**vars(get_parser().parse_args()))

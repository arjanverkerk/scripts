# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import os

import console


BIN_DIR = os.path.join(
    os.path.dirname(console.__file__),
    '.venv/bin',
)


def get_parser():
    parser = argparse.ArgumentParser(
        description='Action',
    )
    return parser


def get_names():
    """ Return name generators for console scripts. """
    for script in console.scripts:
        name = script.split()[0]
        yield name
    for name in console.commands:
        yield name


def action():
    """ Create symlinks for all console_scripts of scripts."""
    for name in get_names():
        source = os.path.join(BIN_DIR, name)
        target = os.path.join('/usr/local/bin', name)
        try:
            os.symlink(source, target)
            print('Created: {}'.format(name))
        except OSError as error:
            print('{}: {}'.format(error.strerror, name))


def main():
    action(**vars(get_parser().parse_args()))

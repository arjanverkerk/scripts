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
    'bin',
)


def get_parser():
    parser = argparse.ArgumentParser(
        description='Action',
    )
    return parser


def action():
    """ Create symlinks for all console_scripts of scripts."""
    for script in console.scripts:
        name = script.split()[0]
        source = os.path.join(BIN_DIR, name)
        target = os.path.join('/usr/local/bin', name)
        os.symlink(source, target)


def main():
    action(**vars(get_parser().parse_args()))

# -*- coding: utf-8 -*-

import argparse
import os

import console
import pathlib

SOURCE_DIR = pathlib.Path(console.__file__).parent / 'bin'
TARGET_DIR = pathlib.Path.home() / '.local/bin'


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
    os.makedirs(TARGET_DIR, exist_ok=True)

    for name in get_names():
        source = SOURCE_DIR / name
        target = TARGET_DIR / name
        try:
            os.symlink(source, target)
            print(f'Created: {name}')
        except OSError as error:
            print(f'{error.strerror}: {name}')


def main():
    action(**vars(get_parser().parse_args()))

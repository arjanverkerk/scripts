# -*- coding: utf-8 -*-

import argparse
import os

import console
import pathlib

SCRIPT_DIR = pathlib.Path(console.__file__).parent / '.venv/bin'
BIN_DIR = pathlib.Path.home() / '.local/bin'


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
    os.makedirs(BIN_DIR, exist_ok=True)

    for name in get_names():
        script = SCRIPT_DIR / name
        link = BIN_DIR / name

        try:
            if link.is_symlink():
                link.unlink()
                print(f'Update: {name}')
            else:
                print(f'Create: {name}')
            link.symlink_to(script)
        except OSError as error:
            print(f'{error.strerror}: {name}')


def main():
    action(**vars(get_parser().parse_args()))

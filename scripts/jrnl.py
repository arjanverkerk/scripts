# -*- coding: utf-8 -*-
""" TODO Docstring. """

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import os

from datetime import datetime as Datetime
from os.path import exists, join

HOME = os.environ['HOME']
DIRNAME = '.jrnl'
LOGNAME = 'log'
KEYNAME = 'key'

LOGPATH = join(HOME, DIRNAME, LOGNAME)
KEYPATH = join(HOME, DIRNAME, KEYNAME)


def mkdir():
    path = join(HOME, DIRNAME)
    if not exists(path):
        os.mkdir(path)


class Keys():
    @classmethod
    def initialize(cls, key):
        if exists(KEYPATH):
            return
        with open(KEYPATH, 'w') as keyfile:
            keyfile.write(key)

    def __init__(self):
        with open(KEYPATH, 'r') as keyfile:
            self.keys = keyfile.read().split()

    def __contains__(self, key):
        return key in self.keys

    def __iter__(self):
        return iter(self.keys)

    def add(self, key):
        with open(KEYPATH, 'a') as keyfile:
            keyfile.write('\n' + key)


class Logs():
    @classmethod
    def initialize(cls, key):
        if exists(LOGPATH):
            return
        cls.write(key, prefix='')

    @classmethod
    def write(cls, key, prefix='\n'):
        now = Datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        with open(LOGPATH, 'a') as logfile:
            logfile.write(now + ' ' + key + '\n')

    @classmethod
    def cat(cls):
        with open(LOGPATH) as logfile:
            return print(logfile.read())


def initialize():
    mkdir()
    key = 'stop'
    Keys.initialize(key)
    Logs.initialize(key)


def show_report():
    print('nothing here')


def jrnl(key, add, init, show, report):
    """ Mark start of activity on key, or return. """
    # init
    if init:
        return initialize()

    # report
    if report:
        return show_report(key)

    keys = Keys()

    # keys
    if show:
        for key in keys:
            print(key)
        return

    # print
    if key is None:
        return Logs.cat()

    # add key
    if add:
        if key in keys:
            print('Key "{}" is already in the keyfile.'.format(key))
        else:
            keys.add(key)
        return

    # log a line
    if key not in keys:
        print('Key "{}" is not in the keyfile.'.format(key))
    else:
        Logs.write(key)


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('key', nargs='?')
    parser.add_argument('-a', '--add', action='store_true')
    parser.add_argument('-i', '--init', action='store_true')
    parser.add_argument('-s', '--show', action='store_true')
    parser.add_argument('-r', '--report', action='store_true')
    return parser


def main():
    """ Call jrnl with args from parser. """
    kwargs = vars(get_parser().parse_args())
    jrnl(**kwargs)


if __name__ == '__main__':
    main()

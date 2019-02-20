# -*- coding: utf-8 -*-
"""
Timekeeper.

Call without arguments for todays report.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import collections
import os

from datetime import datetime as Datetime, timedelta as Timedelta
from os.path import exists, join


NOW = Datetime.now()

# locations
HOME = os.environ['HOME']
DIRNAME = '.jrnl'
DIRPATH = join(HOME, DIRNAME)

LOGFORMAT = join(DIRPATH, '%Y-%m-%d_log')
LOGPATH = NOW.strftime(LOGFORMAT)

KEYPATH = join(DIRPATH, 'keys')

# format of timestamp within a logfile
TIME_FORMAT = '%H:%M:%S'


def mkdir():
    os.makedirs(DIRPATH, exist_ok=True)


def remove_micros(timedelta):
    """ Remove microseconds. """
    return timedelta - Timedelta(microseconds=timedelta.microseconds)


class Keys():
    def __init__(self):
        if exists(KEYPATH):
            with open(KEYPATH) as keyfile:
                self._keys = set(keyfile.read().split(','))
        else:
            self._keys = set()

    def __contains__(self, key):
        return key in self._keys

    def __iter__(self):
        return iter(self._keys)

    def remove(self, key):
        self._keys.remove(key)
        with open(KEYPATH, 'w') as keyfile:
            keyfile.write(','.join(self._keys))

    def add(self, key):
        self._keys.add(key)
        with open(KEYPATH, 'w') as keyfile:
            keyfile.write(','.join(self._keys))


class Logs():
    @classmethod
    def initialize(cls, key):
        if exists(LOGPATH):
            return
        cls.write(key, prefix='')

    @classmethod
    def write(cls, key, prefix='\n'):
        now = Datetime.now().strftime(TIME_FORMAT)
        with open(LOGPATH, 'a') as logfile:
            logfile.write(now + ' ' + key + '\n')

    @classmethod
    def cat(cls):
        with open(LOGPATH) as logfile:
            return print(logfile.read())

    @classmethod
    def report(cls):
        result = collections.defaultdict(Timedelta)
        with open(LOGPATH) as logfile:

            # first line
            date = NOW.date()
            text, previous_key = next(logfile).split()
            previous_time = Datetime.strptime(text, TIME_FORMAT).time()
            previous_datetime = Datetime.combine(date, previous_time)

            # remaining lines
            for line in logfile:
                text, current_key = line.split()
                current_time = Datetime.strptime(text, TIME_FORMAT).time()
                current_datetime = Datetime.combine(date, current_time)
                result[previous_key] += current_datetime - previous_datetime

                # current becomes previous
                previous_datetime = current_datetime
                previous_key = current_key

            # add unfinished time
            result[previous_key] += NOW - previous_datetime

        for key, value in result.items():
            print(remove_micros(value), key)


def jrnl(key, add, remove, show, cat):
    """ Mark start of activity on key, or return. """
    # add a key
    if add:
        Keys().add(key)
        return

    # remove a key
    if remove:
        Keys().remove(key)
        return

    # log a line
    if key:
        if key not in Keys():
            print('Key "%s" is not in %s (use --add)' % (key, KEYPATH))
        else:
            Logs.write(key)
        return

    # show keys
    if show:
        for key in Keys():
            print(key)
        return

    # cat the current log
    if cat:
        return Logs.cat()

    # get report for the current log
    return Logs.report()


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'key', nargs='?',
        help='Start working on some key.'
    )
    parser.add_argument(
        '-c', '--cat', action='store_true',
        help='Print the current log.',
    )
    # keys management
    parser.add_argument(
        '-s', '--show', action='store_true',
        help='Show the list of usable keys',
    )
    parser.add_argument(
        '-a', '--add', action='store_true',
        help='add a key to the list of usable keys.'
    )
    parser.add_argument(
        '-r', '--remove', action='store_true',
        help='remove a key from the list of usable keys.'
    )
    return parser


def main():
    """ Call jrnl with args from parser. """
    kwargs = vars(get_parser().parse_args())
    jrnl(**kwargs)


if __name__ == '__main__':
    main()

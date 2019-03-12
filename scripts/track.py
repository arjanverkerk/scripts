# -*- coding: utf-8 -*-
"""
Timetracker using curses.

Room for improvement:
- A message with timeout when a duplicate name is rejected at first row.
- An automatic backup even when activities are not switched.
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from curses import curs_set, echo, noecho, wrapper, A_BOLD, A_NORMAL
from datetime import datetime as Datetime, timedelta as Timedelta
from os.path import exists

KEYS = '123456789bcdefghijklmoprstuvwxyz'
ORDS = [ord(k) for k in KEYS]
DATE = '%Y-%m-%d %H:%M:%S'
NAMEWIDTH = 12
NAMESTART = len(DATE) + 3  # two extra for the year expansion
NAMESLICE = slice(NAMESTART, NAMESTART + NAMEWIDTH)
TIMESLICE = slice(NAMESLICE.stop + 1, None)
ACTIVITYRECORD = '%s {name:<%ss} {time}\n' % (DATE, NAMEWIDTH)


class Widget(object):
    """ Anything with a fixed location in a window. """
    def __init__(self, window, y, x):
        self.window = window
        self.y = y
        self.x = x


class Chart(Widget):
    """ The main table. """
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # table
        header = '#    activity      time  '
        spacer = '-  ------------  --------'
        footer = 'press a to add, q to quit'
        self.window.addstr(self.y + 0, 0, header)
        self.window.addstr(self.y + 1, 0, spacer)
        self.window.addstr(self.y + 2, 0, spacer)
        self.window.addstr(self.y + 3, 0, footer)

        # stack
        self._items = []
        self.active = []

        # backup
        self.path = path
        if self.path is not None and exists(self.path):
            self._load()
        else:
            self.add('idle')
            self.toggle(1)

    def __len__(self):
        return len(self._items)

    def _load(self):
        """ Restore state from file. """
        # parser for the file
        def parse(f):
            for line in f:
                yield line[NAMESLICE].strip(), float(line[TIMESLICE])

        # aggregate into dict
        with open(self.path) as f:
            names_and_times = {name: time for name, time in parse(f)}

        # add them
        for name, time in names_and_times.items():
            self.add(name=name, time=time)

    def _draw(self, item):
        """ Draw item. """
        index = self._items.index(item)
        key = KEYS[index]
        attr = A_BOLD if item.active else A_NORMAL
        row = str(key) + '  ' + str(item)
        self.window.addstr(self.y + index + 2, 0, row, attr)

    def _disable(self):
        """
        Disable any active items.

        Records final time if there is a path.
        """
        while self.active:
            # disable
            item = self.active.pop()
            item.stop()
            self._draw(item)
            # log state of item
            if self.path:
                template = Datetime.now().strftime(ACTIVITYRECORD)
                name = item.name
                time = item.time.total_seconds()
                with open(self.path, 'a') as f:
                    f.write(template.format(name=name, time=time))

    def _enable(self, key):
        """ Enable item with number no. """
        item = self._items[KEYS.index(key)]
        item.start()
        self._draw(item)
        self.active.append(item)

    def add(self, name, time=0):
        """ Add an activity. """
        # prevent duplicates
        if name in [i.name for i in self._items]:
            return

        # add item
        self.window.move(self.y + 2 + len(self._items), 0)
        self.window.insertln()
        item = Activity(name=name, time=time)
        self._items.append(item)
        self._draw(item)

    def toggle(self, key=None):
        """ Disable all active items, enable item with number no. """
        self._disable()
        if key is not None:
            self._enable(key)

    def update(self):
        """ Draw active item. """
        for item in self.active:
            self._draw(item)


class Activity(object):
    """ Name and time. """
    def __init__(self, name, time):
        self._previous = Timedelta(seconds=time)
        self._last = None
        self.name = name

    def start(self):
        self._last = Datetime.now()

    def stop(self):
        self._previous += Datetime.now() - self._last
        self._last = None

    @property
    def time(self):
        """ Return combined previous and elapsed time, rounded to seconds. """
        result = self._previous
        if self.active:
            result += Datetime.now() - self._last
        return result

    @property
    def active(self):
        return self._last is not None

    def __str__(self):
        time = self.time
        time -= Timedelta(microseconds=time.microseconds)  # strip micros
        return '{:<12s}  {:>8s}'.format(self.name, str(time))


class Reader(Widget):
    """ Read text. """
    def _pre(self):
        self.window.timeout(-1)
        curs_set(1)
        echo()

    def _post(self):
        self.window.timeout(1000)
        curs_set(0)
        noecho()

    def read(self, message, length):
        self._pre()
        self.window.addstr(self.y, self.x, message)
        position = self.x + len(message)
        result = self.window.getstr(self.y, position, length).decode('utf-8')
        self.window.addstr(self.y, self.x, ' ' * (len(message) + length))
        self._post()
        return result


def track(window, path):
    # general
    window.timeout(1000)
    curs_set(0)
    noecho()

    # widgets
    reader = Reader(window=window, y=0, x=0)
    chart = Chart(path=path, window=window, y=1, x=0)

    # main loop
    while True:
        c = window.getch(0, 0)
        if c == ord('a') and len(chart) < len(KEYS):
            name = reader.read('New activity: ', NAMEWIDTH)
            chart.add(name)
        if c == ord('q'):
            chart.toggle()
            break
        if c in ORDS[:len(chart)]:
            chart.toggle(KEYS[ORDS.index(c)])
        chart.update()


def get_parser():
    """ Return argument parser. """
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'path',
        nargs='?',
        metavar='FILE',
        help='File to use for backup and restore.'
    )
    return parser


def main():
    """ Call wrapped track with args from parser. """
    wrapper(track, **vars(get_parser().parse_args()))


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
Timetracker using curses.
"""

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from curses import A_BOLD, A_NORMAL
from curses import curs_set, echo, noecho, wrapper, use_default_colors
from datetime import datetime as Datetime, timedelta as Timedelta
from os.path import exists

# key definitions
KEYS = '123456789bcdefghijklmoprstuvwxyz'
ORDS = [ord(k) for k in KEYS]

# width of activity names
NAMEWIDTH = 12

# stored record configuration
ACTIVITYRECORD = '%Y-%m-%d %H:%M:%S {name} {time}\n'


class Widget(object):
    """ Anything with a fixed location in a window. """
    def __init__(self, window, y, x):
        self.window = window
        self.y = y
        self.x = x


class Line(Widget):
    """ Mulifunctional statusline. """
    WIDTH = 25

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._header = 'press a to add, q to quit'
        self._messages = {}
        self.update()

    def display(self, text, seconds=None):
        """
        Display text for some seconds.

        If seconds is None, set text as header.
        """
        if seconds is None:
            # a new header
            self._header = text
        else:
            # add to messages
            timedelta = Timedelta(seconds=seconds)
            if self._messages:
                until = max(self._messages) + timedelta
            else:
                until = Datetime.now() + timedelta
            self._messages[until] = text

        # draw
        self.update()

    def update(self):
        """ Draw current message or default header. """
        now = Datetime.now()
        for until in sorted(self._messages):
            if until < now:
                # discard outdated
                del self._messages[until]
                continue
            # draw message
            self._draw(self._messages[until])
            break  # skips the else clause of the for loop
        else:
            # no message was drawn, draw header
            self._draw(self._header)

    def read(self, text, length):
        self._pre()
        self._draw(text)
        position = self.x + len(text)
        result = self.window.getstr(self.y, position, length).decode('utf-8')

        self._post()
        return result

    def _draw(self, text):
        blank = ' ' * (self.WIDTH - len(text))
        self.window.addstr(self.y, self.x, text + blank)

    def _pre(self):
        self.window.timeout(-1)
        curs_set(1)
        echo()

    def _post(self):
        self.window.timeout(1000)  # milliseconds
        curs_set(0)
        noecho()


class Chart(Widget):
    """ The main table. """
    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # table
        header = '#    activity      time  '
        spacer = '-  ------------  --------'
        self.window.addstr(self.y + 0, 0, header, A_BOLD)
        self.window.addstr(self.y + 1, 0, spacer)
        self.window.addstr(self.y + 2, 0, spacer)

        # stack
        self._items = []
        self.active = []

        # backup
        self.path = path
        if self.path is not None and exists(self.path):
            self._load()
        else:
            self.add('idle')
        self.toggle(KEYS[0])

    def __len__(self):
        return len(self._items)

    def __contains__(self, name):
        return name in [i.name for i in self._items]

    def _load(self):
        """ Restore state from file. """
        # parser for the file
        def parse(f):
            for line in f:
                parts = line.split()[2:]
                yield parts[0], float(parts[1])

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
                time = round(item.time.total_seconds())
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


def track(window, path):
    # general
    use_default_colors()
    window.timeout(1000)
    curs_set(0)
    noecho()

    # widgets
    line = Line(window=window, y=0, x=0)
    chart = Chart(path=path, window=window, y=1, x=0)

    # main loop
    while True:
        c = window.getch(0, 0)
        if c == ord('a') and len(chart) < len(KEYS):
            name = line.read('new activity: ', NAMEWIDTH)
            if not name:
                line.display('cannot add empty name', seconds=3)
            elif ' ' in name:
                line.display('no spaces allowed in name', seconds=3)
            elif name in chart:
                line.display('"%s" already exists' % name, seconds=3)
            else:
                chart.add(name)
                if len(chart) == len(KEYS):
                    line.display('press q to quit')
        if c == ord('q'):
            chart.toggle()  # write a line to the log
            break
        if c in ORDS[:len(chart)]:
            chart.toggle(KEYS[ORDS.index(c)])

        chart.update()
        line.update()


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

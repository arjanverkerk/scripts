# -*- coding: utf-8 -*-
"""
Timetracker using curses.
"""
from curses import curs_set, echo, noecho, wrapper, A_BOLD, A_NORMAL
from datetime import datetime as Datetime, timedelta as Timedelta
from logging import basicConfig, getLogger, DEBUG

"""
The goal is that numbers select the current line
Idea is that clock of active line is added to updater, and not the rest.
Use insert and delete lines to shift header and footer automatically
"""
FMT = '%H:%M:%S'

logger = getLogger()


class Widget(object):
    def __init__(self, window, y, x):
        self.window = window
        self.y = y
        self.x = x


class Updater(set):
    """ Container for updateables. """
    def update(self):
        for item in self:
            item.update()


class Clock(Widget):
    """ Clock. """
    def update(self):
        content = str(Datetime.now().strftime(FMT))
        self.window.addstr(self.y, self.x, content)
        self.window.refresh()


class Chart(Widget):
    """ The main table. """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.items = []

        # scaffolding
        self.header = '#    activity      time  '
        self.spacer = '-  ------------  --------'
        self.footer = 'press a to add, q to quit'

        # init
        self.window.addstr(self.y + 0, 0, self.header)
        self.window.addstr(self.y + 1, 0, self.spacer)

        # row
        self.row = '{:d}  {:<12s}  00:00:00'
        self.width = 25

    def update(self):
        for no, item in enumerate(self.items, 1):
            attr = A_BOLD if no % 2 else A_NORMAL
            row = self.row.format(no, str(item))
            self.window.addstr(self.y + no + 1, 0, row, attr)
        self.window.addstr(self.y + no + 2, 0, self.spacer)
        self.window.addstr(self.y + no + 3, 0, self.footer)


class Activity(object):
    """ Key and time. """
    def __init__(self, key):
        self.time = Timedelta()
        self.key = key

    def __str__(self):
        return self.key


class Reader(Widget):
    """ Read text. """
    def pre(self):
        self.window.timeout(-1)
        curs_set(1)
        echo()

    def post(self):
        self.window.timeout(1000)
        curs_set(0)
        noecho()

    def read(self, message, length):
        self.pre()
        self.window.addstr(self.y, self.x, message)
        position = self.x + len(message)
        result = self.window.getstr(self.y, position, length).decode('utf-8')
        self.window.addstr(self.y, self.x, ' ' * (len(message) + length))
        self.post()
        return result


def track(window, **kwargs):
    # general
    window.timeout(1000)
    curs_set(0)
    noecho()

    # clock & chart
    clock = Clock(window, 0, 19)
    chart = Chart(window, 2, 0)

    # initial testdata
    chart.items.append(Activity('zingen'))
    chart.items.append(Activity('vechten'))
    chart.items.append(Activity('lachen'))

    updater = Updater([clock, chart])
    updater.update()

    reader = Reader(window, 1, 0)

    # main loop
    while True:
        c = window.getch(0, 0)
        if c == ord('q'):
            break
        if c == ord('a'):
            item = reader.read('New activity: ', 12)
            chart.items.append(Activity(item))
        if c == ord('x'):
            pass  # TODO remove active line
            logger.info(c)
        if c == ord('j'):
            pass  # TODO move active line up
            logger.info(c)
        if c == ord('k'):
            pass  # TODO move active line down
            logger.info(c)
        if ord('0') <= c <= ord('9'):
            pass  # TODO toggle activity
            logger.info(c)
        updater.update()


def main():
    basicConfig(filename='track.log', level=DEBUG)
    logger.info(80 * '-')
    wrapper(track)


if __name__ == '__main__':
    main()

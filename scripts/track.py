# -*- coding: utf-8 -*-
"""
Timetracker using curses.
"""
from curses import curs_set, echo, noecho, wrapper
from datetime import datetime as Datetime

import argparse
import threading

"""
Update the clocks in a thread
Extend the header number, key, time, active
Number the keys
Move keys
Remove keys
Select keys
Track keys
Export / import functionality
Update loop updating clock and active key
"""




class Clock(object):
    def __init__(self, window):
        self.window = window.subwin(3, 10, 1, 1)
        # self.window=window
        self.window.border()
        self.update()

    def update(self):
        self.window.addstr(1, 1, str(Datetime.now().strftime('%H:%M:%S')))
        self.window.refresh()


def activate(window):
    window.timeout(-1)
    curs_set(2)
    echo()


def deactivate(window):
    curs_set(0)
    window.timeout(1000)
    noecho()


def track(window, **kwargs):
    window.border()
    deactivate(window)
    keys = set()

    # header
    window.addstr(5, 1, 'allowed keys')
    window.addstr(6, 1, '------------')

    clock = Clock(window)

    while True:
        clock.update()
        c = window.getch(10, 10)
        if c == ord('q'):
            break
        if c == ord('a'):
            msg = 'Enter new key: '
            window.addstr(4, 1, msg)
            activate(window)
            k = (window.getstr(4, len(msg), 16)).decode('utf-8')
            deactivate(window)
            window.addstr(4, 1, ' ' * (len(msg) + len(k)))
            keys.add(k)
            for i, k in enumerate(keys):
                window.addstr(7 + i, 1, '[ ] %d %s' % (i, k))


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(description=__doc__)
    return parser


def main():
    """ Call jrnl with args from parser. """
    kwargs = vars(get_parser().parse_args())
    wrapper(track, **kwargs)


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
Timetracker using curses.
"""
from curses import curs_set, echo, noecho, wrapper
from datetime import datetime as Datetime

import argparse

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


def clock(window):
    window.addstr(0, 0, str(Datetime.now().strftime('%H:%S')))


def activate(window):
    window.timeout(-1)
    curs_set(2)
    echo()


def deactivate(window):
    curs_set(0)
    window.timeout(1000)
    noecho()


def track(window, **kwargs):
    deactivate(window)
    keys = set()

    # header
    window.addstr(3, 0, 'allowed keys')
    window.addstr(4, 0, '------------')

    while True:
        clock(window)
        c = window.getch(10, 10)
        if c == ord('q'):
            break
        if c == ord('a'):
            msg = 'Enter new key: '
            window.addstr(1, 0, msg)
            activate(window)
            k = (window.getstr(1, len(msg), 16)).decode('utf-8')
            deactivate(window)
            window.addstr(1, 0, ' ' * (len(msg) + len(k)))
            keys.add(k)
            for i, k in enumerate(keys):
                window.addstr(5 + i, 0, '[ ] %d %s' % (i, k))


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

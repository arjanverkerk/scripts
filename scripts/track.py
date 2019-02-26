# -*- coding: utf-8 -*-
"""
Timetracker using curses.
"""
from curses import curs_set, echo, wrapper
from datetime import datetime as Datetime

import time
import argparse

"""
Add key
Remove key
Select key
"""

def track(window, **kwargs):
    # no cursor
    curs_set(0)
    
    # echo on, because wrapper disables it
    echo()

    # window.clear()
    # window.refresh()


    window.timeout(1000)
    window.addstr(5, 5, 'test')
    window.addstr(6, 5, 'test two')

    while True:
        c = window.getch(10, 10)
        if c == ord('q'):
            break
        window.addstr(7, 5, str(Datetime.now()))


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

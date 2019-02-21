from curses import wrapper
from curses import curs_set

import time

def main(stdscr):
    # no cursor
    curs_set(0)

    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    stdscr.addstr(5, 5, 'test')
    stdscr.refresh()
    time.sleep(1)

    stdscr.addstr(6, 5, 'test two')
    time.sleep(1)
    stdscr.refresh()
    time.sleep(1)

wrapper(main)

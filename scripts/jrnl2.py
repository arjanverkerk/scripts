from curses import wrapper
from curses import echo
from curses import curs_set

import time
from datetime import datetime as Datetime

"""
Key to add key
Keys to select
"""

def main(window):
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

wrapper(main)

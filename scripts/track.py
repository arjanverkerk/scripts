# -*- coding: utf-8 -*-
"""
Timetracker using curses.
"""
from curses import curs_set, echo, noecho, wrapper
from datetime import datetime as Datetime
from time import sleep
from threading import Thread

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

update_items = set()


def update():
    while True:
        for item in update_items:
            item.update()
        sleep(1)


class Clock(object):
    def __init__(self, window):
        self.window = window.subwin(3, 10, 1, 1)
        self.update()

    def update(self):
        original = self.window.getyx()
        self.window.addstr(1, 1, str(Datetime.now().strftime('%H:%M:%S')))
        self.window.move(*original)
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
    deactivate(window)
    keys = set()

    # header
    window.addstr(5, 1, 'allowed keys')
    window.addstr(6, 1, '------------')

    # clock
    clock = Clock(window)
    update_items.add(clock)

    # update thread
    updater = Thread(target=update)
    updater.daemon = True
    updater.start()

    while True:
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


def main():
    wrapper(track)


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
"""
Timetracker using curses.

TODO
- commandline add a backup file to create or resume
- write on each toggle or addition
- using it in an alias can put a week number in it
- think about the limit on keys - maybe add letters, F-keys
"""
from curses import curs_set, echo, noecho, wrapper, A_BOLD, A_NORMAL
from datetime import datetime as Datetime, timedelta as Timedelta


class Widget(object):
    """ Anything with a fixed location in a window. """
    def __init__(self, window, y, x):
        self.window = window
        self.y = y
        self.x = x


class Chart(Widget):
    """ The main table. """
    def __init__(self, *args, **kwargs):
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
        self.items = []
        self.active = []

        # idle
        self.add('idle')
        self.toggle(1)

    def __len__(self):
        return len(self.items)

    def add(self, name):
        """ Add an activity. """
        self.window.move(self.y + 2 + len(self.items), 0)
        self.window.insertln()
        item = Activity(name)
        self.items.append(item)
        self.draw(item)

    def draw(self, item):
        """ Draw item. """
        no = self.items.index(item) + 1
        attr = A_BOLD if item.active else A_NORMAL
        row = str(no) + '  ' + str(item)
        self.window.addstr(self.y + no + 1, 0, row, attr)

    def toggle(self, no):
        """ Disable all active items, enable item with number no. """
        # disable
        while self.active:
            item = self.active.pop()
            item.stop()
            self.draw(item)

        # enable
        item = self.items[no - 1]
        item.start()
        self.draw(item)
        self.active.append(item)

    def update(self):
        """ Draw active item. """
        for item in self.active:
            self.draw(item)


class Activity(object):
    """ Key and time. """
    def __init__(self, key):
        self.previous = Timedelta()
        self.last = None
        self.key = key

    def start(self):
        self.last = Datetime.now()

    def stop(self):
        self.previous += Datetime.now() - self.last
        self.last = None

    @property
    def time(self):
        """ Return combined previous and elapsed time, rounded to seconds. """
        result = self.previous
        if self.active:
            result += Datetime.now() - self.last
        return result

    @property
    def active(self):
        return self.last is not None

    def __str__(self):
        time = self.time
        time -= Timedelta(microseconds=time.microseconds)  # strip micros
        return '{:<12s}  {:>8s}'.format(self.key, str(time))


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


def track(window, **kwargs):
    # general
    window.timeout(1000)
    curs_set(0)
    noecho()

    # widgets
    reader = Reader(window, 0, 0)
    chart = Chart(window, 1, 0)
    chart.update()

    # main loop
    while True:
        c = window.getch(0, 0)
        if c == ord('q'):
            break
        if c == ord('a') and len(chart) < 9:
            name = reader.read('New activity: ', 12)
            chart.add(name)
        if ord('1') <= c <= ord(str((len(chart)))):
            chart.toggle(c - ord('0'))
        chart.update()


def main():
    wrapper(track)


if __name__ == '__main__':
    main()

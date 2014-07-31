#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals


import sys
from itertools import chain, cycle


BLACK = 'BLACK'
BLUE = 'BLUE'
GREEN = 'GREEN'
RED = 'RED'
YELLOW = 'YELLOW'

if sys.hexversion >= 0x03000000:
    raw_input = input
    xrange = range
    range = lambda *a, **kw: list(xrange(*a, **kw))
else:
    from codecs import open


def uni_open(filename):
    return open(filename, mode='r', encoding='utf-8')


class ColorText(object):
    def __init__(self, base_color=GREEN):
        if base_color == RED:
            self.base = self.make_color(self.get_red())
        elif base_color == GREEN:
            self.base = self.make_color(self.get_green())
        elif base_color == BLUE:
            self.base = self.make_color(self.get_blue())
        elif base_color == YELLOW:
            self.base = self.make_color(self.get_yellow())
        elif base_color == BLACK:
            self.base = self.make_color(self.get_black())

        self.colors = cycle(self.base)
        self.color = next(self.colors)

    def _set_color(self, fg):
        result = ''
        if fg:
            result += '\x1b[38;5;%dm' % fg
        return result

    def reset_color(self):
        print('\x1b[0m', end='')

    def make_color(self, color_list):
        return list(
            chain(
                *map(
                    lambda c: (c,) * 5,
                    (lambda l: l+l[::-1])(color_list)
                )
            )
        )

    def rgb(self, red, green, blue):
        return (red * 36) + (green * 6) + blue + 16

    def get_red(self):
        return [self.rgb(i, 0, 0) for i in xrange(1, 6)]

    def get_green(self):
        return [self.rgb(0, i, 0) for i in xrange(1, 6)]

    def get_blue(self):
        return [self.rgb(0, 0, i) for i in xrange(1, 6)]

    def get_yellow(self):
        return [self.rgb(i, i, 0) for i in xrange(1, 6)]

    def get_black(self):
        return range(232, 242)

    def colorize_file(self, _file):
        for i, line in enumerate(_file, start=2):
            print(self.colorize(line, i), end='')

    def colorize(self, line, i):
        new_line = []
        for c in line:
            color = self._set_color(self.color)
            new_line.append(color + c)
            self.color = next(self.colors)

        self.colors = cycle(self.base)
        while i:
            i -= 1
            next(self.colors)

        return ''.join(new_line)


def main():
    ct = ColorText()
    for filename in sys.argv[1:] or ['-']:
        if filename == '-':
            try:
                while True:
                    ct.reset_color()
                    t = raw_input()
                    print(ct.colorize(t))
            except EOFError:
                pass
            except KeyboardInterrupt:
                print()
            finally:
                sys.exit(0)
        else:
            with uni_open(filename) as _file:
                ct.colorize_file(_file)
    ct.reset_color()

if __name__ == '__main__':
    main()

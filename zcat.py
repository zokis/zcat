#!/usr/bin/env python
from __future__ import print_function
from __future__ import unicode_literals


import math
import sys
from itertools import chain, cycle
from optparse import OptionParser


BLACK = 'BLACK'
BLUE = 'BLUE'
GREEN = 'GREEN'
PURPLE = 'PURPLE'
RAINBOW = 'RAINBOW'
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
    def __init__(self, base_color=RAINBOW, columns=15, color_list=None):
        self.columns = columns
        self.i = 2
        if not color_list is None:
            self.base = self.make_color(color_list)
        elif base_color == RAINBOW:
            self.base = self.make_color(self.get_rainbow())
        elif base_color == RED:
            self.base = self.make_color(self.get_red())
        elif base_color == GREEN:
            self.base = self.make_color(self.get_green())
        elif base_color == BLUE:
            self.base = self.make_color(self.get_blue())
        elif base_color == YELLOW:
            self.base = self.make_color(self.get_yellow())
        elif base_color == BLACK:
            self.base = self.make_color(self.get_black())
        elif base_color == PURPLE:
            self.base = self.make_color(self.get_purple())
        else:
            self.base = self.make_color(self.get_red())

        self.colors = cycle(self.base)
        self.color = next(self.colors)

    def _set_color(self, fg):
        result = ''
        if fg:
            result += '\x1b[38;5;%dm' % fg
        # if bg:
        #     result += '\x1b[48;5;%dm' % bg
        return result

    def reset_color(self):
        print('\x1b[0m', end='')

    def make_color(self, color_list):
        return list(
            chain(
                *map(
                    lambda c: (c,) * self.columns,
                    (lambda l: l[1:]+l[::-1][:-1])(color_list)
                )
            )
        )

    def rgb(self, red, green, blue, hue=16):
        return (red * 36) + (green * 6) + blue + hue

    def rainbow(self, X):
        red = (math.sin(X) * 127) + 128
        green = (math.sin(X + 2*math.pi/3.0) * 127) + 128
        blue = (math.sin(X + 4*math.pi/3.0) * 127) + 128
        return map(lambda x: int((x*5)/255.0), (red, green, blue))

    def get_simple_rainbow_hue(self, hue, size=16):
        return [
            self.rgb(
                *self.rainbow(X),
                hue=hue
            ) for X in xrange(1, size)
        ]

    def get_rainbow(self):
        return list(
            chain(
                *zip(
                    self.get_simple_rainbow_hue(16),
                    self.get_simple_rainbow_hue(17)
                )
            )
        )

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

    def get_purple(self):
        return [self.rgb(i, 0, i, hue=0) for i in xrange(1, 6)]

    def colorize_file(self, _file):
        for i, line in enumerate(_file, start=2):
            print(self.colorize(line, i), end='')

    def colorize(self, line, i=None):
        if i is None:
            i = self.i
            self.i += 1

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


def main(argv):
    opar = OptionParser()
    opar.add_option("-C", "--columns", dest="columns",
                    help="columns", type="int", default=5)
    opar.add_option("-c", "--color", dest="color",
                    help="Colors: RED BLUE GREEN YELLOW BLACK and RAINBOW", type="str", default=RAINBOW)

    options, args = opar.parse_args(argv)

    ct = ColorText(base_color=options.color, columns=options.columns)
    for filename in args[1:] or ['-']:
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
    main(sys.argv)

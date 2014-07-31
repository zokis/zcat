#!/usr/bin/env python
from __future__ import print_function


import sys
from itertools import chain


def cycle(_iter):
    l = len(_iter)
    i = 0
    while True:
        yield _iter[i % l]
        i += 1


class ColorText(object):
    def __init__(self):
        self.base = self.make_color(self.get_green())

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

    def get_green(self):
        return [self.rgb(0, i, 0) for i in xrange(1, 6)]

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
        with open(filename, 'rb') as _file:
            ct.colorize_file(_file)
    ct.reset_color()

if __name__ == '__main__':
    main()

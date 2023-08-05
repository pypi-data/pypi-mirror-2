#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Dililatum: a quest system for simple RPGs
# Copyright (C) 2010  Niels Serup

# This file is part of Dililatum.
#
# Dililatum is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dililatum is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dililatum.  If not, see <http://www.gnu.org/licenses/>.

##[ Name        ]## bitmap
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the BitMap class which enable bits to be
                  # stored as bits and not bytes

import numpy

class BitMap:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arr = numpy.zeros((x, y/8), dtype=numpy.int8)

    def load(self, filename):
        f = open(filename, 'rb')
        c = f.read()
        p = 0
        for j in range(self.x):
            for i in range(self.y/8):
                self.arr[j][i] = ord(c[p])
                p += 1
        f.close()

    def set(self, x, y, do=True):
        try:
            p = self.arr[x][y/8]
        except IndexError:
            return
        tmp = 1;
        for i in range(y % 8):
            tmp *= 2
        if do and not self.get(x, y):
            self.arr[x][y/8] += tmp
        elif not do and self.get(x, y):
            self.arr[x][y/8] -= tmp

    def unset(self, x, y):
        self.set(x, y, False)

    def get(self, x, y):
        try:
            p = self.arr[x][y/8]
        except IndexError:
            return
        tmp = 1;
        for i in range(int(y % 8)):
            tmp *= 2
        return (p / tmp) % 2 == 1

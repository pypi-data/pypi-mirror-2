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

##[ Name        ]## various
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Various minor (but still important) parts


import sys
from threading import Thread

def read_file(filename, throw_exceptions=False):
    if not throw_exceptions:
        try:
            f = open(filename, 'U')
            return f.read()
        except Exception:
            return ''
    else:
        f = open(filename)
        return f.read()

def error(msg, cont=True, pre=None):
    errstr = msg + '\n'
    if pre is not None:
        errstr = pre + ': ' + errstr
    sys.stderr.write(errstr)
    if cont is not True:
        try:
            sys.exit(cont)
        except Exception:
            sys.exit(1)

def usable_error(msg, cont=True):
    error(msg, cont, 'dililatum: ')


class thread(Thread):
    def __init__(self, func, *args):
        Thread.__init__(self)
        self.func = func
        self.args = args
        self.setDaemon(True) # self.daemon = True
        self.start()

    def run(self):
        self.func(*self.args)


# Not running in daemon mode
class nthread(Thread):
    def __init__(self, func, *args):
        Thread.__init__(self)
        self.func = func
        self.args = args
        self.start()

    def run(self):
        self.func(*self.args)

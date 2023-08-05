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

##[ Name        ]## font
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the Font class, which makes it possible
                  # to write text

import pygame
from pygame.locals import *
import math

class Font:
    def __init__(self, world, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default

        self.world = world
        self.path = get('path', None)
        self.size = get('size', 30)

        self.create_font()

    def create_font(self):
        self.font = pygame.font.Font(self.path, self.size)

    def split_text(self, text, width):
        spl = text.split('\n')
        r = []
        for x in spl:
            r.extend(self.split_text_pieces(x, width))
        return r

    def split_text_pieces(self, text, width):
        t = text[:]
        ts = []
        while t:
            tt = t[:]
            s = False
            while self.font.size(tt)[0] > width:
                nf = tt.rfind(' ')
                if nf != -1:
                    tt = tt[:nf]
                    s = True
                else:
                    tt = tt[:-1]
                    s = False
            ts.append(tt)
            if s:
                t = t[len(tt) + 1:]
            else:
                t = t[len(tt):]
        return ts

    def write(self, text, **oargs):
        color = oargs.get('color') or (0, 0, 0)
        antialias = oargs.get('antialias') or True
        split = oargs.get('split') or False
        indent_size = oargs.get('indent_size') or None
        indent_text = oargs.get('indent_text') or None
        if indent_text is not None and indent_size is None:
            indent_size = (20, 20)

        if not split:
            return self.font.render(text, antialias, color)
        else:
            fh = self.font.size('')[1]
            ts = self.split_text(text, split[0])
            tslen = len(ts)
            if indent_text:
                tsi = []
                tsisimp = []
                i = 0
                j = 0
                for x in indent_text:
                    st = self.split_text(x, split[0] -
                               indent_size[0])
                    tsi.append(st)
                    k = 0
                    for y in st:
                        tsisimp.append((y, k))
                        k += 1
                        j += 1
                    i += 1
                tsilen = i
                tsitotallen = j
                pposs = []
                surf_of_ans = []
            else:
                tsitotallen = 0

            rows_p_t = int(split[1] / fh)
            surfs = []
            # Needs commenting
            icount = 0
            for i in range(int(math.ceil(float(tslen + tsitotallen) / rows_p_t))):
                surf = pygame.Surface(split).convert_alpha()
                surf.fill(pygame.Color(0, 0, 0, 0))
                for j in range(rows_p_t):
                    n = i * rows_p_t + j
                    if n >= tslen:
                        if indent_text is None:
                            break
                        else:
                            n -= tslen
                            if n >= tsitotallen:
                                break
                            else:
                                tsimp = tsisimp[n]
                                if tsimp[1] == 0: # First line of an answer
                                    pposs.append((0, fh * j))
                                    if j == 0:
                                        ni = i - 1
                                    else:
                                        ni = i
                                    surf_of_ans.append((icount, ni))
                                    icount = i
                                tsurf = self.font.render(
                                    tsimp[0], antialias, color)
                                surf.blit(tsurf, (indent_size[0], fh * j))
                    else:
                        tsurf = self.font.render(ts[n], antialias, color)
                        surf.blit(tsurf, (0, fh * j))
                surfs.append(surf)
            if not indent_text:
                return surfs
            else:
                del surf_of_ans[0]
                surf_of_ans.append((icount, i))
                return surfs, pposs, surf_of_ans

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

##[ Name        ]## posmarker
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the OKPositionsMarker class to aid in
                  # marking where on a background characters can
                  # safely walk

import sys
import pygame
from pygame.locals import *
from dililatum.bitmap import BitMap

class NewSurface(pygame.Surface):
    def __init__(self, *args):
        pygame.Surface.__init__(self, *args)
        self.x = args[0][0]
        self.y = args[0][1]
        self.none = pygame.Color(0, 0, 0, 0)
        self.color = pygame.Color(18, 13, 228, 90)
        self.fill(self.none)

    def set_checkpoints(self, pos):
        self.positions = pos

    def set_at(self, x, y):
        pygame.Surface.set_at(self, (x, y), self.color)

    def del_at(self, x, y):
        pygame.Surface.set_at(self, (x, y), self.none)

    def add_rect(self, pos, size):
        s2 = size / 2
        x1 = pos[0] - s2
        y1 = pos[1] - s2
        x2 = pos[0] + s2
        y2 = pos[1] + s2
        if x1 < 0: x1 = 0
        if y1 < 0: y1 = 0

        for i in range(y1, y2):
            if i >= self.y: break
            for j in range(x1, x2):
                if j >= self.x: break
                if not self.positions.get(j, i):
                    self.set_at(j, i)
                    self.positions.set(j, i)

    def del_rect(self, pos, size):
        s2 = size / 2
        x1 = pos[0] - s2
        y1 = pos[1] - s2
        x2 = pos[0] + s2
        y2 = pos[1] + s2

        for i in range(y1, y2):
            for j in range(x1, x2):
                self.del_at(j, i)
                self.positions.unset(j, i)

class OKPositionsMarker:
    def __init__(self, imgfile, posfile):
        self.imgfile = imgfile
        self.posfile = posfile

        self.rect_size = 50

    def start(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('posmarker')
        self.img = pygame.image.load(self.imgfile).convert()
        self.points = NewSurface((640, 480), SRCALPHA)
        self.positions = BitMap(640, 480)
        self.points.set_checkpoints(self.positions)

        try:
            self.positions.load(self.posfile)
            for i in xrange(480):
                for j in xrange(640):
                    if self.positions.get(j, i):
                        self.points.set_at(j, i)
        except Exception:
            pass

        self.clock = pygame.time.Clock()
        self.loop()

    def end(self):
        self.positions.arr.tofile(self.posfile)

    def loop(self):
        done = False
        pressed = 0, 0, 0
        while not done:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
                    pressed = pygame.mouse.get_pressed()
                elif event.type == KEYDOWN:
                    if event.key == K_PAGEUP:
                        self.rect_size += 1
                        if self.rect_size > 100:
                            self.rect_size = 100
                    elif event.key == K_PAGEDOWN:
                        self.rect_size -= 1
                        if self.rect_size < 1:
                            self.rect_size = 1
                    elif event.key == K_ESCAPE:
                        done = True
                elif event.type == QUIT:
                    done = True
            point = pygame.mouse.get_pos()
            if pressed[0]:
                self.points.add_rect(point, self.rect_size)
            elif pressed[2]:
                self.points.del_rect(point, self.rect_size)

            self.screen.blit(self.img, (0, 0))
            self.screen.blit(self.points, (0, 0))
            pygame.display.flip()

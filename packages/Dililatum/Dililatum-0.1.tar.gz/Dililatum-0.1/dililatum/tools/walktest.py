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

##[ Name        ]## walktest
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains walk tests

from datetime import datetime
import os.path
import pygame
from pygame.locals import *


class WalkTestSimple:
    def __init__(self, files):
        self.files = files

    def start(self):
        pygame.display.init()

        self.screen = pygame.display.set_mode((300, 600))

        self.images = []
        for f in self.files:
            img = pygame.image.load(f)
            self.images.append((img.convert_alpha(), img.get_width(), img.get_height()))

        self.background = pygame.Surface(self.screen.get_size()).convert()

        self.clock = pygame.time.Clock()
        self.loop_images()

    def microseconds(self, tdelta):
        #return tdelta.microseconds + tdelta.seconds * 1000000 + \
        #    tdelta.min * 60000000
        return tdelta.microseconds

    def loop_images(self):
        done = False
        l = len(self.images)
        i = 0
        cr = 255
        cg = 0
        cb = 0

        time = datetime.now()
        while not done:
            self.clock.tick(30)
            #cr = 0
            #cg = 0
            #cb = 0
            self.background.fill((cr, cg, cb))
            self.screen.blit(self.background, (0, 0))
            img = self.images[i]
            self.screen.blit(img[0], ((300 - img[1]) / 2,
                                      (600 - img[2]) / 2))

            pygame.display.flip()
            if cr == 255 and cg < 255 and cb == 0:
                cg += 5
            elif cr > 0 and cg == 255 and cb == 0:
                cr -= 5
            elif cr == 0 and cg == 255 and cb < 255:
                cb += 5
            elif cr == 0 and cg > 0 and cb == 255:
                cg -= 5
            elif cr < 255 and cg == 0 and cb == 255:
                cr += 5
            elif cr == 255 and cg == 0 and cb > 0:
                cb -= 5
            if cr > 255: cr = 255
            elif cr < 0: cr = 0
            if cg > 255: cg = 255
            elif cg < 0: cg = 0
            if cb > 255: cb = 255
            elif cb < 0: cb = 0

            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        done = True
            if self.microseconds(datetime.now() - time) > 250000:
                i = (i + 1) % l
                time = datetime.now()


class WalkTestAdvanced:
    def __init__(self, sett):
        self.directory = sett.directory
        self.time = sett.time
        self.direction = sett.direction
        self.bgtype = sett.background
        self.shadow = sett.shadow
        self.size = (sett.width, sett.height)

        self.frames = {}

    def file2surface(self, dirname, files):
        for i in range(len(files)):
            img = pygame.image.load(os.path.join(self.directory,
                                                 dirname, files[i]))
            files[i] = (img.convert_alpha(),
                        img.get_width(),
                        img.get_height())
        return files

    def path_walk(self, name, dirname, files):
        self.frames[name] = self.file2surface(dirname, sorted(files))

    def start(self):
        pygame.display.init()

        self.screen = pygame.display.set_mode(self.size)

        for x in 'lt', 'ct', 'rt', 'lm', 'rm', 'lb', 'cb', 'rb':
            os.path.walk(os.path.join(self.directory, x), self.path_walk, x)

        self.bgsurface = \
            pygame.Surface(self.screen.get_size()).convert()

        if self.shadow:
            self.create_shadow()
        else:
            self.shadow = None

        self.clock = pygame.time.Clock()
        self.loop()

    def create_shadow(self):
        size = (self.size[0] / 2, self.size[1] / 15)
        ssize = [s * 3 for s in size]
        rect = pygame.Rect((0, 0), ssize)
        surf = pygame.Surface(ssize).convert_alpha()
        surf.fill(pygame.Color(0, 0, 0, 0))
        pygame.draw.ellipse(surf, pygame.Color(0, 0, 0, 200), rect)
        surf = pygame.transform.smoothscale(surf, size)

        self.shadow = surf
        self.shadow_pos = (self.size[0] - size[0]) / 2

    def microseconds(self, tdelta):
        return tdelta.microseconds

    def loop(self):
        done = False
        i = 0
        cflow = self.bgtype == 'colorflow'
        if cflow:
            cr = 255
            cg = 0
            cb = 0
        else:
            color = self.bgtype

        time = datetime.now()
        while not done:
            self.clock.tick(30)
            if cflow:
                color = (cr, cg, cb)
            self.bgsurface.fill(color)
            self.screen.blit(self.bgsurface, (0, 0))

            if i >= len(self.frames[self.direction]):
                i = 0
            img = self.frames[self.direction][i]

            if self.shadow is not None:
                self.screen.blit(self.shadow, (self.shadow_pos,
                (self.size[1] - img[2]) / 2 + img[2] - img[2] / 10))

            self.screen.blit(img[0], ((300 - img[1]) / 2,
                                      (600 - img[2]) / 2))

            pygame.display.flip()
            if cflow:
                if cr == 255 and cg < 255 and cb == 0:
                    cg += 5
                elif cr > 0 and cg == 255 and cb == 0:
                    cr -= 5
                elif cr == 0 and cg == 255 and cb < 255:
                    cb += 5
                elif cr == 0 and cg > 0 and cb == 255:
                    cg -= 5
                elif cr < 255 and cg == 0 and cb == 255:
                    cr += 5
                elif cr == 255 and cg == 0 and cb > 0:
                    cb -= 5
                if cr > 255: cr = 255
                elif cr < 0: cr = 0
                if cg > 255: cg = 255
                elif cg < 0: cg = 0
                if cb > 255: cb = 255
                elif cb < 0: cb = 0

            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        done = True
                    elif event.key == K_KP7 or event.key == K_7:
                        self.direction = 'lt'
                    elif event.key == K_KP8 or event.key == K_8:
                        self.direction = 'ct'
                    elif event.key == K_KP9 or event.key == K_9:
                        self.direction = 'rt'
                    elif event.key == K_KP4 or event.key == K_4:
                        self.direction = 'lm'
                    elif event.key == K_KP6 or event.key == K_6:
                        self.direction = 'rm'
                    elif event.key == K_KP1 or event.key == K_1:
                        self.direction = 'lb'
                    elif event.key == K_KP2 or event.key == K_2:
                        self.direction = 'cb'
                    elif event.key == K_KP3 or event.key == K_3:
                        self.direction = 'rb'

            if self.microseconds(datetime.now() - time) > self.time:
                i = (i + 1) % len(self.frames[self.direction])
                time = datetime.now()


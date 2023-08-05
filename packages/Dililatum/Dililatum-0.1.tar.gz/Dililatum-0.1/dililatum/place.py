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

##[ Name        ]## place
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the generic form of the Place class

import pygame
from pygame.locals import *
from dililatum.bitmap import BitMap

class Place:
    def __init__(self, world, imgfile=None, posfile=None, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default
        self.world = world
        self.imgfile = imgfile
        self.posfile = posfile
        self.name = None
        self.objects = []
        self.objects = get('objs', [])
        self.obj_names = {}
        self.dir_objects = {}
        self.bgsounds = get('bgsnd', [])

        if self.world.sys.etc.loadwait:
            self.load_imgfile()
            self.load_posfile()
        else:
            self.surf = None
            self.posoks = None

    def load_imgfile(self):
        if self.imgfile is not None:
            try:
                self.surf = pygame.image.load(self.imgfile).convert()
            except Exception:
                pass

    def load_posfile(self):
        if self.posfile is not None:
            try:
                bm = BitMap(*self.world.size)
                bm.load(self.posfile)
                self.posoks = bm
            except Exception:
                pass

    def add_object(self, obj):
        self.objects.append(obj)

    def set_direction_object(self, direction, obj):
        self.dir_objects[direction] = obj

    def remove_object(self, obj):
        self.objects.remove(obj)

    def char_size(self, pos):
        return 1.0

    def char_pos(self, pos):
        return pos

    def pos_ok(self, pos, size):
        if self.posoks is None:
            self.load_posfile()
        if self.posoks is None: # Still..
            return True
        else:
            height = self.char_size(pos) * \
                self.world.leading_character.get_frame().height / 20
            s0 = size[0] / 2
            posmh = pos[1] - height
            return self.posoks.get(*pos) and \
                self.posoks.get(pos[0] - s0, pos[1]) and \
                self.posoks.get(pos[0] + s0, pos[1]) and \
                self.posoks.get(pos[0], posmh) and \
                self.posoks.get(pos[0] - s0, posmh) and \
                self.posoks.get(pos[0] + s0, posmh) and \
                self.posoks.get(pos[0], (pos[1] + posmh) / 2)

    def draw(self, surf=None):
        if surf is None:
            surf = self.world
        if self.surf is None:
            self.load_imgfile()
        surf.blit(self.surf, (0, 0))


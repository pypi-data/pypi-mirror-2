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

##[ Name        ]## object
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the Object class whose purpose is to be
                  # drawn onto instances of Place classes (and thereby
                  # the screen)

import pygame
from pygame.locals import *

class Object:
    def __init__(self, world, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default

        self.world = world
        self.rel = get('rel', 0) # 1 for real position, 0 for
                                 # modified (visible) position
        self.action = get('action', None)
        self.unaction = get('unaction', None)
        self.visible = get('visible', True)
        self.pos = get('pos', (0, 0))
        self.size = get('size', None)
        self.area = get('area', None)
        self.areaadd = get('areaadd', (0, 0))
        self.in_area = False
        if self.size is None and self.pos is not None and \
                'append' in dir(self.pos[0]) and len(self.pos) > 1:
            self.size = self.pos[1]
            self.pos = self.pos[0]
        self.imgfile = get('imgfile', None)
        if self.imgfile is not None and self.world.sys.etc.loadwait:
            self.load_image()
        else:
            self.surf = None
        self.walkonact = get('walkonact', True)
        self.require_event = get('require', None)
        if self.require_event is not None:
            self.world.link_event(self.require_event[0],
                                  self.event_check)
            self.close_to_touch = False

    def get_bottom_area(self):
        if self.surf is None: self.load_image()
        try:
            if self.rel == 0:
                return [a[1] + 0 for a in self.area]
            else:
                return [self.world.current_place.char_pos(self.area[1])[i]
                        + 0 for i in range(2)]
        except Exception:
            return 0, 0

    def load_image(self):
        if self.imgfile is None: return
        self.surf = self.world.load_image(self.imgfile, True)
        self.size = self.surf.get_size()
        if self.area is None:
            self.area = ([self.pos[i] + self.areaadd[i]
                          for i in range(2)],
                         [self.pos[i] + self.size[i]
                          for i in range(2)])
        else:
            for i in range(2):
                if self.area[0][i] is None:
                    self.area[0][i] = self.pos[i]
                if self.area[1][i] is None:
                    self.area[1][i] = self.area[0][i] + self.size[i]
                else:
                    self.area[1][i] -= self.area[0][i]

    def event_check(self, event):
        if self.world.keys_locked:
            return
        if event.key == self.require_event[1] and self.close_to_touch:
            self.actions(True)

    def check_if_action_needed(self, pos, size):
        if self.surf is None: self.load_image()
        retval = True

        if self.rel == 0:
            npos = self.world.current_place.char_pos(pos)
        else:
            npos = pos

        touch = self.feet_in_obj_check(self.area[0], self.area[1],
                                       pos, size)
        self.close_to_touch = touch and self.require_event is not None
        if touch:
            retval = self.walkonact

        if self.require_event is None:
            rtouch = touch
        else:
            rtouch = False
        self.actions(rtouch)
        return retval

    def actions(self, touch):
        if touch and not self.in_area:
            if self.require_event is None:
                self.in_area = True
            self.do_action()
        elif not touch and self.in_area:
            if self.require_event is None:
                self.in_area = False
            self.do_unaction()

    def feet_in_obj_check(self, spos, spos2, cpos, csize):
        pos1 = [cpos[0] - csize[0] / 2, cpos[1] - csize[1] / 20]
        pos2 = [cpos[0] + csize[0] / 2, cpos[1]]
        xos1 = spos
        xos2 = spos2

        return pos1[0] < xos2[0] and pos2[0] > xos1[0] and \
            pos1[1] < xos2[1] and pos2[1] > xos1[1]

    def do_action(self):
        if self.action is not None:
            self.action[0](*self.action[1:])

    def do_unaction(self):
        if self.unaction is not None:
            self.unaction[0](*self.unaction[1:])

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, surf=None):
        if not self.visible: return
        if self.surf is None: self.load_image()
        if self.surf is None: return
        if surf is None:
            surf = self.world

        surf.blit(self.surf, self.pos)

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

##[ Name        ]## character
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the Character class, controlling how
                  # people and monsters alike move

from datetime import datetime
import os.path
import pygame
from pygame.locals import *

class Frame:
    def __init__(self, img):
        self.surf = img
        self.width = img.get_width()
        self.height = img.get_height()

class EmptyCharacter:
    def stop(self):
        pass

    def walk(self, direction):
        pass

class Character:
    def __init__(self, world, idname, datafiles, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default
        self.id = idname
        self.name = get('name', None)
        self.world = world
        self.data = datafiles
        self.frames = {}
        self.walking = False
        self.step = 0
        self.original_direction = get('direction', 'cb')
        self.direction = self.original_direction[:]
        self.position = get('position', world.get_center())
        self.duration = get('duration', 200) * 1000
        self.movement = get('movement', dict(
                cb=(0, 3),
                ct=(0, -3),
                lm=(-3, 0),
                rm=(3, 0),
                lb=(-2.12, 2.12),
                rt=(2.12, -2.12),
                lt=(-2.12, -2.12),
                rb=(2.12, 2.12)
        ))
        self.use_shadow = get('shadow', True)
        self.shadow_details = get('shadowdetails', {})
        self.default_direction = 'cb'
        self.default_position = (
            self.world.size[0] / 2,
            int(self.world.size[1] * 0.9))
        self.original_position = get('position', self.default_position[:])
        self.position = self.position[:]
        self.modified_position = self.position[:]
        self.visible = get('visible', False)

        self.create()
        if self.use_shadow:
            self.create_shadow()

    def get_bottom_area(self):
        return self.modified_position[0] + self.get_size(self.position)[0] / 2, self.modified_position[1]

    def convert_files_to_surfaces(self, *files):
        frames = []
        for f in files:
            img = self.world.load_image(f, True)
            frames.append(Frame(img))
        return frames

    def create(self):
        for x in 'lt', 'ct', 'rt', 'lm', 'rm', 'lb', 'cb', 'rb':
            if x in self.data[1]: # Files and directories
                files = self.data[1][x][1] # 1 = files
                files = [os.path.join(self.data[0], x, t) for t in files]
                self.frames[x] = \
                    self.convert_files_to_surfaces(*files)

        if len(self.frames) < 8:
            self.fill_out_remaining_directions()

        maxw = 0
        maxh = 0
        for x in self.frames.values():
            for y in x:
                if y.width > maxw:
                    maxw = y.width
                if y.height > maxh:
                    maxh = y.height
        self.maxsize = (maxw, maxh)

        try:
            self.head = \
                self.world.load_image(os.path.join(self.data[0],
                                                   'head.png'), True)
        except Exception:
            self.head = None

    def fill_out_remaining_directions(self):
        tries = {
            'lt': ('ct', 'lm', 'rt', 'lb', 'rm', 'cb', 'rb'),
            'rt': ('ct', 'rm', 'lt', 'rb', 'lm', 'cb', 'lb'),
            'ct': ('lt', 'rt', 'lm', 'rm', 'lb', 'rb', 'cb'),
            'cb': ('lb', 'rb', 'lm', 'rm', 'lt', 'rt', 'ct'),
            'lm': ('lt', 'lb', 'ct', 'cb', 'rt', 'rb', 'rm'),
            'rm': ('rt', 'rb', 'ct', 'cb', 'lt', 'lb', 'lm'),
            'lb': ('cb', 'lm', 'rb', 'lt', 'rm', 'ct', 'rt'),
            'rb': ('cb', 'rm', 'lb', 'rt', 'lm', 'ct', 'lt')
            }
        for x in 'lt', 'ct', 'rt', 'lm', 'rm', 'lb', 'cb', 'rb':
            if x not in self.frames:
                ok = False
                i = 0
                while not ok:
                    try:
                        self.frames[x] = self.frames[tries[x][i]]
                        ok = True
                        break
                    except Exception:
                        if i == 7:
                            break
                        i += 1
                if not ok:
                    self.frames[x] = None

    def create_shadow(self):
        charsurf = self.frames['cb'][0]
        size = (charsurf.width - charsurf.width / 15, charsurf.height / 15)
        ssize = [s * 3 for s in size]
        rect = pygame.Rect((0, 0), ssize)
        surf = pygame.Surface(ssize).convert_alpha()
        surf.fill(pygame.Color(0, 0, 0, 0))
        pygame.draw.ellipse(surf, pygame.Color(0, 0, 0, 200), rect)
        surf = pygame.transform.smoothscale(surf, size)

        self.shadow = surf
        self.shadow_size = surf.get_size()

    def get_size(self, pos, img=None):
        resize = self.world.current_place.char_size(pos)
        if img is None:
            img = self.get_frame()
        w = int(img.width * resize)
        h = int(img.height * resize)
        return w, h, resize

    def get_frame(self):
        if self.walking:
            return self.frames[self.direction][self.step]
        else:
            return self.frames[self.direction][0]

    def next_step(self):
        self.step = (self.step + 1) % len(self.frames[self.direction])

    def stop(self):
        self.walking = False

    def is_reverse(self, direction):
        a = self.direction
        b = direction
        return (a == 'cb' and b in ('ct', 'rt', 'lt')) \
            or (a == 'ct' and b in ('cb', 'rb', 'lb')) \
            or (a == 'lm' and b in ('rm', 'rt', 'rb')) \
            or (a == 'rm' and b in ('lm', 'lt', 'lb')) \
            or (a == 'lt' and b == 'rb') \
            or (a == 'rt' and b == 'lb') \
            or (a == 'lb' and b == 'rt') \
            or (a == 'rb' and b == 'lt')

    def walk(self, direction):
        w, h, resize = self.get_size(self.position)
        size = w, h
        maxsize = [s * resize for s in self.maxsize]
        mov = self.movement[direction]
        pos = self.position
        pos_ok = False
        scale = 1.0

        while not pos_ok:
            npos = [int(pos[i] + mov[i] * resize * scale *
                        self.world.size[i] / 100.0) for i in range(2)]
            mpos = self.world.current_place.char_pos(npos)
            pos_ok = self.world.current_place.pos_ok(mpos, maxsize)

            scale -= .1
            if scale < 0.4:
                break
        if pos_ok:
            conti = True
            for o in self.world.current_place.objects:
                t = o.check_if_action_needed(npos, maxsize)
                if not t: conti = False
            if conti:
                self.direction = direction
                self.position = npos
                self.modified_position = mpos
                self.walking = True
        else:
            self.stop()

    def set_position(self, pos):
        self.position = pos
        self.modified_position = self.world.current_place.char_pos(pos)

    def reset_position(self):
        self.position = self.original_position[:]
        self.modified_position = self.original_position[:]
        self.direction = self.original_direction
        w, h, resize = self.get_size(self.modified_position)
        for o in self.world.current_place.objects:
            o.check_if_action_needed(self.position, (w, h))

    def say(self, msg, **oargs):
        if self.name is not None:
            msg = self.name + ': ' + msg
        oargs = oargs.copy()
        oargs['head'] = self.head
        self.world.show_message(msg, **oargs)

    def ask(self, question, *answers, **oargs):
        if self.name is not None:
            question = self.name + ': ' + question
        oargs = oargs.copy()
        oargs['head'] = self.head
        self.world.show_question(question, *answers, **oargs)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def draw(self, surf=None):
        if not self.visible: return False
        img = self.get_frame()
        pos = self.modified_position

        w, h, r = self.get_size(pos, img)
        img = pygame.transform.smoothscale(img.surf, (w, h))
        if surf is None:
            surf = self.world
        if self.use_shadow:
            ssize = [int(s * r) for s in self.shadow_size]
            shad = pygame.transform.smoothscale(
                self.shadow, ssize)
            shad_pos = (pos[0] - w / 2 + (w - ssize[0]) / 2, pos[1] - h / 15)
            surf.blit(shad, shad_pos)
        surf.blit(img, (pos[0] - w / 2, pos[1] - h))

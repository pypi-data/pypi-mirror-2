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

##[ Name        ]## msgbox
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Makes it possible to display messages and speech
                  # throughout the game

import pygame
from pygame.locals import *
import os.path

HEADSIZE = 75

class MessageBox:
    def __init__(self, world, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default

        self.world = world
        self.path = get('path', None)
        self.font = get('font', None)
        self.default_pos = get('pos', None)
        self.headtextrel = get('headtextrel', 0)
        # 0: | HEAD | TEXT... |
        # 1: | TEXT... | HEAD |
        # 2: |   HEAD  |
        #    | TEXT... |
        # 3: | TEXT... |
        #    |   HEAD  |
        self.size = get('size', (620, 120))
        self.posize = get('posize', (10, 10))
        self.visible = False

        self.msgcontainers = []

        if self.path is not None:
            try:
                self.bgimg = \
                    self.world.load_image(os.path.normpath(
                        os.path.join(self.path, 'bgimg.png')), True)
                self.size = self.bgimg.get_size()
            except Exception:
                self.bgimg = None
            try:
                self.poimg = \
                    self.world.load_image(os.path.normpath(
                        os.path.join(self.path, 'pointer.png')), True)
                self.posize = self.poimg.get_size()
            except Exception:
                self.poimg = None

            if self.default_pos is None:
                self.default_pos = ((self.world.size[0] - self.size[0]) / 2, 10)
            if self.headtextrel == 0:
                self.headpos = (10, (self.size[1] - HEADSIZE) / 2)
                self.textpos = (20 + HEADSIZE, 10)
                self.textsize = (self.size[0] - 35 - HEADSIZE,
                                 self.size[1] - 20)
            elif self.headtextrel == 1:
                self.textpos = (10, 10)
                self.textsize = (self.size[0] - 35 - HEADSIZE,
                                 self.size[1] - 20)
                self.headpos = (self.textpos[0] + self.textsize[0] +
                                10, (self.size[1] - HEADSIZE) / 2)
            elif self.headtextrel == 2:
                self.headpos = ((self.size[0] - HEADSIZE) / 2, 10)
                self.textpos = (10, 20 + HEADSIZE)
                self.textsize = (self.size[0] - 20,
                                 self.size[1] - 35 - HEADSIZE)
            elif self.headtextrel == 3:
                self.textpos = (10, 10)
                self.textsize = (self.size[0] - 20,
                                 self.size[1] - 35 - HEADSIZE)
                self.headpos = ((self.size[0] - HEADSIZE) / 2,
                                self.textpos[1] + self.textsize[1] + 10)
        else:
            self.bgimg = None
            self.poimg = None
            if self.default_pos is None:
                self.default_pos = (10, 10)
            self.headpos = (20, 20)
            self.textpos = (20 + HEADSIZE, 20)

    def draw(self):
        for x in self.msgcontainers:
            x.draw()

class MessageContainer:
    def __init__(self, msgbox, pos=None):
        self.msgbox = msgbox
        self.world = self.msgbox.world
        self.head = None
        self.text = None

        self.visible = False

    # Messages
    def show_message(self, text=None, **oargs):
        self.head = oargs.get('head') or None
        self.pos = oargs.get('pos') or self.msgbox.default_pos
        self.temp_endaction = oargs.get('endaction') or None
        if text is not None:
            self.text = text
            self.textsurfs = self.msgbox.font.write(
                text, split=self.msgbox.textsize)
            self.surfnum = 0
            self.world.lock_keys()
            self.world.link_event(KEYDOWN,
                                  self.show_more_message_text)
        if self.head or self.text:
            self.msgbox.msgcontainers.append(self)
            self.visible = True

    def show_more_message_text(self, event):
        if event.key in (K_RETURN, K_SPACE, K_KP_ENTER):
            self.surfnum += 1
        if self.surfnum == len(self.textsurfs):
            self.hide()
            self.world.unlink_event(KEYDOWN,
                                    self.show_more_message_text)
            self.world.unlock_keys()
            if self.temp_endaction is not None:
                self.temp_endaction[0](*self.temp_endaction[1:])
            del self.temp_endaction

    # Questions with answers
    def show_question(self, question=None, *answers, **oargs):
        self.head = oargs.get('head') or None
        posize = oargs.get('posize') or None
        self.pointer = oargs.get('pointer') or None
        self.pos = oargs.get('pos') or self.msgbox.default_pos
        self.temp_endaction = oargs.get('endaction') or None
        self.answers = answers
        if question is not None:
            self.text = question
            self.textsurfs, self.pposs, self.surf_of_ans = self.msgbox.font.write(
                self.text, split=self.msgbox.textsize,
                indent_size=posize, indent_text=[a[0] for a in self.answers])
            self.surfnum = 0
            self.ansnum = 0
            self.anslen = len(self.pposs)
            self.surfnumstart, self.surfnumend = \
                self.surf_of_ans[self.ansnum]
            self.surfnum = self.surfnumstart
            self.world.lock_keys()
            self.world.link_event(KEYDOWN,
                                  self.show_more_question_text)
        if self.head or self.text:
            self.msgbox.msgcontainers.append(self)
            self.visible = True

    def show_more_question_text(self, event):
        if event.key in (K_DOWN,):
            if self.surfnum < self.surfnumend:
                self.surfnum += 1
            elif self.ansnum < self.anslen - 1:
                self.ansnum += 1
                self.surfnumstart, self.surfnumend = \
                    self.surf_of_ans[self.ansnum]
                self.surfnum = self.surfnumstart
        elif event.key in (K_UP,):
            if self.surfnum > self.surfnumstart:
                self.surfnum -= 1
            elif self.ansnum > 0:
                self.ansnum -= 1
                self.surfnumstart, self.surfnumend = \
                    self.surf_of_ans[self.ansnum]
                self.surfnum = self.surfnumend

        if event.key in (K_RETURN, K_SPACE, K_KP_ENTER):
            self.hide()
            self.world.unlink_event(KEYDOWN,
                                    self.show_more_question_text)
            self.world.unlock_keys()
            if self.temp_endaction is not None:
                self.temp_endaction[0](*self.temp_endaction[1:])
            del self.temp_endaction
            a = self.answers[self.ansnum]
            a[1](*a[2:])

    def hide(self):
        self.msgbox.msgcontainers.remove(self)
        self.visible = False

    def draw(self):
        if not self.visible: return

        if self.msgbox.bgimg is not None:
            self.world.blit(self.msgbox.bgimg, self.pos)

        if self.head is not None:
            self.world.blit(self.head,
                            [self.msgbox.headpos[i] +
                             self.pos[i]
                             for i in range(2)])

        if self.text is not None:
            surf = self.textsurfs[self.surfnum]
            text_x = self.msgbox.textpos[0] + self.pos[0]
            text_y = self.pos[1] + self.msgbox.textpos[1] + \
                (self.msgbox.size[1] - surf.get_size()[1]) / 2
            pos = (text_x, text_y)
            self.world.blit(surf, pos)

            try:
                if self.surfnum == self.surfnumstart:
                    self.world.blit(
                        self.pointer, (text_x, text_y +
                                       self.pposs[self.ansnum][1]))
            except AttributeError:
                pass


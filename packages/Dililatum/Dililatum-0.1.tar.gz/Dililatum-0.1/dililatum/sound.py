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

##[ Name        ]## sound
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the Sound class, which makes it possible
                  # to play back sound

import pygame
from pygame.locals import *

class Sound:
    def __init__(self, world, path):
        self.world = world
        self.path = path
        self.is_playing = False
        if self.world.sys.etc.loadwait:
            self.load_sound()
        else:
            self.snd = None

    def load_sound(self):
        self.snd = pygame.mixer.Sound(self.path)

    def play(self):
        if self.world.sys.etc.mute: return
        self.world.sys.emit_signal('beforesoundplay', self, self.snd)
        if self.snd is None:
            self.load_sound()
        self.snd.play(-1) # Looping indefinitely
        self.is_playing = True
        self.world.sys.emit_signal('aftersoundplay', self, self.snd)

    def stop(self):
        self.world.sys.emit_signal('beforesoundstop', self, self.snd)
        try:
            self.snd.stop()
        except AttributeError:
            pass
        self.is_playing = False
        self.world.sys.emit_signal('aftersoundstop', self, self.snd)

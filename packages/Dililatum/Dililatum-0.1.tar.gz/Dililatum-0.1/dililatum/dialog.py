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

##[ Name        ]## dialog
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the Dialog class whose purpose is to
                  # contain text and menus and to be drawn onto the
                  # screen

import pygame
from pygame.locals import *

class Dialog:
    def __init__(self, world, data=None):
        self.world = world

        self.surf = None
        if data is not None:
            self.use_data(data)

    def use_data(self, data):
        pass

    def draw(self, surf=None):
        if self.surf is None: return
        if surf is None:
            surf = self.world.screen
        surf.blit(self.surf, (0, 0))

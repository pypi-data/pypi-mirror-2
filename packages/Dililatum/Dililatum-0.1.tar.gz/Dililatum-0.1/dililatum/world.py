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

##[ Name        ]## world
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Contains the World class, controlling display
                  # output as well as key detection

from datetime import datetime
import os.path
import pygame
from pygame.locals import *
from dililatum.character import Character, EmptyCharacter
from dililatum.object import Object
from dililatum.place import Place
from dililatum.font import Font
from dililatum.sound import Sound
from dililatum.msgbox import MessageBox, MessageContainer
from dililatum.statusprinter import StatusPrinter
from dililatum.various import thread

microseconds = lambda tdelta: tdelta.microseconds
class TimeCounter:
    def __init__(self, obj, func):
        self.obj = obj
        self.func = func
        self.start = self.reset

    def reset(self):
        self.time = datetime.now()

    def think(self):
        if microseconds(datetime.now() - self.time) > \
                self.obj.duration:
            self.func()
            self.reset()

class Duration:
    def __init__(self, dur):
        self.duration = dur * 1000

class World:
    default_character_moving_keys = dict(
        cb=[K_DOWN],
        ct=[K_UP],
        lm=[K_LEFT],
        rm=[K_RIGHT],
        lb=[K_LEFT, K_DOWN],
        rt=[K_RIGHT, K_UP],
        lt=[K_LEFT, K_UP],
        rb=[K_RIGHT, K_DOWN]
    )

    def __init__(self, stm, size, **oargs):
        def get(key, default):
            try: return oargs[key]
            except KeyError: return default
        self.sys = stm
        self.size = size
        self.real_size = tuple(self.size[:])
        self.loaded_images = {}
        self.objects = []
        self.sounds = []
        self.characters = []
        self.leading_character = EmptyCharacter()
        self.leading_character_direction = None
        self.character_moving_keys = get('charkeys',
                                         self.default_character_moving_keys)
        self.walking_speed = get('walkspeed', Duration(100))
        self.msgboxes = []
        self.default_msgbox = None
        self.counters = []
        self.places = []
        self.current_place = None
        self.running = False
        self.quitting = False
        self.status = StatusPrinter('WORLD', self.sys.etc, 'cyan', 'blue')
        self.link_event = self.sys.gameactions.add
        self.unlink_event = self.sys.gameactions.remove
        self.keys_down = []
        self.screen_offset = [0, 0]
        self.screen_bars = [None, None]
        self.keys_locked = False
        self.event = {}
        self.sys.emit_signal('afterworldinit', self)

    def start(self):
        self.sys.emit_signal('beforeworldstart', self)
        self.status('Starting up...')

        self.link_event(QUIT, self.quit)
        self.link_event(KEYDOWN, self.key_builtin)
        self.link_event(KEYDOWN, self.lead_walk)
        self.link_event(KEYUP, self.lead_walk)

        self.counters.append(TimeCounter(self.walking_speed, self.check_lead_walk))

        self.pygame_init()
        self.create_screen()
        self.fill_background((0, 0, 0))
        self.set_caption(self.sys.game.name)

        self.innerclock = pygame.time.Clock()
        self.sys.emit_signal('afterworldstart', self)

    def pygame_init(self):
        pygame.display.init()
        pygame.font.init()
        pygame.mixer.pre_init(44100) # Sound files must be resampled
                                     # to 44.1 kHz
        pygame.mixer.init()

    def load_image(self, path, alpha=False):
        p = os.path.abspath(path)
        if p not in self.loaded_images.values():
            img = pygame.image.load(p)
            if alpha:
                img = img.convert_alpha()
            else:
                img = img.convert()
            self.loaded_images[p] = img
        else:
            img = self.loaded_images[p]
        return img

    def create_screen(self):
        self.screen_bars = [None, None]
        etc = self.sys.etc
        if etc.fullscreen:
            flags = FULLSCREEN
            if etc.hwaccel:
                flags = flags | HWSURFACE
            if etc.doublebuf:
                flags = flags | DOUBLEBUF
            self.screen = pygame.display.set_mode(self.size, flags)
        elif etc.fakefullscreen or etc.size is not None:
            barsize = None
            if etc.fakefullscreen or (etc.size is not None and etc.size[0] is None and etc.size[1] is None):
                try:
                    info = pygame.display.Info()
                    size = info.current_w, info.current_h
                    if size[0] == -1: # in this case, size[1] will also be -1
                        self.sys.error('your SDL is too old for width and height detection', False)
                except Exception:
                    self.sys.error('your PyGame is too old for width and height detection', False)
            else:
                size = list(etc.size)
            if size[0] is None:
                self.sys.etc.zoom = size[1] / float(self.size[1])
                size[0] = int(self.size[0] * etc.zoom)
            elif size[1] is None:
                self.sys.etc.zoom = size[0] / float(self.size[0])
                size[1] = int(self.size[1] * etc.zoom)
            else:
                scales = [size[i] / float(self.size[i]) for i in range(2)]
                if scales[0] < scales[1]: a = 0; b = 1
                else:                     a = 1; b = 0

                self.sys.etc.zoom = scales[a]
                self.screen_offset[b] = int((size[b] - self.size[b] * etc.zoom) / 2)
                barsize = [0, 0]
                barsize[a] = size[a]
                barsize[b] = self.screen_offset[b]
            self.real_size = size
            self.status('Modified size of game is: %dx%d' % tuple(self.real_size))
            flags = None
            if not etc.border or etc.fakefullscreen:
                flags = NOFRAME
            if etc.doublebuf:
                if flags is not None:
                    flags = flags | DOUBLEBUF
                else:
                    flags = DOUBLEBUF
            try:
                self.screen = pygame.display.set_mode(self.real_size, flags)
            except pygame.error:
                if not etc.border or etc.fakefullscreen:
                    flags = NOFRAME
                else:
                    flags = 0
                self.screen = pygame.display.set_mode(self.real_size, flags)
            if barsize is not None:
                self.screen_bars[b] = pygame.Surface(barsize).convert()
        else:
            if etc.zoom != 1:
                self.real_size = [int(x * etc.zoom) for x in self.size]
                self.status('Scaled size of game is: %dx%d' % tuple(self.real_size))
            flags = None
            if not etc.border or etc.fakefullscreen:
                flags = NOFRAME
            if etc.doublebuf:
                if flags is not None:
                    flags = flags | DOUBLEBUF
                else:
                    flags = DOUBLEBUF
            try:
                self.screen = pygame.display.set_mode(self.real_size, flags)
            except pygame.error:
                if not etc.border or etc.fakefullscreen:
                    flags = NOFRAME
                else:
                    flags = 0
                self.screen = pygame.display.set_mode(self.real_size, flags)

        self.bgsurface = pygame.Surface(self.real_size).convert()

    def fill_background(self, color):
        self.bgsurface.fill(color)
        for x in self.screen_bars:
            if x is not None:
                x.fill(color)

    def set_caption(self, caption):
        pygame.display.set_caption(caption)

    def set_icon(self, surf):
        pygame.display.set_icon(surf)

    def load_icon(self, path):
        self.set_icon(self.load_image(path, True))

    def blit(self, surf, pos=(0, 0), area=None):
        if surf is None: return
        surf = pygame.transform.smoothscale(
            surf, [int(x * self.sys.etc.zoom)
                   for x in surf.get_size()])
        if area is not None:
            area.width *= self.sys.etc.zoom
            area.height *= self.sys.etc.zoom
        self.screen.blit(surf, [self.screen_offset[i] + pos[i] *
                                self.sys.etc.zoom for i in range(2)], area)

    def flip(self):
        pygame.display.flip()

    def lock_keys(self):
        self.keys_locked = True

    def unlock_keys(self):
        self.keys_locked = False

    def create_font(self, **oargs):
        return Font(self, **oargs)

    def create_character(self, idname, datafiles, **oargs):
        self.sys.emit_signal('beforecharactercreate', self, idname)
        char = Character(self, idname, datafiles, **oargs)
        self.sys.emit_signal('aftercharactercreate', char)
        return char

    def add_character(self, char):
        self.sys.emit_signal('beforecharacteradd', char)
        self.characters.append(char)
        counter = TimeCounter(char, char.next_step)
        self.counters.append(counter)
        if self.running:
            counter.start()
        self.sys.emit_signal('aftercharacteradd', char)

    def create_msgbox(self, **oargs):
        self.sys.emit_signal('beforemsgboxcreate', self, oargs)
        msgbox = MessageBox(self, **oargs)
        self.sys.emit_signal('aftermsgboxcreate', msgbox)
        return msgbox

    def add_msgbox(self, msgbox):
        self.sys.emit_signal('beforemsgboxadd', msgbox)
        self.msgboxes.append(msgbox)
        self.sys.emit_signal('aftermsgboxadd', msgbox)

    def show_message(self, msg, **oargs):
        msgbox = oargs.get('msgbox') or self.default_msgbox
        MessageContainer(msgbox).show_message(msg, **oargs)

    def show_question(self, *args, **oargs):
        msgbox = oargs.get('msgbox') or self.default_msgbox
        oargs['pointer'] = msgbox.poimg
        oargs['posize'] = msgbox.posize
        MessageContainer(msgbox).show_question(*args, **oargs)

    def set_leading_character(self, char):
        self.leading_character = char

    def check_lead_walk(self):
        if self.leading_character_direction is None:
            self.leading_character.stop()
        else:
            self.leading_character.walk(self.leading_character_direction)

    def lead_walk(self, event):
        if event.type == KEYDOWN:
            self.keys_down.append(event.key)
        elif event.type == KEYUP:
            try:
                self.keys_down.remove(event.key)
            except ValueError:
                pass

        if not self.keys_locked:
            self.leading_character_direction = \
                self.get_value_of_key_dict(self.character_moving_keys)
        else:
            self.leading_character_direction = None

    def get_value_of_key_dict(self, keydict):
        result = None
        result_key_numbers = None
        result_points = None
        for value, keys in keydict.items():
            p = []
            tp = 0
            tn = 0
            ok = True
            for k in keys:
                i = 0
                ok = False
                for d in self.keys_down:
                    if k == d:
                        tp += i
                        tn += 1
                        ok = True
                        break
                    i += 1
                if not ok:
                    break
            if ok:
                if result_key_numbers is not None:
                    tngo = tn > result_key_numbers
                    tn2go = tn == result_key_numbers
                else:
                    tngo = True
                if not tngo:
                    if result_points is not None:
                        tpgo = tp < result_points
                    else:
                        tpgo = True

                if tngo or (tn2go and tpgo):
                    result = value
                    result_points = tp
                    result_key_numbers = tn

        return result

    def remove_character(self, char):
        if 'id' not in dir(char):
            char = None
            for t in self.characters:
                if t.id == char:
                    char = t
            if char is None:
                return False

        self.sys.emit_signal('beforecharacterremove', char)
        self.characters.remove(char)
        self.remove_counter(char)
        self.sys.emit_signal('aftercharacterremove', char)
        return True

    def remove_counter(self, obj):
        try:
            self.counters.remove(obj)
            return True
        except Exception:
            for t in self.counters:
                if t.obj == obj:
                    self.counters.remove(t)
                    return True
            return False

    def create_sound(self, path):
        self.sys.emit_signal('beforesoundcreate', self, path)
        snd = Sound(self, path)
        self.sys.emit_signal('aftersoundcreate', self, snd)
        return snd

    def add_sound(self, snd):
        self.sys.emit_signal('beforesoundadd', self, snd)
        self.sounds.append(snd)
        self.sys.emit_signal('aftersoundadd', self, snd)

    def create_object(self, *args, **oargs):
        self.sys.emit_signal('beforeobjectcreate', self)
        args = list(args)
        args.insert(0, self)
        obj = Object(*args, **oargs)
        self.sys.emit_signal('afterobjectcreate', obj)
        return obj

    def create_place(self, *args, **oargs):
        self.sys.emit_signal('beforeplacecreate', self)
        args = list(args)
        args.insert(0, self)
        place = Place(*args, **oargs)
        self.sys.emit_signal('afterplacecreate', place)
        return place

    def add_place(self, place):
        self.sys.emit_signal('beforeplaceadd', place)
        self.places.append(place)
        self.sys.emit_signal('afterplaceadd', place)

    def set_place(self, place, npos=None, direction=None):
        try:
            curbgsnds = self.current_place.bgsounds
        except Exception:
            curbgsnds = []
        if 'draw' in dir(place):
            self.current_place = place
        else:
            try:
                self.current_place = self.places[place]
            except IndexError:
                pass
        if self.leading_character is None:
            return

        if npos is None:
            npos = self.leading_character.default_position
        npos = npos[:]
        if npos[0] < 0:
            npos[0] = int(
                self.size[0] + npos[0] -
                place.char_size(npos) *
                self.leading_character.maxsize[0]
            )
        self.leading_character.stop()

        if direction is not None:
            if direction[0] == 'l':
                npos[0] = int(npos[0] - (place.char_size(npos) / 2) *
                              self.leading_character.maxsize[0])
            elif direction[0] == 'r':
                npos[0] = int(npos[0] + (place.char_size(npos) / 2) *
                              self.leading_character.maxsize[0])
            self.leading_character.original_direction = direction
            self.leading_character.direction = direction
            self.leading_character_direction = direction
        self.leading_character.original_position = npos
        self.leading_character.position = npos[:]
        self.leading_character.modified_position = npos[:]

        newbgsnds = self.current_place.bgsounds
        for x in curbgsnds:
            if x not in newbgsnds:
                x.stop()
        for x in newbgsnds:
            if not x.is_playing:
                thread(x.play)

    def get_center(self):
        return [x / 2 for x in self.size]

    def set_default_msgbox(self, msgbox):
        self.default_msgbox = msgbox

    def draw(self):
        self.screen.blit(self.bgsurface, (0, 0))
        if self.current_place is None:
            return
        self.current_place.draw()

        objs = self.characters[:]
        objs.extend(self.current_place.objects)
        objs.extend(self.objects)
        objs.sort(key=lambda o: o.get_bottom_area()[1])
        for x in objs:
            if x.visible:
                x.draw()

        for x in self.msgboxes:
            x.draw()

        if self.screen_bars[0] is not None:
            self.screen.blit(self.screen_bars[0], (0, 0))
            self.screen.blit(self.screen_bars[0],
                             (self.real_size[0] -
                              self.screen_bars[0].get_size()[0], 0))
        if self.screen_bars[1] is not None:
            self.screen.blit(self.screen_bars[1], (0, 0))
            self.screen.blit(self.screen_bars[1],
                             (0, self.real_size[1] -
                              self.screen_bars[1].get_size()[1]))

        pygame.display.flip()

    def run(self):
        self.sys.emit_signal('beforeworldrun', self)
        self.status('Running...')
        self.running = True

        for c in self.counters:
            c.start()

        while not self.quitting:
            self.innerclock.tick(30)
            self.sys.emit_signal('beforegameloop', self)

            for event in pygame.event.get():
                self.event[event.type] = event
                self.sys.emit_event(event.type, event)

            for c in self.counters:
                c.think()

            self.draw()
            self.sys.emit_signal('aftergameloop', self)

        self.sys.emit_signal('afterworldrun', self)

    def quit(self, event):
        self.quitting = True

    def key_builtin(self, event):
        if event.key == K_SCROLLOCK:
            self.leading_character.reset_position()
        if event.key == K_ESCAPE:
            self.quit(event)

    def end(self):
        self.sys.emit_signal('beforeworldend', self)
        self.status('Stopping...')
        self.sys.emit_signal('afterworldend', self)

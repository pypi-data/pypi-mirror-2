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

##[ Name        ]## placelinker
##[ Maintainer  ]## Niels Serup <ns@metanohi.org>
##[ Description ]## Makes it possible to visually link places together

import sys
import os.path
import math
import random
import pygame
from pygame.locals import *
try:
    import cPickle as pickle
except ImportError:
    import pickle


placelinker_help = """\
To use this tool, remember the following:

LMB down => move screen
RMB down => move current background
MMB down => center screen to current position
Mouse scrolling and PageDown/PageUp => zoom in/out

Special keys:
s => stop any current special key action
r => create a rectangle on a background
    how: press r, click on start pos, click on end pos, type name,
         press enter, return or escape, type target direction, press
         enter, return or escape
p => create a point on a background
    how: press p, click on a position
l => create a link (points can have more than one link, but rects cannot)
    how: press l, click on a rectangle or a point, do that again
n => name a rectangle
    how: press n, click on a rectangle, type name, press enter, return
         or escape
d => set the target direction
    how: press d, click on a rectangle, type target direction, press
         enter, return or escape
m => move an object on a background
    how: press m, mouse down on an object, move object, mouse up
a => adjust the size of a rectangle
    how: press a, click on a rectangle, click on the new start pos,
         click on the new end pos
shift+a => adjust the start pos of a rectangle
    how: press a, click on a rectangle, click on the new start pos,
ctrl+a => adjust the end pos of a rectangle
    how: press a, click on a rectangle, click on the new end pos
delete: delete an object or a background
    how: press delete, click on what you want to throw away
e: delete link associated with an object
    how: press e, click on an object\
"""


class LinkedPlace:
    def __init__(self, parent, surf, pos, path):
        self.parent = parent
        self.surf = surf
        self.size = surf.get_size()
        self.pos = pos
        self.path = path

        self.current = False

        self.rects = []
        self.points = []

        self.highlighted_obj = None

        self.borders = Borders(self)

        surf = self.parent.large_font.render(os.path.basename(path),
                                             True, (0, 0, 255))
        self.surf.blit(surf, (0, 0))

    def check_hovered(self, pos):
        ipos = [pos[i] - self.pos[i] for i in range(2)]
        h = ipos[0] >= 0 and ipos[0] < self.size[0] and \
            ipos[1] >= 0 and ipos[1] < self.size[1]

        self.current = h
        self.check_internal_hovered(ipos)
        return h

    def check_internal_hovered(self, rpos):
        h = False
        self.highlighted_obj = None
        for p in self.points:
            if rpos[0] >= p.rpos[0] and rpos[1] >= p.rpos[1] and \
                    rpos[0] < p.rpos[0] + p.size[0] and \
                    rpos[1] < p.rpos[1] + p.size[1]:
                p.highlight()
                self.highlighted_obj = p
                h = True
            elif p.highlighted:
                p.unhighlight()

        for r in self.rects:
            if rpos[0] >= r.rpos[0] and rpos[1] >= r.rpos[1] and \
                    rpos[0] < r.rpos[0] + r.size[0] and \
                    rpos[1] < r.rpos[1] + r.size[1]:
                if not h:
                    r.highlight()
                    self.highlighted_obj = r
            elif r.highlighted:
                r.unhighlight()

    def create_rect(self, rpos, size, name='', target=''):
        rect = Rect(self, rpos, size, name, target)
        self.rects.append(rect)
        return rect

    def create_point(self, rpos):
        point = Point(self, rpos)
        self.points.append(point)
        return point

    def remove_object(self, o):
        if o is not None:
            if o in self.points:
                self.points.remove(o)
            elif o in self.rects:
                self.rects.remove(o)
            else:
                return
        for l in o.linked_with:
            self.parent.links.remove(l)
            for w in l.objs:
                try:
                    w.linked_with.remove(l)
                except ValueError:
                    pass

    def delete_highlighted_object(self):
        o = self.highlighted_obj
        self.remove_object(o)
        self.highlighted_obj = None

    def delete_self(self):
        for x in self.rects:
            self.remove_object(x)
        for x in self.points:
            self.remove_object(x)

        self.parent.places.remove(self)
        self.highlighted_obj = None

    def blit(self, surf):
        surf.pos = [surf.rpos[i] + self.pos[i] for i in range(2)]
        self.parent.blit(surf)

    def draw(self):
        if self.current:
            self.borders.draw()
        self.parent.blit(self)
        for r in self.rects:
            r.draw()
        for p in self.points:
            p.draw()


class LinkedPlaceObject:
    var='obj'

    def __init__(self, place, *args):
        self.place = place
        self.highlighted = False
        self.linked_with = []
        self.init(*args)
        self.unmark()
        self.update()

    def init(self, *args):
        self.normal_color = pygame.Color(0, 0, 0)
        self.highlight_color = pygame.Color(255, 255, 255)

    def highlight(self):
        self.highlighted = True
        self.mark()
        self.update()

    def unhighlight(self):
        self.highlighted = False
        self.unmark()
        self.update()

    def mark(self):
        pass

    def unmark(self):
        pass

    def update(self):
        pass

    def draw(self):
        self.place.blit(self)

class Borders(LinkedPlaceObject):
    def init(self):
        self.rpos = [-s / 25 for s in self.place.size]
        self.size = [int(s + s / 12.5) for s in self.place.size]
        self.surf = pygame.Surface(self.size)
        self.surf.fill((0, 0, 0))

class Text:
    def __init__(self, rect, text, where, font, color):
        self.rect = rect
        self.text = text
        self.where = where
        self.font = font
        self.fgcolor = color

    def draw(self):
        if self.rect.name == '':
            return
        surf = self.font.render(self.text(), True, self.fgcolor)
        size = surf.get_size()
        ratio = 1
        maxsize = [s * 0.9 for s in self.rect.size]
        if size[0] > maxsize[0]:
            ratio = maxsize[0] / float(size[0])
        if size[1] > maxsize[1]:
            nratio = maxsize[1] / float(size[1])
            if nratio < ratio:
                ratio = nratio

        if ratio != 1:
            size = [int(s * ratio) for s in size]
            surf = pygame.transform.smoothscale(surf, size)
        if self.where[0] == 1 and self.where[1] == 1:
            pos = [(self.rect.size[i] - size[i]) / 2 for i in range(2)]
        elif self.where[0] == 2 and self.where[1] == 2:
            pos = [(self.rect.size[i] - size[i]) for i in range(2)]
        self.rect.surf.blit(surf, pos)

class Rect(LinkedPlaceObject):
    var = 'rect'
    def init(self, rpos, size, name='', targetdir=''):
        self.rpos = rpos
        self.size = size
        self.name = name
        self.targetdir = targetdir

        self.normal_color = pygame.Color(18, 13, 228, 70)
        self.highlight_color = pygame.Color(118, 213, 128, 90)
        self.text = Text(self, lambda: self.name, (1, 1),
                         self.place.parent.large_font, self.place.parent.large_font_color)
        self.targettext = Text(self, lambda: self.targetdir, (2, 2),
                               self.place.parent.small_font, self.place.parent.small_font_color)

    def recreate(self):
        self.surf = pygame.Surface(self.size).convert_alpha()

    def mark(self):
        self.recreate()
        self.surf.fill(self.highlight_color)

    def unmark(self):
        self.recreate()
        self.surf.fill(self.normal_color)

    def update(self):
        if self.highlighted:
            self.mark()
        else:
            self.unmark()
        self.text.draw()
        self.targettext.draw()

class Point(LinkedPlaceObject):
    var = 'point'
    def init(self, rrpos):
        self.rrpos = rrpos
        self.size = (20, 20)
        self.rpos = [self.rrpos[i] - self.size[i] / 2 for i in range(2)]

        self.surf = pygame.Surface(self.size)
        self.normal_color = pygame.Color(0, 0, 0)
        self.highlight_color = pygame.Color(255, 255, 255)

    def mark(self):
        self.surf.fill(self.highlight_color)

    def unmark(self):
        self.surf.fill(self.normal_color)

class Link:
    def __init__(self, parent, *objs):
        self.parent = parent
        self.objs = objs
        for o in self.objs:
            o.linked_with.append(self)

    def draw(self):
        self.parent.draw_line(*[[o.pos[i] + o.size[i] / 2
                                 for i in range(2)]
                                for o in self.objs])

class PlaceLinker:
    def __init__(self, size=None):
        self.size = size
        self.zoom = 1.0
        self.offset = [0, 0]
        self.places = []
        self.links = []

        self.bgcolor = pygame.Color(255, 255, 255)
        self.current_hovered_place = None
        self.moving = False
        self.moving_a_place = False
        self.moving_an_object = False

        self.creating_rect = False
        self.adjusting_rect = False
        self.creating_point = False
        self.creating_link = False
        self.naming_rect = False
        self.setting_target_dir = False
        self.deleting_obj = False
        self.deleting_link = False

        self.special_key_func = None

    def get_screen_size(self):
        try:
            info = pygame.display.Info()
            size = info.current_w, info.current_h
            if size[0] == -1: # in this case, size[1] will also be -1
                sys.stderr.write('your SDL is too old for width \
and height detection\n')
                sys.exit(1)
        except Exception:
            sys.stderr.write('your PyGame is too old for width \
and height detection\n')
            sys.exit(1)
        self.size = size

    def start(self):
        pygame.display.init()
        pygame.font.init()

        if self.size is None:
            self.get_screen_size()

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('placelinker')
        self.bgsurface = pygame.Surface(self.size)
        self.bgsurface.fill(self.bgcolor)

        match = pygame.font.match_font('freesans,dejavusans', True)
        self.large_font = pygame.font.Font(match, 30)
        self.large_font_color = pygame.Color(233, 30, 45)
        self.small_font = pygame.font.Font(match, 20)
        self.small_font_color = pygame.Color(30, 233, 45)

    def blit(self, obj):
        size = obj.size
        surf = obj.surf
        pos = obj.pos

        size = [int(s * self.zoom) for s in size]
        pos = [int((pos[i] + self.offset[i]) * self.zoom) for i in
               range(2)]

        if pos[0] + size[0] >= 0 and \
                pos[0] <= self.size[0] and \
                pos[1] + size[1] >=0 and \
                pos[1] <= self.size[1]:
            surf = pygame.transform.scale(surf, size)
            self.screen.blit(surf, pos)

    def draw_line(self, *p):
        p = [self.get_screen_pos(x) for x in p]
        pygame.draw.aaline(self.screen, (128, 55, 38), p[0], p[1])
        pygame.draw.aaline(self.screen, (128, 55, 38),
                           (p[0][0] - 1, p[0][1]),
                           (p[1][0] - 1, p[1][1]))
        pygame.draw.aaline(self.screen, (128, 55, 38),
                           (p[0][0] + 1, p[0][1]),
                           (p[1][0] + 1, p[1][1]))

    def new_place(self, surf, x, y, name):
        return LinkedPlace(self, surf, (x, y), name)

    def new(self, *images):
        num = int(math.ceil(math.sqrt(len(images))))
        x = 0
        y = 0
        xi = 0
        size = None
        for path in images:
            try:
                plc = self.new_place(pygame.image.load(path).convert(),
                                     x, y, path)
                self.places.append(plc)
                if size is None:
                    size = plc.size[:]
                xi = (xi + 1) % num
                if xi == 0:
                    x = 0
                    y += int(size[1] * 1.5)
                else:
                    x += int(size[0] * 1.5)
            except pygame.error, e:
                sys.stderr.write('failed loading %s, python said:\
 %s\n' % (path, str(e)))
        xmax = size[0] * num + (size[0] / 2) * (num - 1)
        ymax = size[1] * num + (size[1] / 2) * (num - 1)

        self.zoom = self.size[0] / float(xmax) * 0.9
        self.offset[0] = (self.size[0] / self.zoom - xmax) / 2
        self.offset[1] = (self.size[1] / self.zoom - ymax) / 2

        self.outfilename = 'linked-places.lnkdplcs'
        self.fileoverride = False

    def load(self, datapath, *images):
        data = pickle.load(open(datapath, 'rb'))
        self.offset = list(data['offset'])
        self.zoom = data['zoom']
        for x in data['places']:
            plcinf = x[0]
            rects = x[1]
            points = x[2]
            plc = self.new_place(
                pygame.image.load(plcinf[0]).convert(),
                plcinf[1][0], plcinf[1][1], plcinf[0])
            self.places.append(plc)

            for r in rects:
                nrect = plc.create_rect(*r)
            for p in points:
                plc.create_point(p)

        for objnums in data['links']:
            objs = []
            for x in objnums:
                obj = None
                plcrange = range(len(self.places))
                for i in plcrange:
                    if i != x[1]:
                        continue

                    if x[0] == 1:
                        search_in = self.places[i].rects
                    elif x[0] == 2:
                        search_in = self.places[i].points
                    for j in range(len(search_in)):
                        if j == x[2]:
                            obj = search_in[j]
                            break
                    if obj is not None:
                        break
                objs.append(obj)
            self.create_link(*objs)

        self.outfilename = datapath
        self.fileoverride = True

        if len(images) > 0:
            for x in images:
                self.add_place(x)

    def add_place(self, path):
        plc = self.new_place(pygame.image.load(path).convert(),
                             0, 0, path)
        size = plc.size
        pos1 = [0, 0]

        ok = False
        while not ok:
            pos2 = [pos1[i] + size[i] for i in range(2)]

            nok = True
            for x in self.places:
                xos1 = x.pos
                xos2 = [xos1[i] + x.size[i] for i in range(2)]
                tok = (pos2[0] < xos1[0] or pos1[0] > xos2[0]) and \
                    (pos2[1] < xos1[1] or pos1[1] > xos2[1])
                if not tok:
                    nok = False
                    break

            if nok:
                ok = True
            else:
                pos1 = [pos1[i] + random.randint(10, 30) * size[i] / 100.0
                        for i in range(2)]

        if ok:
            plc.pos = pos1
            self.places.append(plc)

    def save(self):
        for p in self.places:
            for r in p.rects:
                if 0 in r.size:
                    p.remove_object(r)

        ofn = self.outfilename
        if not self.fileoverride:
            while os.path.exists(ofn):
                ofn = '_' + ofn

        data = {}
        data['zoom'] = self.zoom
        data['offset'] = tuple(self.offset)

        dp = []
        for plc in self.places:
            place = (plc.path, plc.pos)
            rects = []
            points = []
            for r in plc.rects:
                rects.append((r.rpos, r.size, r.name, r.targetdir))
            for p in plc.points:
                points.append(p.rrpos)
            dp.append((place, tuple(rects), tuple(points)))
        data['places'] = tuple(dp)

        dl = []
        plcrange = range(len(self.places))
        for l in self.links:
            objs = []
            for o in l.objs:
                objnum = None
                for i in plcrange:
                    tp = self.places[i]
                    for j in range(len(tp.rects)):
                        if tp.rects[j] == o:
                            objnum = (1, i, j)
                            break
                    for j in range(len(tp.points)):
                        if tp.points[j] == o:
                            objnum = (2, i, j)
                            break
                    if objnum is not None:
                        break
                objs.append(objnum)
            dl.append(tuple(objs))
        data['links'] = tuple(dl)

        try:
            f = open(ofn, 'wb')
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
            f.close()
        except Exception, e:
            sys.stderr.write(e + '\n\n\n')
            sys.stdout.write(pickle.dumps(data))

    def get_true_pos(self, pos):
        return [pos[i] / self.zoom - self.offset[i] for i in range(2)]

    def get_screen_pos(self, pos):
        return [(pos[i] + self.offset[i]) * self.zoom for i in range(2)]

    def relative_zoom(self, pos, way):
        opos = self.get_true_pos(pos)

        if way is True:
            zoom = self.zoom * 1.1
            if zoom > 10.0: zoom = 10.0
            self.zoom = zoom
        else:
            zoom = self.zoom / 1.1
            if zoom < 0.01: zoom = 0.01
            self.zoom = zoom

        self.offset = [pos[i] / self.zoom - opos[i] for i in range(2)]

        for p in self.places:
            for r in p.rects:
                r.update()

        if self.moving_an_object:
            self.end_obj_moving()
        if self.moving:
            self.end_screen_moving()
        if self.moving_a_place:
            self.end_place_moving()

    def new_center(self, pos):
        opos = self.get_true_pos(pos)
        offset = [(self.size[i] / 2) / self.zoom - opos[i] for i in range(2)]
        self.offset = offset

    def get_hovered_place(self, pos):
        tpos = self.get_true_pos(pos)
        if self.current_hovered_place is None:
            for p in self.places:
                check = p.check_hovered(tpos)
                if check:
                    self.current_hovered_place = p
                    break
        else:
            c = self.current_hovered_place
            if not c.check_hovered(tpos):
                self.current_hovered_place = None

    def begin_screen_moving(self, pos):
        self.moving = True
        self.moving_pos = pos
        self.moving_offset = self.offset[:]

    def continue_screen_moving(self, pos):
        self.offset = \
            [int(self.moving_offset[i] +
                 (pos[i] - self.moving_pos[i])
                 / self.zoom) for i in range(2)]

    def end_screen_moving(self):
        self.moving = False

    def begin_place_moving(self, pos):
        self.moving_a_place = True
        tpos = self.get_true_pos(pos)
        self.moving_a_place_pos = pos
        self.temp_obj = self.current_hovered_place
        self.moving_a_place_offset = \
            [tpos[i] - tpos[i] +
             self.temp_obj.pos[i] for
             i in range(2)]
        self.places.remove(self.current_hovered_place)
        self.places.insert(-1, self.current_hovered_place)

    def continue_place_moving(self, pos):
        self.temp_obj.pos = \
            [self.moving_a_place_offset[i] +
             (pos[i] - self.moving_a_place_pos[i])
             / self.zoom for i in range(2)]

    def end_place_moving(self):
        self.moving_a_place = False

    def begin_creating_rect(self):
        self.creating_rect = 1
        self.bgsurface.fill((0, 0, 255))

    def continue_creating_rect(self, pos):
        if self.creating_rect == 1:
            rpos = [self.get_true_pos(pos)[i] -
                    self.current_hovered_place.pos[i]
                    for i in range(2)]
            self.temp_rect = rpos
            self.creating_rect = 2
        elif self.creating_rect == 2:
            arpos = self.temp_rect
            brpos = [self.get_true_pos(pos)[i] -
                     self.current_hovered_place.pos[i]
                     for i in range(2)]
            for i in range(2):
                if arpos[i] > brpos[i]:
                    t = brpos[i]
                    brpos[i] = arpos[i]
                    arpos[i] = t
            size = [brpos[i] - arpos[i] for i in range(2)]
            rect = self.current_hovered_place.create_rect(arpos, size)

            self.creating_rect = False
            self.bgsurface.fill(self.bgcolor)
            self.begin_naming_rect(rect, True)

    def begin_adjusting_rect(self, mod=0):
        self.adjusting_rect_mod = mod
        self.adjusting_rect = 1
        self.bgsurface.fill((0, 222, 222))

    def continue_adjusting_rect(self, pos):
        if self.adjusting_rect == 1:
            self.temp_obj = self.current_hovered_place.highlighted_obj
            if self.temp_obj is not None and self.temp_obj.var == 'rect':
                self.adjusting_rect = 2
        elif self.adjusting_rect == 2:
            rpos = [self.get_true_pos(pos)[i] -
                    self.current_hovered_place.pos[i]
                    for i in range(2)]
            to = self.temp_obj
            if self.adjusting_rect_mod == 1:
                npos = rpos
                nsize = [to.size[i] + to.rpos[i] - rpos[i] for i in range(2)]
            elif self.adjusting_rect_mod == 2:
                npos = to.rpos[:]
                nsize = [rpos[i] - to.rpos[i] for i in range(2)]
            else:
                self.temp_rpos = rpos
                self.adjusting_rect = 3
                return

            # If 1 or 2:
            self.temp_rpos = npos
            self.temp_size = nsize
            self.adjusting_rect = 4
            self.continue_adjusting_rect(pos)
        elif self.adjusting_rect == 3:
            rpos = [self.get_true_pos(pos)[i] -
                    self.current_hovered_place.pos[i]
                    for i in range(2)]
            self.temp_size = [rpos[i] - self.temp_rpos[i] for i in range(2)]
            self.adjusting_rect = 4
            self.continue_adjusting_rect(pos)
        elif self.adjusting_rect == 4:
            npos = self.temp_rpos
            nsize = self.temp_size
            for i in range(2):
                if nsize[i] < 0:
                    nsize[i] = -nsize[i]
                    npos[i] -= nsize[i]
            self.temp_obj.rpos = npos[:]
            self.temp_obj.size = nsize[:]
            self.temp_obj.update()

            self.adjusting_rect = False
            self.bgsurface.fill(self.bgcolor)

    def begin_creating_point(self):
        self.creating_point = 1
        self.bgsurface.fill((0, 255, 0))

    def continue_creating_point(self, pos):
        if self.creating_point == 1:
            rpos = [self.get_true_pos(pos)[i] -
                    self.current_hovered_place.pos[i]
                    for i in range(2)]
            self.current_hovered_place.create_point(rpos)
            self.creating_point = False
            self.bgsurface.fill(self.bgcolor)

    def create_link(self, a, b):
        self.links.append(Link(self, a, b))

    def begin_creating_link(self):
        self.creating_link = 1
        self.bgsurface.fill((100, 150, 200))

    def continue_creating_link(self):
        if self.creating_link == 1:
            self.temp_obj = self.current_hovered_place.highlighted_obj
            if self.temp_obj is not None and not \
                    (self.temp_obj.var == 'rect' and \
                         len(self.temp_obj.linked_with) > 0):
                self.creating_link = 2
        elif self.creating_link == 2:
            ntemp = self.current_hovered_place.highlighted_obj
            if ntemp != self.temp_obj and \
                    ntemp.var != self.temp_obj.var and not \
                    (ntemp.var == 'rect' and \
                         len(ntemp.linked_with) > 0):
                self.create_link(self.temp_obj, ntemp)
                self.creating_link = False
                self.bgsurface.fill(self.bgcolor)

    def begin_naming_rect(self, obj=None, also_name_target_dir=False):
        self.naming_rect = 1
        self.temp_also_name_dir = also_name_target_dir
        if obj is not None:
            self.temp_obj = obj
            self.reset_naming_rect()
        self.bgsurface.fill((200, 150, 100))

    def rect_namer(self, event):
        if event.key in (K_RETURN, K_KP_ENTER, K_ESCAPE):
            self.naming_rect = 2
            self.continue_naming_rect()
        elif event.key == K_BACKSPACE:
            self.temp_obj.name = self.temp_obj.name[:-1]
            self.temp_obj.update()
        else:
            self.temp_obj.name += event.unicode
            self.temp_obj.update()

    def reset_naming_rect(self):
        self.special_key_func = self.rect_namer

    def continue_naming_rect(self):
        if self.naming_rect == 1:
            self.temp_obj = self.current_hovered_place.highlighted_obj
            if self.temp_obj is not None and self.temp_obj.var == 'rect':
                self.reset_naming_rect()
        elif self.naming_rect == 2:
            self.special_key_func = None
            self.naming_rect = False
            self.temp_naming_obj = None
            self.bgsurface.fill(self.bgcolor)
            if self.temp_also_name_dir:
                self.also_name_dir = False
                self.begin_setting_target_dir(self.temp_obj)

    def begin_setting_target_dir(self, obj=None):
        self.setting_target_dir = 1
        if obj is not None:
            self.temp_obj = obj
            self.reset_setting_target_dir()
        self.bgsurface.fill((200, 150, 200))

    def dir_namer(self, event):
        if event.key in (K_RETURN, K_KP_ENTER, K_ESCAPE):
            self.setting_target_dir = 2
            self.continue_setting_target_dir()
        elif event.key == K_BACKSPACE:
            self.temp_obj.targetdir = self.temp_obj.targetdir[:-1]
            self.temp_obj.update()
        else:
            self.temp_obj.targetdir += event.unicode
            self.temp_obj.update()

    def reset_setting_target_dir(self):
        self.temp_obj.targetdir = ''
        self.special_key_func = self.dir_namer

    def continue_setting_target_dir(self):
        if self.setting_target_dir == 1:
            self.temp_obj = self.current_hovered_place.highlighted_obj
            if self.temp_obj is not None and self.temp_obj.var == 'rect':
                self.reset_setting_target_dir()
        elif self.setting_target_dir == 2:
            self.special_key_func = None
            self.setting_target_dir = False
            self.bgsurface.fill(self.bgcolor)

    def begin_deleting_obj(self):
        self.deleting_obj = 1
        self.bgsurface.fill((255, 0, 0))

    def continue_deleting_obj(self):
        if self.deleting_obj == 1:
            try:
                self.current_hovered_place.delete_highlighted_object()
            except Exception:
                self.current_hovered_place.delete_self()
            self.deleting_obj = False
            self.bgsurface.fill(self.bgcolor)

    def begin_deleting_link(self):
        self.deleting_link = 1
        self.bgsurface.fill((255, 0, 132))

    def continue_deleting_link(self):
        if self.deleting_link == 1:
            ls = self.current_hovered_place.highlighted_obj.linked_with
            for l in ls:
                self.links.remove(l)
                for w in l.objs:
                    try:
                        w.linked_with.remove(l)
                    except ValueError:
                        pass

            self.deleting_link = False
            self.bgsurface.fill(self.bgcolor)

    def begin_obj_moving(self):
        self.moving_an_object = 1
        self.bgsurface.fill((55, 55, 132))

    def continue_obj_moving(self, pos):
        if self.moving_an_object == 1:
            self.temp_object = \
                self.current_hovered_place.highlighted_obj
            if self.temp_object is not None:
                self.temp_rpos = self.temp_object.rpos
                self.moving_an_obj_pos = pos
                self.moving_an_object = 2
        elif self.moving_an_object == 2:
            npos = [self.temp_rpos[i] +
                    (pos[i] - self.moving_an_obj_pos[i])
                    / self.zoom for i in range(2)]
            to = self.temp_object
            if npos[0] < 0:
                npos[0] = 0
            if npos[1] < 0:
                npos[1] = 0
            if npos[0] + to.size[0] > to.place.size[0]:
                npos[0] = to.place.size[0] - to.size[0]
            if npos[1] + to.size[1] > to.place.size[1]:
                npos[1] = to.place.size[1] - to.size[1]

            if self.temp_object.var == 'point':
                o = self.temp_object
                o.rrpos = [o.rrpos[i] + npos[i] - o.rpos[i] for i in range(2)]
            self.temp_object.rpos = npos

    def end_obj_moving(self):
        self.moving_an_object = False
        self.bgsurface.fill(self.bgcolor)


    def run(self):
        clock = pygame.time.Clock()
        done = False
        while not done:
            clock.tick(30)

            pos = pygame.mouse.get_pos()
            self.get_hovered_place(pos)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        cont = True
                        if self.current_hovered_place is not None:
                            cont = False
                            if self.creating_rect:
                                self.continue_creating_rect(pos)
                            elif self.adjusting_rect:
                                self.continue_adjusting_rect(pos)
                            elif self.creating_point:
                                self.continue_creating_point(pos)
                            elif self.creating_link:
                                self.continue_creating_link()
                            elif self.naming_rect:
                                self.continue_naming_rect()
                            elif self.setting_target_dir:
                                self.continue_setting_target_dir()
                            elif self.deleting_obj:
                                self.continue_deleting_obj()
                            elif self.deleting_link:
                                self.continue_deleting_link()
                            elif self.moving_an_object == 1:
                                self.continue_obj_moving(pos)
                            else: cont = True
                        if cont:
                            if not self.moving:
                                self.begin_screen_moving(pos)

                    elif event.button == 3:
                        if not self.moving_a_place and \
                                self.current_hovered_place is not None:
                            self.begin_place_moving(pos)

                    elif event.button == 4:
                        self.relative_zoom(pos, True)
                    elif event.button == 5:
                        self.relative_zoom(pos, False)

                    elif event.button == 2:
                        self.new_center(pos)

                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.moving_an_object:
                            self.end_obj_moving()
                        elif self.moving:
                            self.end_screen_moving()
                    elif event.button == 3:
                        if self.moving_a_place:
                            self.end_place_moving()

                elif event.type == MOUSEMOTION:
                    if self.moving_an_object == 2:
                        self.continue_obj_moving(pos)

                    if self.moving:
                        self.continue_screen_moving(pos)

                    if self.moving_a_place:
                        self.continue_place_moving(pos)

                elif event.type == KEYDOWN:
                    if self.special_key_func is not None:
                        self.special_key_func(event)
                        continue

                    nothing = \
                        not self.creating_rect and \
                        not self.adjusting_rect and \
                        not self.creating_point  and \
                        not self.creating_link    and \
                        not self.naming_rect       and \
                        not self.setting_target_dir and \
                        not self.deleting_obj        and \
                        not self.deleting_link        and \
                        not self.moving_an_object

                    if event.key == K_r and nothing:
                        self.begin_creating_rect()
                    if event.key == K_a and nothing:
                        mods = pygame.key.get_mods()
                        if mods & KMOD_SHIFT:
                            mod = 1
                        elif mods & KMOD_CTRL:
                            mod = 2
                        else:
                            mod = 0
                        self.begin_adjusting_rect(mod)
                    elif event.key == K_p and nothing:
                        self.begin_creating_point()
                    elif event.key == K_l and nothing:
                        self.begin_creating_link()
                    elif event.key == K_n and nothing:
                        self.begin_naming_rect()
                    elif event.key == K_d and nothing:
                        self.begin_setting_target_dir()
                    elif event.key == K_DELETE and nothing:
                        self.begin_deleting_obj()
                    elif event.key == K_e and nothing:
                        self.begin_deleting_link()
                    elif event.key == K_m and nothing:
                        self.begin_obj_moving()
                    elif event.key == K_PAGEDOWN:
                        self.relative_zoom(pos, False)
                    elif event.key == K_PAGEUP:
                        self.relative_zoom(pos, True)
                    elif event.key == K_s:
                        mods = pygame.key.get_mods()
                        if mods & KMOD_CTRL:
                            self.save()
                        elif not nothing:
                            self.creating_rect = False
                            self.adjusting_rect = False
                            self.creating_point = False
                            self.creating_link = False
                            self.naming_rect = False
                            self.setting_target_dir = False
                            self.deleting_obj = False
                            self.deleting_link = False
                            self.moving_an_object = False
                            self.bgsurface.fill(self.bgcolor)
                    elif event.key == K_ESCAPE:
                        done = True
                elif event.type == QUIT:
                    done = True

            self.screen.blit(self.bgsurface, (0, 0))
            for plc in self.places:
                plc.draw()
            for l in self.links:
                l.draw()

            pygame.display.flip()

from datetime import datetime
import os.path
import pygame
from pygame.locals import *

class WalkTestAdvanced:
    def __init__(self, sett):
        self.directory = sett.directory
        self.time = sett.time
        self.direction = sett.direction
        self.bgtype = sett.background
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

        self.bgsurface = pygame.Surface(self.screen.get_size()).convert()

        self.clock = pygame.time.Clock()
        self.loop()

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

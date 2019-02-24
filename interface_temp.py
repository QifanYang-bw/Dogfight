""" interface.py

Contains the Reversi Interface class.
"""
import sys
import pygame as pg
from envi import *
# from const import *
# from core import *

import random

""" Initialization """

Image_Path = 'image/'

""" The length and size data here consists with the board
image.
"""

class Game(object):
    def __init__(self):
        self.done = False
        self.screen = pg.display.set_mode((640, 320))
        self.screen_rect = self.screen.get_rect()

        self.fps = 30
        self.clock = pg.time.Clock()

        # self.spawn_timer = 0
        # self.spawn_frequency = 3000 #milliseconds
        # self.enemies = pg.sprite.Group()

        self.player = [plane(0, vec(100, Bottom_Margin))]
        self.player[0].key[87] = True

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done  = True

    def update(self, dt):
        for obj in self.player:
            obj.frame_control()
            obj.fly()

        if random.random() < 0.1:
            self.player[0].key[68] = True
        else:
            self.player[0].key[68] = False

    def draw(self):
        with self.player[0] as p:
            print(p.heading, p.pos, p._rotation)


            self.rect = pg.Rect(0, 0, 24, 6)
            self.rect.center = p.pos.tocp()
            # self.pos = self.rect.center

            self.image = pg.Surface(self.rect.size)
            if not p.crashed:
                self.image.fill(pg.Color("dodgerblue"))
            else:
                self.image.fill(pg.Color("red"))


            self.screen.fill(pg.Color("gray10"))
            self.screen.blit(self.image, self.rect)

            # self.rot = pygame.transform.rotate(Surface, angle)

            # self.rect = mySprite.image.get_rect()

        # self.screen.fill(pg.Color("gray10"))
        # self.enemies.draw(self.screen)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
    pg.quit()
    sys.exit()

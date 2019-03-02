""" interface.py

Contains the Reversi Interface class.
"""
import sys
import pygame as pg

from lib import *
from envi import *
# from const import *
# from core import *

""" Initialization """

Image_Path = 'resources/'
Planeimg_Filename = ['plane1.png', 'plane2.png']

""" The length and size data here consists with the board image.
"""

class Player(pg.sprite.Sprite):
    def __init__(self, plane, image, color):
        super().__init__()

        self.plane = plane

        self.image = image
        # Store a reference to the original to preserve the image quality.
        self.orig_image = self.image

        self.color = color

        self.pos = (plane.pos.x, plane.pos.y)
        self.rect = self.image.get_rect(center = self.pos)

        self.angle = plane.rotation
        self.angle_change = 0

    def update(self):
        if self.plane.heading == 0:
            self.angle = (540 - self.plane.rotation) % 360
        else:
            self.angle = 360 - self.plane.rotation

        # rotozoom is preferred. 
        self.image = pg.transform.rotozoom(self.orig_image, self.angle, 1)
        self.pos = (self.plane.pos.x, self.plane.pos.y)
        self.rect = self.image.get_rect(center = self.pos)

class Game(object):
    def __init__(self):
        self.done = False
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.screen_rect = self.screen.get_rect()

        self.fps = 30
        self.clock = pg.time.Clock()

        self.PlaneImg = []
        for Plane_Filename in Planeimg_Filename:
            curimage = pg.image.load(Image_Path + Plane_Filename).convert_alpha()
            
            # curimage.set_colorkey((255,255,255))
            # cursize = curimage.get_size()
            cur_imgresize = pg.transform.scale(curimage, (42, 16))

            self.PlaneImg.append(cur_imgresize)

        self.all_sprites = pg.sprite.Group()

        # self.enemies = pg.sprite.Group()

        self.players = [Plane(0, vec(100, Bottom_Margin)), Plane(1, vec(540, Bottom_Margin))]
        self.players[0].enemy = self.players[1]
        self.players[1].enemy = self.players[0]

        self.playerdisplay = [Player(self.players[0], self.PlaneImg[0], (128, 220, 32)),
                              Player(self.players[1], self.PlaneImg[1], (220, 64,  64))]

        for _ in self.playerdisplay:
            self.all_sprites.add(_)

    def event_loop(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.done = True

            boolValue = None
            if event.type == pg.KEYDOWN:
                # Set the rotation speed of the car sprite.
                boolValue = True
            elif event.type == pg.KEYUP:
                # Stop rotating if the player releases the keys.
                boolValue = False

            with self.players[0] as p1:
                if event.key == pg.K_LEFT:
                    p1.key['Left'] = boolValue
                elif event.key == pg.K_RIGHT:
                    p1.key['Right'] = boolValue
                elif event.key == pg.K_UP:
                    p1.key['Up'] = boolValue
                elif event.key == pg.K_DOWN:
                    p1.key['Down'] = boolValue
                elif event.key == pg.K_COMMA:
                    p1.key['Fire'] = boolValue


            if len(self.players) > 1:
                with self.players[1] as p2:
                    if event.key == pg.K_a:
                        p2.key['Left'] = boolValue
                    elif event.key == pg.K_d:
                        p2.key['Right'] = boolValue
                    elif event.key == pg.K_w:
                        p2.key['Up'] = boolValue
                    elif event.key == pg.K_s:
                        p2.key['Down'] = boolValue
                    elif event.key == pg.K_v:
                        p2.key['Fire'] = boolValue


    def update(self, dt):
        alive_count = 0

        for obj in self.players:
            if not obj.crashed:
                obj.frame_control()
                obj.fly()


    def draw(self):

        self.all_sprites.update()

        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        for player in self.playerdisplay:
            plane = player.plane
            if plane.beam_track[0] > 0:
                plane.beam_track[0] -= 1
                pg.draw.lines(self.screen, player.color, False, [(plane.pos.x, plane.pos.y), plane.beam_track[1]], 2)

        pg.display.flip()

        # pygame.draw.lines(screen, color, closed, pointlist, thickness)

        # with self.players[0] as p:
        #     print(p.heading, p.pos, p._rotation)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            # pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
    pg.quit()
    sys.exit()

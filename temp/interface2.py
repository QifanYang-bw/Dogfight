""" interface.py

Contains the Game Interface class.
"""
import sys
import pygame as pg

from const import *
from lib import *
from envi import *

""" Game Constants """

controlseq = ['Left', 'Right', 'Up', 'Down', 'Fire']

p1_keyseq = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_COMMA]
p2_keyseq = [pg.K_a, pg.K_d, pg.K_w, pg.K_s, pg.K_v]

p1_init_pos = vec(100, Bottom_Margin)
p2_init_pos = vec(540, Bottom_Margin)

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
        self.close = False
        self.winner = None

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

        self.players = [Plane(playerlist[0], 0, p1_init_pos.copy()),
                        Plane(playerlist[1], 1, p2_init_pos.copy())]

        self.players[0].enemy = self.players[1]
        self.players[1].enemy = self.players[0]

        self.playerdisplay = [Player(self.players[0], self.PlaneImg[0], (128, 220, 32)),
                              Player(self.players[1], self.PlaneImg[1], (220, 64,  64))]

        for _ in self.playerdisplay:
            self.all_sprites.add(_)

    def event_loop(self):

        # for p in self.players:
        #     if p.controller == PlayerState.AI_RL:
        #         output_key = RLagent.think(p)

        #         for i in range(len(output_key)):
        #             p.key[controlseq[i]] = output_key[i]

        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.close = True

            boolValue = None
            if event.type == pg.KEYDOWN:
                boolValue = True
            elif event.type == pg.KEYUP:
                boolValue = False

            with self.players[0] as p:
                if p.controller == PlayerState.Human:
                    for i in range(len(p1_keyseq)):
                        if event.key == p1_keyseq[i]:
                            p.key[controlseq[i]] = boolValue
                            break


            with self.players[1] as p:
                if len(self.players) > 1:
                    if p.controller == PlayerState.Human:
                        for i in range(len(p2_keyseq)):
                            if event.key == p2_keyseq[i]:
                                p.key[controlseq[i]] = boolValue
                                break


    def update(self):
        alive_count = 0

        for obj in self.players:
            if not obj.crashed and obj.hp > 0:
                alive_count += 1

                obj.frame_control()
                obj.fly()

        if alive_count <= 1:
            self.winner = "No Winner"
            for obj_num in range(len(self.players)):
                if not self.players[obj_num].crashed and self.players[obj_num].hp > 0:
                    self.winner = 'Player ' + str(obj_num)

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
        while not self.close and self.winner == None:
            self.update()

            dt = self.clock.tick(self.fps)
            self.draw()
            # pg.display.update()

        print(self.winner, 'wins!')

        while not self.close:
            self.event_loop()

def main():
    game = Game()
    game.run()
    pg.quit()
    sys.exit()

'''
Check if main.py is the called program.
'''
if __name__ == '__main__':
    main()

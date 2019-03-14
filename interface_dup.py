""" interface.py

Contains the Game Interface class.
"""

# ------ Temporary Const Def ------

from enum import Enum

# dirname = os.path.dirname(__file__)

class PlayerState(Enum):
    Human = 0
    AI_RL = 1

playerlist = [PlayerState.AI_RL, PlayerState.AI_RL]

# ------ Temporary Const Def ------

import sys
import random
import pygame as pg

from lib import *
from envi import *

""" Game Constants """

controlseq = ['Left', 'Right', 'Up', 'Down', 'Fire']

p1_keyseq = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_COMMA]
p2_keyseq = [pg.K_a, pg.K_d, pg.K_w, pg.K_s, pg.K_v]

Input_Dim = 18
Output_Dim = 5

p1_init_pos = vec(100, Bottom_Margin)
p2_init_pos = vec(540, Bottom_Margin)

# Upper and Lower limit of data, for normalization
#                 [_.heading, _.pos.x, _.pos.y, _.speed, _.rotation, _.accel.x, _.accel.y, _.missile_cooldown, _.hp]
state_upper_bar = [1, Right_Margin,     Top_Margin,    2, 360, 2,  2, 105, 100]
state_lower_bar = [0, Left_Margin - 30, Bottom_Margin, 0, 0,   0,  0, 0,     0]

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

    def reset(self):
        self.close = False
        self.winner = None

        self.players[0].reset(p1_init_pos.copy())
        self.players[1].reset(p2_init_pos.copy())

        self.players[0].enemy = self.players[1]
        self.players[1].enemy = self.players[0]

    def done(self):
        return self.winner != None

    def state(self, serial):
        serial -= 1

        cur_player = self.players[serial]

        cur_state = []

        for _ in [cur_player, cur_player.enemy]:

            _state = [_.heading, _.pos.x, _.pos.y, _.speed, _.rotation, _.accel.x, _.accel.y, \
                      _.missile_cooldown, _.hp]

            for i in range(len(_state)):
                _state[i] = (_state[i] - state_lower_bar[i]) / (state_upper_bar[i] - state_lower_bar[i])

            cur_state += _state

        return cur_state

    def reward(self, serial):
        serial -= 1

        return self.players[serial].score()

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

        pg.display.update()

        # pygame.draw.lines(screen, color, closed, pointlist, thickness)

        # with self.players[0] as p:
        #     print(p.heading, p.pos, p._rotation)

    def clear(self):
        '''
            System would mark the program as freezed without the command.
        '''
        # pg.event.clear()

        # To allow the user to close the process:

        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.close = True

    def make_move(self, serial, output_state):
        serial -= 1

        with self.players[serial] as p:
            for i in range(Output_Dim):

                boolValue = random.random() < output_state[i]

                p.key[controlseq[i]] = boolValue

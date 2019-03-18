""" interface.py

Contains the Game Interface class.
"""

import sys
import random
import pygame as pg

from const import *
from lib import *
from envi import *
from AI_DQN import *

""" Game Constants """

playerlist = [PlayerState.AI_RL, PlayerState.AI_RL]

controlseq = ['Left', 'Right', 'Up', 'Down', 'Fire']

p1_keyseq = [pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN, pg.K_COMMA]
p2_keyseq = [pg.K_a, pg.K_d, pg.K_w, pg.K_s, pg.K_v]

p1_init_pos = vec(100, Bottom_Margin)
p2_init_pos = vec(540, Bottom_Margin)

""" Initialization """

Image_Path = 'resources/'
Planeimg_Filename = ['plane1.png', 'plane2.png']

pos_rand_const = 0.6
step_upper_thresh = 50000

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

        self.PlaneImg = []
        for Plane_Filename in Planeimg_Filename:
            curimage = pg.image.load(Image_Path + Plane_Filename).convert_alpha()
            
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

    def reset(self, rand = 0):
        self.close = False
        self.winner = None

        if random.random() > rand:
            self.players[0].reset(p1_init_pos.copy())
            self.players[1].reset(p2_init_pos.copy())
        else:
            self.players[0].random_state()
            self.players[1].random_state()

            # print(self.players[0]., self.players[1].accel)

        self.players[0].enemy = self.players[1]
        self.players[1].enemy = self.players[0]

    def done(self):
        return self.winner != None

    def state(self, serial):
        serial -= 1

        cur_player = self.players[serial]

        cur_state = []

        for _ in [cur_player, cur_player.enemy]:

            _state = [_.heading, _.pos.x, _.pos.y, _.speed, _.rotation, _.accel.x, _.accel.y, _.hp]

            for i in range(len(_state)):
                _state[i] = (_state[i] - state_lower_bar[i]) / (state_upper_bar[i] - state_lower_bar[i])

            if _ == cur_player:
                cur_state += _state
            else:
                cur_state += _state[1:]

        return cur_state

    def reward(self, serial):
        serial -= 1

        return self.players[serial].score()

    def update(self):
        alive_count = 0

        for obj in self.players:
            if not obj.crashed and obj.hp > 0:
                obj.frame_control()
                obj.fly()

            if not obj.crashed and obj.hp > 0:
                alive_count += 1

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

        # print(output_state, net_output_bool[output_state])

        for i in range(len(controlseq)):

            self.players[serial].key[controlseq[i]] = net_output_bool[output_state][i]
            

params = {
    'training': True,
    'gamma': 0.95,
    'epsi_high': 0.9,
    'epsi_low': 0.05,
    'decay': int(5e5), # Need edit
    'lr': 0.001,
    'buffer_size': 40000,
    'batch_size': 64,
    'unusual_sample_factor': 0.99,
    'state_space_dim': Input_Dim,
    'action_space_dim': Output_Dim
}

def main():

    env = Game()

    agent = Agent_RL(**params)

    score_1 = []
    mean_1 = []

    agent.load()

    for episode in range(2000):
        env.reset(rand = min(((1 - agent.epsi) ** 2) / 2, pos_rand_const))

        total_reward_p1 = 0 
        total_reward_p2 = 0

        s0_1 = env.state(serial = 1)
        s0_2 = env.state(serial = 2)

        r1_1 = env.reward(1)
        r1_2 = env.reward(2)

        # while True:
        print('Episode', episode)
        print('Epsi {:.4f}'.format(agent.epsi))

        _ = 0
        while _ < step_upper_thresh:
            _ += 1

            env.clear()

            if env.close:
                break

            env.draw()

            a0_1 = agent.act(s0_1)
            a0_2 = agent.act(s0_2)

            env.make_move(1, a0_1)
            env.make_move(2, a0_2)

            env.update()

            s1_1, s1_2 = env.state(1), env.state(2)

            r1_1 = env.reward(1)
            r1_2 = env.reward(2)

            if _ % 100 == 0:

                print('Trial', _, end = ' [')

                for data in net_output_bool[a0_1]:
                    print(int(data), end = '')

                print('] {:.4f} {:.1f}  ['.format(r1_1, env.players[0].hp), end = '')

                for data in net_output_bool[a0_2]:
                    print(int(data), end = '')

                print('] {:.4f} {:.1f}'.format(r1_2, env.players[1].hp))

            if r1_1 != 0 or random.random() < 0.01:
                agent.put(s0_1, a0_1, r1_1, s1_1)
            if r1_2 != 0 or random.random() < 0.01: 
                agent.put(s0_2, a0_2, r1_2, s1_2)
            
            agent.learn()

            total_reward_p1 += r1_1
            total_reward_p2 += r1_2

            if env.done():
                break

            s0_1, s0_2 = s1_1, s1_2

        if _ >= step_upper_thresh:
            print('\nStop current episode with no winner\n')

        if env.close:
            break

        score_1.append(total_reward_p1 + total_reward_p2)
        mean_1.append( sum(score_1[-100:])/min(len(score_1), 100))

        if episode % 5 == 0:
            print('Score: {:.3f}, Mean: {:.3f}'.format(score_1[-1], mean_1[-1]))
            agent.save()

        # agent.plot(score, mean)

    pg.quit()
    sys.exit()

'''
Check if main.py is the called program.
'''
if __name__ == '__main__':
    main()

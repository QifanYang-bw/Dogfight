""" interface.py

Contains the Game Interface class.
"""

import sys
import random

from const import *
from lib import *
from envi import *
from AI_DQN import *

from game_count_nd import compete

import csv

""" Game Constants """

controlseq = ['Left', 'Right', 'Up', 'Down', 'Fire']

p1_init_pos = vec(100, Bottom_Margin)
p2_init_pos = vec(540, Bottom_Margin)

step_upper_thresh = 50000

""" Initialization """

pos_rand_const = 0.1
random_shift_prob = 0.001

class Game(object):
    def __init__(self, plist):
        self.close = False
        self.winner = None

        self.players = [Plane(plist[0], 0, p1_init_pos.copy(), mute = True, hp = 10),
                        Plane(plist[1], 1, p2_init_pos.copy(), mute = True, hp = 10)]

        self.players[0].enemy = self.players[1]
        self.players[1].enemy = self.players[0]

    def reset(self, rand = 0):
        self.close = False
        self.winner = None

        if random.random() > rand:
            self.players[0].reset(p1_init_pos.copy(), hp = 10)
            self.players[1].reset(p2_init_pos.copy(), hp = 10)
        else:
            self.players[0].random_state()
            self.players[1].random_state()

        self.players[0].enemy = self.players[1]
        self.players[1].enemy = self.players[0]

    def done(self):
        alive_count = 0

        for obj in self.players:
            if not obj.crashed and obj.hp > 0:
                alive_count += 1

        if alive_count <= 1:
            self.winner = "No Winner"
            for obj_num in range(len(self.players)):
                if not self.players[obj_num].crashed and self.players[obj_num].hp > 0:
                    self.winner = 'Player ' + str(obj_num)

        return self.winner != None



    def state(self, serial):
        serial -= 1

        cur_player = self.players[serial]
        cur_state = []

        for _ in [cur_player, cur_player.enemy]:

            if serial == 0:

                _state = [_.pos.x, _.pos.y, _.speed, _.rotation, _.accel.x, _.accel.y, _._stall]

                for i in range(len(_state)):
                    _state[i] = (_state[i] - state_lower_bar[i]) / (state_upper_bar[i] - state_lower_bar[i])

            else:

                new_rot = vertical_mirror(_.rotation)

                _state = [Right_Margin - (_.pos.x - (Left_Margin - 30)), _.pos.y, _.speed, new_rot, -_.accel.x, _.accel.y, _._stall]

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
            if random.random() > random_shift_prob:
                if not obj.crashed and obj.hp > 0:
                    obj.frame_control()
                    obj.fly()
            else:
                obj.random_state()

    def make_move(self, serial, output_state):
        serial -= 1

        # print(output_state, net_output_bool[output_state])

        for i in range(len(controlseq)):

            self.players[serial].key[controlseq[i]] = net_output_bool[output_state][i]
            

params = {
    'training': True,
    'gamma': 0.96,
    'epsi_high': 0.9,
    'epsi_low': 0.1,
    'decay': int(1e5), # Need edit
    'lr': 0.0005,
    'buffer_size': 80000,
    'batch_size': 64,
    'state_space_dim': Input_Dim,
    'action_space_dim': Output_Dim
}


def main():

    plist = [PlayerState.AI_RL, PlayerState.AI_RL]

    env = Game(plist = plist)

    agent = Agent_RL(**params)

    score_1 = []
    mean_1 = []

    # agent.load()

    test_flag = False

    for episode in range(1000):

        rands = min(1 - agent.epsi, pos_rand_const)

        env.reset(rand = rands)

        total_reward_p1 = 0 
        total_reward_p2 = 0

        s0_1 = env.state(serial = 1)
        s0_2 = env.state(serial = 2)

        r1_1 = env.reward(1)
        r1_2 = env.reward(2)

        if episode % 2 == 0 and episode < 200 or episode % 10 == 0:
            test_flag = True
        else:
            test_flag = False

        if test_flag:
            print('Episode', episode)
            print('Epsi {:.4f}'.format(agent.epsi))

        _ = 0
        while _ < step_upper_thresh:
            _ += 1

            a0_1 = agent.act(s0_1)
            a0_2 = agent.act(s0_2)

            env.make_move(1, a0_1)
            env.make_move(2, a0_2)

            env.update()

            s1_1, s1_2 = env.state(1), env.state(2)

            r1_1 = env.reward(1)
            r1_2 = env.reward(2)

            if test_flag:
                if _ % 200 == 0:
                    print('Trial', _, end = ' [')

                    for data in net_output_bool[a0_1]:
                        print(int(data), end = '')

                    print('] {:.2f} {:.1f}  ['.format(r1_1, env.players[0].hp), end = '')

                    for data in net_output_bool[a0_2]: 
                        print(int(data), end = '')

                    print('] {:.2f} {:.1f}'.format(r1_2, env.players[1].hp))

            if r1_1 != 0 or random.random() < 1: 
                agent.put(s0_1, a0_1, r1_1, s1_1)
            if r1_2 != 0 or random.random() < 1: 
                agent.put(s0_2, a0_2, r1_2, s1_2)
            
            agent.learn()

            total_reward_p1 += r1_1
            total_reward_p2 += r1_2

            if env.done():
                break

            s0_1, s0_2 = s1_1, s1_2


        score_1.append(total_reward_p1 + total_reward_p2)
        mean_1.append(sum(score_1[-100:])/min(len(score_1), 100))

        if test_flag:

            agent.save()

            with open(r'winrate.csv', 'a') as f:
                writer = csv.writer(f)

                ratio = compete(record = False, total_trial = 100)
                fields = [episode, agent.steps, ratio]

                writer.writerow(fields)

            print('Episode', episode, 'ends')
            print('Score: {:.3f}, Mean: {:.3f}\n'.format(score_1[-1], mean_1[-1]))

            print('Training...\n\n')

        # if _ > 10000 and _ % 10000 == 0:
        #     print('\n', score_1, '\n')

        # if _ >= step_upper_thresh:
        #     print('\nStop current episode with no winner\n')

        if env.close:
            break


        # agent.plot(score, mean)

    sys.exit()

'''
Check if main.py is the called program.
'''
if __name__ == '__main__':
    main()

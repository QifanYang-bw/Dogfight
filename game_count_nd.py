"""
Contains the Game Interface class.
"""

import sys

from const import *
from lib import *
from envi import *

# -------------------- Loading Agent Library -------------------- #

from AI_DQN import *

params = {
    'training': False,
    'state_space_dim': Input_Dim,
    'action_space_dim': Output_Dim
}

RLAgent = Agent_RL(**params)
RLAgent.load()

from AI_hardcoded import *

HCAgent = Agent_Hardcoded()


# -------------------- End of Agent Loading -------------------- #



# -------------------- Initialization -------------------- #

controlseq = ['Left', 'Right', 'Up', 'Down', 'Fire']

p1_init_pos = vec(100, Bottom_Margin)
p2_init_pos = vec(540, Bottom_Margin)

# -------------------- End of Initialization -------------------- #

class Game_Count(object):
    def __init__(self, plist = playerlist, mute = True):

        self.mute = mute

        self.plist = plist

        self.close = False
        self.winner = None

        self.players = [Plane(plist[0], 0, p1_init_pos.copy(), mute = self.mute),
                        Plane(plist[1], 1, p2_init_pos.copy(), mute = self.mute)]

        self.players[0].enemy = self.players[1]
        self.players[1].enemy = self.players[0]


    def event_loop(self):

        for serial in range(2):

            p = self.players[serial]

            if p.controller == PlayerState.AI_RL or p.controller == PlayerState.AI_Random:
                cur_state = self.state(serial + 1)

                if p.controller == PlayerState.AI_RL:
                    output_act = RLAgent.act(cur_state)
                elif p.controller == PlayerState.AI_Random:
                    output_act = RLAgent.act(cur_state, epsi = 1)

                for i in range(len(controlseq)):
                    self.players[serial].key[controlseq[i]] = net_output_bool[output_act][i]

            if p.controller == PlayerState.AI_Hardcoded:
                output_set = HCAgent.act(p)

                for i in range(len(controlseq)):
                    self.players[serial].key[controlseq[i]] = output_set[i]


    def reset(self):
        self.close = False
        self.winner = None

        self.players = [Plane(self.plist[0], 0, p1_init_pos.copy(), mute = self.mute),
                        Plane(self.plist[1], 1, p2_init_pos.copy(), mute = self.mute)]

        self.players[0].enemy = self.players[1]
        self.players[1].enemy = self.players[0]


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
                    self.winner = 'Player ' + str(obj_num + 1)


    def run(self, record = False, count = 0):
        while not self.close and self.winner == None:
            self.event_loop()
            self.update()

        hp1 = self.players[0].hp
        hp2 = self.players[1].hp
        crashed = False
        if self.players[0].crashed: 
            hp1 = 0
            crashed = True
        if self.players[1].crashed:
            hp2 = 0
            crashed = True

        return (self.winner, hp1, hp2, crashed)


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


def compete(record = True, total_trial = 100):

    global enable_print

    if not record:
        enable_print = False

    plist = [PlayerState.AI_RL, PlayerState.AI_Hardcoded]

    game = Game_Count(plist = plist)

    winner = [0, 0]

    print('Game Running ... ', end = '')

    for trial_count in range(total_trial):

        game.reset()

        if trial_count % 20 == 0:
            print('#{} ... '.format(trial_count), end = '')

        rec_flag = record and trial_count % 20 == 0

        res, hp1, hp2, crashed = game.run(record = rec_flag, count = trial_count)

        if game.close:
            break

        if hp1 > hp2 and plist[0] == PlayerState.AI_RL or hp1 < hp2 and plist[1] == PlayerState.AI_RL:
            winner[0] += 1
        else:
            winner[1] += 1

        if random.random() >= 0.5:
            plist[0], plist[1] = plist[1], plist[0]
            game.plist = plist

    print('\nAI wins', winner[0], 'of', total_trial, 'matches.\n')

    if not record:
        enable_print = True

    return winner[0] / total_trial

'''
Check if main.py is the called program.
'''
if __name__ == '__main__':
    compete()

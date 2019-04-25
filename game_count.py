""" 
Contains the Game Interface class.
"""

import sys
import pygame as pg

from game import *

""" Set Up Manual Print Function """

enable_print = True

def lprint(*args, **kwargs):
    if enable_print:
        return print(*args, **kwargs)

class Game_Count(Game):
    def __init__(self, plist = playerlist):
        super().__init__(plist = plist, mute = True)

        self.plist = plist

    def reset(self):
        self.close = False
        self.winner = None

        self.all_sprites = pg.sprite.Group()

        self.players = [Plane(self.plist[0], 0, p1_init_pos.copy(), mute = self.mute),
                        Plane(self.plist[1], 1, p2_init_pos.copy(), mute = self.mute)]

        self.players[0].enemy = self.players[1]
        self.players[1].enemy = self.players[0]

        self.playerdisplay = [Player(self.players[0], self.PlaneImg[0], (128, 220, 32)),
                              Player(self.players[1], self.PlaneImg[1], (220, 64,  64))]

        for _ in self.playerdisplay:
            self.all_sprites.add(_)


    def run(self, record = False, count = 0):
        while not self.close and self.winner == None:
            self.event_loop()
            self.update()

            self.draw()

        if record:
            fname = "result/winimg" + str(count) + ".png"
            pg.image.save(self.screen, fname)

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


def compete(record = True, total_trial = 100):

    global enable_print

    if not record:
        enable_print = False

    plist = [PlayerState.AI_RL, PlayerState.AI_Hardcoded]

    game = Game_Count(plist = plist)

    winner = [0, 0]
    for trial_count in range(total_trial):

        game.reset()

        lprint('Game #{} Running ... '.format(trial_count), end = '')

        rec_flag = record and trial_count % 20 == 0

        res, hp1, hp2, crashed = game.run(record = rec_flag, count = trial_count)

        if game.close:
            break

        if hp1 > hp2 and plist[0] == PlayerState.AI_RL or hp1 < hp2 and plist[1] == PlayerState.AI_RL:
            lprint('AI_RL wins with', '{}:{}'.format(hp1, hp2), end = '')
            if crashed:
                lprint(' due to crashing')
            else:
                lprint()
            winner[0] += 1
        else:
            lprint('AI_HC wins with', '{}:{}'.format(hp1, hp2), end = '')
            if crashed:
                lprint(' due to crashing')
            else:
                lprint()
            winner[1] += 1

        if random.random() >= 0.5:
            plist[0], plist[1] = plist[1], plist[0]
            game.plist = plist

    print('AI', 'wins', winner[0], 'of', total_trial, 'matches')

    if not record:
        enable_print = True

    return winner[0] / total_trial

'''
Check if main.py is the called program.
'''
if __name__ == '__main__':
    compete()

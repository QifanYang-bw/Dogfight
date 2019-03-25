""" 
Contains the Game Interface class.
"""
import sys
import pygame as pg

from game import *

""" Import Multiple AIs """

total_trial = 1000

class Game_Count(Game):
    def __init__(self):
        super().__init__(mute = True)

    def reset(self):
        self.close = False
        self.winner = None

        self.all_sprites = pg.sprite.Group()

        self.players = [Plane(playerlist[0], 0, p1_init_pos.copy(), mute = self.mute),
                        Plane(playerlist[1], 1, p2_init_pos.copy(), mute = self.mute)]

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

        # while not self.close:
        #     self.event_loop()


def main():
    game = Game_Count()

    winner = [0, 0]
    for trial_count in range(total_trial):

        game.reset()

        print('Game #{} Running ... '.format(trial_count), end = '')

        res, hp1, hp2, crashed = game.run(record = trial_count % 20 == 0, count = trial_count)

        if game.close:
            break

        if hp1 > hp2 and playerlist[0] == PlayerState.AI_RL or hp1 < hp2 and playerlist[1] == PlayerState.AI_RL:
            print('AI_RL wins with', '{}:{}'.format(hp1, hp2), end = '')
            if crashed:
                print(' due to crashing')
            else:
                print()
            winner[0] += 1
        else:
            print('AI_HC wins with', '{}:{}'.format(hp1, hp2), end = '')
            if crashed:
                print(' due to crashing')
            else:
                print()
            winner[1] += 1

        if random.random() >= 0.5:
            playerlist[0], playerlist[1] = playerlist[1], playerlist[0]

    if winner[0] > winner[1]:
        argmax = 0
    else:
        argmax = 1

    print('Player', argmax + 1, 'wins', winner[argmax], 'of', total_trial, 'matches')
    pg.quit()
    sys.exit()

'''
Check if main.py is the called program.
'''
if __name__ == '__main__':
    main()

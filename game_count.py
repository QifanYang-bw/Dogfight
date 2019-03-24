""" 
Contains the Game Interface class.
"""
import sys
import pygame as pg

from game import *

playerlist = [PlayerState.AI_RL, PlayerState.AI_Hardcoded]

total_trial = 100

class Game_Count(Game):
    def __init__(self):
        super().__init__(mute = True)

    def run(self):
        while not self.close and self.winner == None:
            self.event_loop()
            self.update()

            # dt = self.clock.tick(self.fps)
            self.draw()
            # pg.display.update()

        hp1 = self.players[0].hp
        hp2 = self.players[1].hp
        if self.players[0].crashed: 
            hp1 = 0
        if self.players[1].crashed: 
            hp2 = 0

        return (self.winner, hp1, hp2)

        # while not self.close:
        #     self.event_loop()


def main():
    game = Game_Count()

    winner = [0, 0]
    for trial_count in range(total_trial):

        print('Game #{} Running ... '.format(trial_count), end = '')

        res, hp1, hp2 = game.run()
        print(res, 'wins!')

        if hp1 > hp2:
            winner[0] += 1
        else:
            winner[1] += 1

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
    print(playerlist)
    main()

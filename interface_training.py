""" interface.py

Contains the Game Interface class.
"""
import sys

from lib import *
from envi import *

from AI_Frame import *

""" Initialization """

""" The length and size data here consists with the board image.
"""

# playerlist = [PlayerState.AI_RL, PlayerState.AI_RL]
controlseq = ['Left', 'Right', 'Up', 'Down', 'Fire']

RLagent = RL_Agent()

class Game(object):
    def __init__(self):
        self.close = False
        self.winner = None

        self.players = [Plane(0, vec(100, Bottom_Margin)), Plane(1, vec(540, Bottom_Margin))]
        self.players[0].enemy = self.players[1]
        self.players[1].enemy = self.players[0]

    def event_loop(self):

        for p in self.players:
            if p.controller == PlayerState.AI_RL:
                output_key = RLagent.think(p)

                for i in range(output_key):
                    p.key[controlseq[i]] = output_key[i]

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

    def run(self):
        while not self.winner == None:
            self.event_loop()
            self.update()

        print(self.winner, 'wins!')


def main(object):
    game = Game()
    game.run()
    sys.exit()

'''
Check if main.py is the called program.
'''
if __name__ == '__main__':
    main()


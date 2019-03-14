# import os

from enum import Enum

# dirname = os.path.dirname(__file__)

class PlayerState(Enum):
    Human = 0
    AI_RL = 1

playerlist = [PlayerState.Human, PlayerState.Human]

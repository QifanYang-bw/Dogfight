from enum import Enum

class PlayerState(Enum):
    Human = 0
    AI_RL = 1
    AI_Random = 2
    AI_Hardcoded = 3

global playerlist

playerlist = [PlayerState.Human, PlayerState.AI_RL]
from enum import Enum

class PlayerState(Enum):
    Human = 0
    AI_RL = 1
    AI_Random = 2
    AI_Hardcoded = 3

playerlist = [PlayerState.Human, PlayerState.AI_RL]
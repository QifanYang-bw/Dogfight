# from const import *
# from core import *
# from DeepQNetwork import DeepQNetwork
from envi import *

# import itertools
import random
import numpy as np

class RL_Agent(object):
    """DeepQAI object that controls the move of AI.

    Attributes:
        __plane: Plane object.
        __enemy: Opposite plane object.
    """

    def __init__(self):
        self.__plane = None
        self.__enemy = None

        # self.policy_net = DeepQNetwork([64, 256, 256, 64, 64], Network_Learning_Rate)

        # # Variables for Q learning
        # self.q_lr = Q_Learning_Rate
        # self.discount_factor = Discount_Factor

        self.play_history = []
        self.wins = 0

    def think(self, plane, epsilon = 0, log = False):
        """ The main mathod for decision making."""

        epsilon = 1

        self.__plane = plane
        self.__enemy = plane.enemy

        input_state = []

        for _ in [self.__plane, self.__enemy]:
            _state = [_.heading, _.pos.x, _.pos.y, _.speed, _.rotation, _.accel.x, _.accel.y, \
                      _.missile_cooldown, _.hp]
            input_state.append(_state)

        output_state = None # 5 bool elements

        # epsilon greedy to pick random move
        if np.random.random() < epsilon:
            output_state = self.random_move(input_state)
        else:
            output_state = self.network_based_move(input_state)

        # if log:
        #     input_state = np.apply_along_axis(
        #         lambda x: int((x == self.__currentState and 1) or (x != BoardState.Empty and -1)),
        #         1,
        #         np.asarray(self.__reversi.get_chessMap()).reshape((64, 1))
        #     ).reshape((64, 1))
        #     self.play_history.append((np.copy(input_state), output_row * 8 + output_col))


        return output_state

    def random_move(self, *args):
        output_state = []
        for i in range(5):
            output_state.append(random.random() >= .5)

        return output_state

    # def network_based_move(self, condition):
        # input_state = np.apply_along_axis(
        #     lambda x: int((x == self.__currentState and 1) or (x != BoardState.Empty and -1)),
        #     1,
        #     np.asarray(condition.get_chessMap()).reshape((64, 1))
        # ).reshape((64, 1))

        # # Retrieve output from neural network
        # out = self.policy_net.getOutput(input_state)

        # pos_seq = [(v, i) for i, v in enumerate(out)]
        # pos_seq.sort(key = lambda x: x[0], reverse = True)

        # ifmoved = False
        # while not ifmoved and pos_seq:
        #     pos_1D = pos_seq.pop()[1]

        #     pos = pos_1D // 8, pos_1D % 8

        #     ifmoved = condition.validity_test(
        #         pos[0],
        #         pos[1],
        #         self.__currentState,
        #         self.__opponentState
        #     )[0]

        # if ifmoved:
        #     return pos
        # else:
        #     raise ValueError('No possible moves available')

    # def updateWeights(self, final_score):
        # i = 0
        # state, action = self.play_history[i]

        # q = self.policy_net.getOutput(state)
        # n_play_history = len(self.play_history)
        # while i < n_play_history:
        #     i += 1

        #     if i == n_play_history:
        #         q[action] += self.q_lr * (final_score - q[action])

        #     else:
        #         state_, action_ = self.play_history[i]
        #         q_ = self.policy_net.getOutput(state_)
        #         q[action] += self.q_lr * (self.discount_factor * np.max(q_) - q[action])

        #     self.policy_net.backProp(state, self.policy_net.mkVec(q))

        #     if i != n_play_history:
        #         action, q = action_, q_

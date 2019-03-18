# import os

from enum import Enum
import numpy as np

WIDTH = 640
HEIGHT = 320

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

Top_Margin = 1;
Left_Margin = 0
Right_Margin = 640
Bottom_Margin = 310
Real_Top_Margin = 0
Real_Bottom_Margin = 320

Resize_Factor = 0.72
Plane_Width = 42
Plane_Height = 16

Control_Stearing = 17
Power_Stage = 0.05
Min_Stall = 0

Max_Power = 4

class PlayerState(Enum):
    Human = 0
    AI_RL = 1
    AI_Random = 2

#controlseq = ['Left', 'Right', 'Up', 'Down', 'Fire']

Input_Dim = 15
Output_Dim = 3

# net_output_match = [[2], [2, 0], [2, 1],
# 					[] , [   0], [   1],
# 					[3], [3, 0], [3, 1],
# 					[2, 4], [2, 0, 4], [2, 1, 4],
# 					[   4], [   0, 4], [   1, 4],
# 					[3, 4], [3, 0, 4], [3, 1, 4]]

net_output_match = [[2, 4], [2, 0, 4], [2, 1, 4]]

net_output_bool = [[False for _ in range(5)] for __ in range(Output_Dim)]

for i in range(Output_Dim):
	for j in net_output_match[i]:
		net_output_bool[i][j] = True

net_random_prior = [1] * Output_Dim #[10, 10, 10, 1, 1, 1, 1, 1, 1, 10, 10, 10, 1, 1, 1, 1, 1, 1]
net_random_prior = list(np.array(net_random_prior) / sum(net_random_prior))

# Upper and Lower limit of data, for normalization
#                 [_.heading, _.pos.x, _.pos.y, _.speed, _.rotation, _.accel.x, _.accel.y, _.hp]
state_upper_bar = [1, Right_Margin,     Top_Margin,    4, 360, 2,  2, 10]
state_lower_bar = [0, Left_Margin - 30, Bottom_Margin, 0, 0,   0,  0, 0]
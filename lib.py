import math
# import os

epsilon = 1e-6

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


class vec(object):
    def __init__(self, *args):
        if len(args) > 0:
            self.x = float(args[0])
            self.y = float(args[1])
        else:
            self.x = .0
            self.y = .0

    def __repr__(self):
        return '({0:.2f}, {1:.2f})'.format(self.x, self.y)

    def __add__(self, vec2):
        return vec(self.x + vec2.x, self.y + vec2.y)

    def __sub__(self, vec2):
        return vec(self.x - vec2.x, self.y - vec2.y)

    def dist(self):
        return (self.x * self.x + self.y * self.y)**0.5

    def copy(self):
        return vec(self.x, self.y)

    def tocp(self):
        return (self.x, self.y)

box_side_coord = [vec(Left_Margin, Real_Bottom_Margin), vec(Left_Margin, Real_Top_Margin),
                  vec(Right_Margin, Real_Top_Margin), vec(Right_Margin, Real_Bottom_Margin)]

# Source: https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
# Returns 1 if the lines intersect, otherwise 0. In addition, if the lines 
# intersect the intersection point may be stored in the floats i.x and i.y.
def cross_product(p, q):
    return p.x * q.y - p.y * q.x

def seg_intersect(p0, p1, p2, p3, outCoord = False):

    s1 = p1 - p0
    s2 = p3 - p2
    s3 = p0 - p2

    collisionFlag = False

    d = cross_product(s1, s2)
    coord = None

    if abs(d) > epsilon:

        s = cross_product(s1, s3)

        if (s <= 0 and d < 0 and s >= d) or (s >= 0 and d > 0 and s <= d):

            t = cross_product(s2, s3)

            if (t <= 0 and d < 0 and t > d) or (t >= 0 and d > 0 and t < d):
                collisionFlag = True
                if outCoord:
                    t = t / d
                    coord = vec(p0.x + t * d.x, p0.y + t * d.y)

    if not coord:
        return collisionFlag
    else:
        return coord

'''
p0, p1, p2, p3 must be in order.
'''
def box_intersect(q0, q1, p0, p1, p2, p3):
    if seg_intersect(q0, q1, p0, p1) or seg_intersect(q0, q1, p1, p2) or \
       seg_intersect(q0, q1, p2, p3) or seg_intersect(q0, q1, p3, p0):
        return True
    else:
        return False

def hitbox_check(center1, rotate1, center2, rotate2, hitbox_width = Plane_Width, hitbox_height = Plane_Height):
    edge_num = int((rotate1 + 45) // 90) % 4
    # edge = vec(box_side_coord[edge_num], box_side_coord[(edge_num + 1) % 4])
    # print(edge_num, box_side_coord[edge_num], (center1.x - box_side_coord[edge_num].x))

    if edge_num & 1 == 1:
        collide_x = center1.x - (center1.y - box_side_coord[edge_num].y) / math.tan(rotate1 / 180 * math.pi)
        collide = vec(collide_x, box_side_coord[edge_num].y)
    else:
        collide_y = center1.y - (center1.x - box_side_coord[edge_num].x) * math.tan(rotate1 / 180 * math.pi)
        collide = vec(box_side_coord[edge_num].x, collide_y)

    # print(collide)

    p2 = center1
    p3 = collide

    hitbox_width = hitbox_width // 2
    hitbox_height = hitbox_height // 2

    rot2_rad = (rotate2) / 180 * math.pi

    flag = False

    for _ in range(4):
        p0 = vec(hitbox_width  * ((_ == 2 or _ == 3) * 2 - 1), 
                 hitbox_height * ((_ == 3 or _ == 0) * 2 - 1))

        p0 = vec(math.cos(rot2_rad) * p0.x - math.sin(rot2_rad) * p0.y + center2.x,
                 math.sin(rot2_rad) * p0.x + math.cos(rot2_rad) * p0.y + center2.y)

        p1 = vec(hitbox_width  * ((_ == 1 or _ == 2) * 2 - 1), 
                 hitbox_height * ((_ == 2 or _ == 3) * 2 - 1))

        p1 = vec(math.cos(rot2_rad) * p1.x - math.sin(rot2_rad) * p1.y + center2.x,
                 math.sin(rot2_rad) * p1.x + math.cos(rot2_rad) * p1.y + center2.y)

        # print(p0, p1, p2, p3)

        if seg_intersect(p0, p1, p2, p3):
            flag = True
            break

    return (flag, p3)

# print(hitbox_check(vec(100, 100), 180, vec(400, 120), 0, 42, 16))

from const import *
from envi import *

import random

class Agent_Hardcoded(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.lower = 250
        self.upper = 80

    def act(self, cur):

        def rand01(thres):
            return int(random.random() <= thres)

        def facingright(cur):

            if cur.rotation >= 90 and cur.rotation < 270:
                return True
            else:
                return False

        def stat(angle, facing_right):

            if not facing_right:

                angle += 180
                if angle > 360: angle -= 360

                mark = -1
            else:
                mark = 1

            if angle >= 155 and angle < 205:
                ans = 0
            elif angle >= 90 and angle < 155:
                ans = mark * 1
            elif angle >= 205 and angle < 270:
                ans = mark * -1

            return ans


        def taking_off(cur):
            ans = [False, False, True, False, True]

            facing_right = facingright(cur)

            st = stat(cur.rotation, facing_right)


            if st == 0 or st == -1:
                turn = 1
            elif st == 1:
                turn = 0

            if facing_right: turn = 1 - turn

            ans[turn] = True
            return ans

        def heading_up(cur):
            ans = [False, False, True, False, True]

            facing_right = facingright(cur)

            st = stat(cur.rotation, facing_right)


            if st == 0 or st == -1:
                turn = rand01(0.75)
            elif st == 1:
                turn = rand01(0.25)

            if facing_right: turn = 1 - turn

            ans[turn] = True
            return ans

        def heading_down(cur):
            ans = [False, False, True, False, True]

            facing_right = facingright(cur)
            st = stat(cur.rotation, facing_right)

            if st == -1:
                turn = rand01(0.75)
            elif st == 0 or st == 1:
                turn = rand01(0.25)

            if facing_right: turn = 1 - turn

            ans[turn] = True
            return ans


        def adjust(cur):
            ans = [False, False, True, False, True]

            facing_right = facingright(cur)
            st = stat(cur.rotation, facing_right)

            if st == 0:
                turn = rand01(0.5)
            elif st == 1:
                turn = rand01(0.25)
            elif st == -1:
                turn = rand01(0.75)

            if facing_right: turn = 1 - turn

            ans[turn] = True
            return ans

        #controlseq : ['Left', 'Right', 'Up', 'Down', 'Fire']

        if cur.pos.y > Bottom_Margin - 10:
            return taking_off(cur)
        if cur.pos.y > self.lower:
            return heading_up(cur)
        elif cur.pos.y < self.upper:
            return heading_down(cur)
        else:
            return adjust(cur)

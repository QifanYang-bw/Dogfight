import math
import random
from lib import *

Initial_HP = 20
Damage_per_hit = 2

KEYPRESS_CODE = ['Up', 'Down', 'Left', 'Right', 'Fire'] #Missile

class Plane(object):

    def __init__(self, controller, heading, init_pos, mute = False):

        self.heading = heading # 0 -> right, 1 -> left

        self.controller = controller
        
        self.enemy = None

        self.mute = mute

        # ------- Flight Settings -------

        self.reset(init_pos)

    def random_state(self):

        def __srand(**kwargs):
            if 'match' in kwargs:
                upper = state_upper_bar[kwargs['match']]
                lower = state_lower_bar[kwargs['match']]
            else:
                upper = kwargs['upper']
                lower = kwargs['lower']

            ans = lower + random.random() * (upper - lower)

            return ans

#       [_.heading, _.pos.x, _.pos.y, _.speed, _.rotation, _.accel.x, _.accel.y, _.missile_cooldown, _.hp]
        rnd_pos = vec(__srand(match = 1), __srand(match = 2))

        self.reset(rnd_pos)

        self.speed = __srand(match = 3)
        self.rotation = __srand(match = 4)

        self.accel = vec(__srand(match = 5), __srand(match = 6))
        self.engine_power = __srand(lower = 0, upper = 4)

        self.missile_cooldown = 0

        self.hp = __srand(lower = 2, upper = 4)

    def reset(self, init_pos):

        self.pos = init_pos
        self.accel = vec(0, 0)

        self.engine_power = 0
        if self.heading == 0:
            self.rotation = 180
        else:
            self.rotation = 0

        self._stall = Min_Stall
        self.speed = 0

        self.key = dict()
        for i in KEYPRESS_CODE:
            self.key[i] = False

        # ------- Enemy and Fire Settings -------

        self.hp = Initial_HP
        self.crashed = False
        self.firing = False
        self.on_ground = True

        self.beam_track = [0, None]

        self.missile_cooldown = 105

        # ------- Reward Settings -------

        # self.delta_speed = 0
        self.damage_caused = 0
        self.damage_received = 0

    def __repr__(self):
        return 'Plane ' + str(self.heading + 1) + ' at ' + str(self.pos)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self

    def fly(self):
        # Missile Cooldown

        if self.missile_cooldown > 0:
            self.missile_cooldown -= 1

        # -----------------------------------------------------------------------------------------------
        # Initialize: yaccel, xaccel, yspeed, xspeed
        # ytop_margin_force, booster_speed

        if self.rotation < 0: self.rotation += 360
        if self.rotation > 360: self.rotation -= 360

        # -----------------------------------------------------------------------------------------------
        # the x and y here are relative to the plane
        # Note that the direction of x heads down, the direction of y head right

        xspeed = self.speed * math.cos(self.rotation / 180 * math.pi) # * self._xscale / 100
        yspeed = self.speed * math.sin(self.rotation / 180 * math.pi) # * self._xscale / 100
        xaccel = self.engine_power * math.cos(self.rotation / 180 * math.pi) / 2 # * self._xscale / 200
        yaccel = self.engine_power * math.sin(self.rotation / 180 * math.pi) / 2 # * self._xscale / 200

        new_pos = self.pos - vec(xspeed + xaccel, yspeed + yaccel)
        new_accel = vec(xaccel, yaccel)

        if new_pos.y < Top_Margin + 30:
            ytop_margin_force = -(Top_Margin + 30 - new_pos.y) / 10
        else:
            ytop_margin_force = 0
        new_pos.y -= ytop_margin_force

        # -----------------------------------------------------------------------------------------------
        # Stall Force Check - Whether the vertical speed of the plane decreases

        if abs(xspeed + xaccel) < 3.7:
            if new_pos.y <= Bottom_Margin - 3:
                new_stall = 0.03 + self._stall * 1.001
            else:
                new_stall = 1.5
        else:
            new_stall = max(self._stall - 0.3, Min_Stall)

        if new_stall > 1:
            new_pos.y += new_stall

        if new_pos.y <= Bottom_Margin:
            booster_speed = (2 * xaccel * xaccel)**0.5
        else:
            booster_speed = new_accel.dist()

        # -----------------------------------------------------------------------------------------------
        if new_pos.x < Left_Margin - 30:
            new_pos.x = Right_Margin

        if new_pos.x > Right_Margin:
            new_pos.x = Left_Margin - 30

        # -----------------------------------------------------------------------------------------------
        # Landing Check

        self.status_change = 0

        # Easter Egg: the 0.75 here related to possible bumps of the plane
        if new_pos.y >= Bottom_Margin:
            cur_rotat = self.rotation
            vertical_force = (yaccel + yspeed + ytop_margin_force + self._stall) * math.sin(self.rotation / 180 * math.pi)
            
            if cur_rotat >= 90 and cur_rotat < 270:
                self.rotation = 180
            else:
                self.rotation = 0

            if self.heading == 1 and (cur_rotat > 15 and cur_rotat < 345):
                vertical_force = 50
            if self.heading == 0 and (cur_rotat < 165 or cur_rotat > 195):
                vertical_force = 50

            new_pos.y = Bottom_Margin
            if vertical_force > 0.46:
                # self.damage = max_damage
                # destructor(this)
                new_accel = vec(0, 0)
                self.speed = 0
                self.crashed = True

                if not self.mute:
                    print('\nPlayer', self.heading + 1, 'Crashed!\n')

            self.on_ground = True

        else:

            self.on_ground = False

        self.altitude_change = abs(self.pos.y - new_pos.y) / 20

        self.pos = new_pos
        self.accel = new_accel

        new_speed = (50 * self.speed / 51) + (booster_speed / 51)
        # self.delta_speed = new_speed - self.speed
        self.speed = new_speed

        self._stall = new_stall

        if self.firing:
            self.firing = False
            self.beam_fire()
        else:
            self.beam_fire_clearup()

    def frame_control(self):
        if self.crashed or self.hp <= 0:
            return

        if self.engine_power > 2:
            self.engine_power -= Power_Stage

        stearing_accel = self.accel.dist() / 9;
        if self.key['Left']:# and self._y < (Bottom_Margin - 2):
            self.rotation = self.rotation - (Control_Stearing * stearing_accel)
        if self.key['Right']:
            self.rotation = self.rotation + (Control_Stearing * stearing_accel)

        if self.key['Up'] and self.engine_power < Max_Power:
            self.engine_power = self.engine_power + (Power_Stage * 3)
        if self.key['Down'] and self.engine_power > 2:
            self.engine_power = self.engine_power - Power_Stage

        if self.key['Fire'] and self.missile_cooldown == 0:
            if not self.on_ground:
                self.firing = True

        if self.on_ground and self.speed < 1.25:
            self.missile_cooldown = max(self.missile_cooldown, 5)

    def beam_fire(self):
        self.missile_cooldown = 22

        res = hitbox_check(self.pos, self.rotation, self.enemy.pos, self.enemy.rotation)

        if res[0]:
            self.enemy.hp -= Damage_per_hit
            self.damage_caused = Damage_per_hit
            self.enemy.damage_received = Damage_per_hit

            if not self.mute:

                print('Player', self.heading + 1, 'hit Player',  self.enemy.heading + 1, 'for', self.damage_caused, 'damage!')

                if self.enemy.hp <= 0:
                    print('\nPlayer', self.enemy.heading + 1, 'fainted!\n')

        self.beam_track = [8, (res[1].x, res[1].y)]


    def beam_fire_clearup(self):
        self.damage_caused = 0
        self.enemy.damage_received = 0

    def score(self):
        ans = 0
        targeting = self.pos.y < Bottom_Margin - 5 and hitbox_check(self.pos, self.rotation, self.enemy.pos, self.enemy.rotation)[0]

        if self.crashed:
            ans -= self.hp
        if self.pos.y < Bottom_Margin - 5:
            ans += 1
        if targeting:
            ans += 1
        if self.enemy.hp <= 0:
            ans += 1
        ans += self.damage_caused - self.damage_received
        return ans



import math
import random
from lib import *

Initial_HP = 5
Damage_per_hit = 1

KEYPRESS_CODE = ['Up', 'Down', 'Left', 'Right', 'Fire'] #Missile

class Plane(object):

    def __init__(self, controller, heading, init_pos):

        self.heading = heading # 0 -> right, 1 -> left

        self.controller = controller
        
        self.enemy = None

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

        self.hp = int(__srand(upper = 5, lower = 1))

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

        self.delta_speed = 0
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

        # if (self._name == "f1"):
        #     self_control(this)
        # else:
        #     enemy_control(this)
        #    if ((self.damage > rep_damage) && (!repire_on)) {
        #        repire_box_activated()

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

            if self.heading == 1 and (cur_rotat > 10 and cur_rotat < 355):
                vertical_force = 50
            if self.heading == 0 and (cur_rotat < 170 or cur_rotat > 185):
                vertical_force = 50


            # if self.heading == 1:
            #     print(new_pos, 'vf', '{0:.4f}'.format(vertical_force))


            new_pos.y = Bottom_Margin
            if vertical_force > 0.46:
                # self.damage = max_damage
                # destructor(this)
                new_accel = vec(0, 0)
                self.speed = 0
                self.crashed = True
                print('\nPlayer', self.heading + 1, 'Crashed!\n')

            # if not self.on_ground:
            #     self.status_change = 1

            self.on_ground = True

        else:
            # if self.on_ground:
            #     self.status_change = 1

            self.on_ground = False

        self.altitude_change = abs(self.pos.y - new_pos.y) / 20

        self.pos = new_pos
        self.accel = new_accel

        new_speed = (50 * self.speed / 51) + (booster_speed / 51)
        self.delta_speed = new_speed - self.speed
        self.speed = new_speed

        self._stall = new_stall

        if self.firing:
            self.firing = False
            self.beam_fire()
        else:
            self.beam_fire_clearup()

        # if self.heading == 1:
        #     print('Pos', self.pos, ' Accel', self.accel, ' Speed {:.3f}'.format(self.speed))

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
        # print(self.speed)
            # if self.heading == 0: print('yes', self.pos)

    def beam_fire(self):
        self.missile_cooldown = 22

        res = hitbox_check(self.pos, self.rotation, self.enemy.pos, self.enemy.rotation)

        if res[0]:
            self.enemy.hp -= Damage_per_hit
            self.damage_caused = Damage_per_hit
            self.enemy.damage_received = Damage_per_hit

            print('Player', self.heading + 1, 'hit Player',  self.enemy.heading + 1, 'for', self.damage_caused, 'damage!')

            if self.enemy.hp <= 0:
                print('\nPlayer', self.enemy.heading + 1, 'fainted!\n')

        self.beam_track = [8, (res[1].x, res[1].y)]

        # print(self.hp, self.enemy.hp)

    def beam_fire_clearup(self):
        self.damage_caused = 0
        self.enemy.damage_received = 0

    def score(self):
        # print(self.altitude_change)
        if self.crashed:
            return -1
        elif self.enemy.hp <= 0:
            return 1
        elif self.damage_caused - self.damage_received != 0:
            return self.damage_caused - self.damage_received
        else:
            return self.delta_speed
            # return self.damage_caused - self.enemy.damage_received + self.altitude_change

    #     if self.crashed or self.hp <= 0:
    #         return 0.
    #     elif self.enemy.hp == 0:
    #         return 1.
    #     else:
    #         return self.hp * 0.005 + (100 - self.enemy.hp) * 0.005



    #     if (Key.isDown(86)):
    #         if ((getTimer() - missle_lasttime_2nd) >= missle_timeout):
    #             missle_lasttime_2nd = getTimer()
    #             fire_missle(self)
    #     if (Key.isDown(67)):
    #         if ((getTimer() - gun_lasttime_2nd) >= gun_timeout)
    #             if (self.gun_counter > 5):
    #                 gun_lasttime_2nd = getTimer()
    #             fire_gun(self)
    #         else:
    #             self.gun_counter = 0

    
    # function fire_gun(my) {
    #     my.gun_counter = my.gun_counter + 2;
    #     var _local6 = my._parent[(("gun_" + my._name) + "_") + (my.gun_counter - 2)].range;
    #     var _local5 = (("gun_" + my._name) + "_") + my.gun_counter;
    #     my._parent.attachMovie("gunfire", _local5, my.gun_counter + 200);
    #     my._parent[_local5].play();
    #     my._parent[_local5]._x = my._x;
    #     my._parent[_local5]._y = my._y;
    #     my._parent[_local5].rotation = my.rotation;
    #     my._parent[_local5].range = range;
    #     if (play_sound) {
    #         gun_shoot.start(0, 4);
    #     }
    #     my._parent[_local5].onEnterFrame = function () {
    #         var _local3;
    #         this._x = this._x - (gun_speed * math.cos((this.rotation * math.pi) / 180));
    #         this._y = this._y - (gun_speed * math.sin((this.rotation * math.pi) / 180));
    #         for (_local3 in _root.flayers) {
    #             if (((_root.flayers[_local3].hitTest(this) && (_local3 != my._name)) && ((_local3 == "f1") || (_local3 == "f4"))) && (this.range < range)) {
    #                 _root.flayers[_local3].attachMovie("explosion", "blow", 1);
    #                 var cur_rotat = new Sound(_root.flayers[_local3]);
    #                 cur_rotat.attachSound("_sfxRicochet");
    #                 cur_rotat.volume(75);
    #                 if (play_sound) {
    #                     cur_rotat.start(0, 1);
    #                 }
    #                 _root.flayers[_local3].blow._xscale = (_root.flayers[_local3].blow._yscale = 100);
    #                 _root.flayers[_local3].blow.onEnterFrame = function () {
    #                     if (this._currentframe == this._totalframes) {
    #                         this._parent.createEmptyMovieClip("destruct", this.getDepth());
    #                     }
    #                 };
    #                 _root.flayers[_local3].damage++;
    #                 score_counter("gunshoot", _root.flayers[_local3]);
    #                 if (_root.flayers[_local3].damage > max_damage) {
    #                     destructor(_root.flayers[_local3]);
    #                 }
    #                 break;
    #             }
    #         }
    #         if ((this._y > Bottom_Margin) || ((this.range--) <= 0)) {
    #             this._parent.createEmptyMovieClip("destruct", this.getDepth());
    #         }
    #     };
    # }
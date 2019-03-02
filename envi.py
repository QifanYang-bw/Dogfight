import math
from lib import *

MIN_STALL = 0
KEYPRESS_CODE = ['Up', 'Down', 'Left', 'Right', 'Fire'] #Missile

class Plane(object):

    def __init__(self, heading, init_pos):
        self.heading = heading # 0 -> right, 1 -> left

        self.pos = init_pos
        self.accel = vec(0, 0)

        self.engine_power = 0
        if self.heading == 0:
            self.rotation = 180
        else:
            self.rotation = 0

        self._stall = MIN_STALL
        self.speed = 0

        self.key = dict()
        for i in KEYPRESS_CODE:
            self.key[i] = False

        self.hp = 100
        self.crashed = False

        self.beam_track = [0, None]

        self.enemy = None
        self.missile_cooldown = 105


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
                self._stall += 0.03 + self._stall * 0.001
            else:
                self._stall = 1.5
        else:
            self._stall = max(self._stall - 0.3, MIN_STALL)

        if self._stall > 1:
            new_pos.y += self._stall

        if new_pos.y < Bottom_Margin:
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

        # Crash Landing check
        if self.rotation < 0:
            self.rotation += 360

        # -----------------------------------------------------------------------------------------------
        # Landing Check
        if new_pos.y > Bottom_Margin + 1:
            cur_rotat = self.rotation
            vertical_force = (yaccel + yspeed + ytop_margin_force + self._stall) * math.sin(self.rotation / 180 * math.pi)
            
            if cur_rotat >= 90 and cur_rotat < 270:
                self.rotation = 180
            else:
                self.rotation = 0

            if self.heading == 1 and self.rotation == 180 and (cur_rotat > 15 or cur_rotat < 355): #need edit!
                vertical_force = 50
            if self.heading == 0 and self.rotation == 0 and (cur_rotat < 165 or cur_rotat > 185):
                vertical_force = 50


            # if self.heading == 1:
                # print(new_pos, 'vf', '{0:.4f}'.format(vertical_force))


            new_pos.y = Bottom_Margin
            if vertical_force > 0.46:
                # self.damage = max_damage
                # destructor(this)
                new_accel = vec(0, 0)
                self.speed = 0
                self.crashed = True
                print('\nBOOM!\n')

        self.pos = new_pos
        self.accel = new_accel
        self.speed = ((50 * self.speed) / 51) + (booster_speed / 51)

        # if self.heading in {0, 1}:
            # print('#{0}'.format(self.heading), 'Rot: {0:.2f} '.format(self.rotation), 'Pos:', self.pos)

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
            self.beam_fire()

    def beam_fire(self):
        self.missile_cooldown = 75

        print(self.rotation)

        res = hitbox_check(self.pos, self.rotation, self.enemy.pos, self.enemy.rotation)

        if res[0]:
            self.enemy.hp -= 50

        self.beam_track = [10, (res[1].x, res[1].y)]

        print(self.hp, self.enemy.hp)





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
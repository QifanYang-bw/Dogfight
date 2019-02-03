
//----------------------------------------------------------------------
//Frame 10
//----------------------------------------------------------------------
    function pause_game(item, pause_bar, depth) {
        if (depth > 5) {
            return(undefined);
        }
        _root.pause_block.gotoAndStop(3);
        var _local2;
        for (_local2 in item) {
            pause_bar[_local2] = new Object();
            if ((item[_local2].onEnterFrame != null) || (item[_local2].onEnterFrame != undefined)) {
                pause_bar[_local2].fx = item[_local2].onEnterFrame;
                item[_local2].onEnterFrame = null;
            }
            pause_game(item[_local2], pause_bar[_local2], depth + 1);
        }
        _root.parabox._visible = 0;
    }
    function continue_game(item, pause_bar) {
        var _local2;
        _root.pause_block.gotoAndStop(2);
        for (_local2 in pause_bar) {
            if (pause_bar[_local2].fx != null) {
                item[_local2].onEnterFrame = pause_bar[_local2].fx;
            }
            continue_game(item[_local2], pause_bar[_local2]);
        }
        _root.parabox._visible = 1;
    }
    function cancel_game() {
        stopAllSounds();
        _root.flayers.removeMovieClip();
        _root.shadows.removeMovieClip();
        _root.smokers.removeMovieClip();
        _root.zeppelin._visible = false;
        _root.game_over_pad.createEmptyMovieClip("destruct", 11);
        _root.last_word._visible = false;
        play_control._visible = true;
        game_play_f1._visible = false;
        game_play_f4._visible = false;
        _root.pause_block.gotoAndStop(1);
        _root.cover_sound.start(0, 9999);
    }
    gameID = 2;
    pause_bar = new Object();
    pause_block.gotoAndStop(1);
    last_word._visible = false;
    // unexpected jump
    // unexpected jump

    function init_score() {
        _root.createEmptyMovieClip("destruct", parabox.getDepth());
        _root.createEmptyMovieClip("destruct", repire_box.getDepth());
        game_play_f1.score.text = 0;
        score_f1 = 0;
        game_play_f1.gunned.text = 0;
        gunned_f1 = 0;
        game_play_f1.raiting.text = rating_list[0];
        damager_f1.damage_scaler._xscale = 0;
        game_play_f4._visible = multyplay;
        if (!multyplay) {
            game_play_f4.name._visible = 1;
            game_play_f1.name._visible = 1;
            game_play_f4.raiting._visible = 1;
            game_play_f1.raiting._visible = 1;
            game_play_f4.name.text = "Enemy:";
            game_play_f1.name.text = "Rank:";
            damager_f1.hp.text = "Player:";
            damager_f4.hp.text = "Enemy:";
        } else {
            game_play_f4.name._visible = 1;
            game_play_f1.name._visible = 1;
            game_play_f4.raiting._visible = 1;
            game_play_f1.raiting._visible = 1;
            damager_f1.hp.text = "Player1:";
            damager_f4.hp.text = "Player2:";
            game_play_f4.name.text = "Won:";
            game_play_f1.name.text = "Won:";
            game_play_f4.raiting.text = won_f4;
            game_play_f1.raiting.text = won_f1;
        }
        game_play_f4.score.text = 0;
        score_f4 = 0;
        game_play_f4.gunned.text = 0;
        gunned_f4 = 0;
        damager_f4.damage_scaler._xscale = 0;
    }
    function update_damage_counter() {
        damager_f1.damage_scaler._xscale = _root.flayers.f1.damage;
        damager_f4.damage_scaler._xscale = _root.flayers.f4.damage;
    }
    function score_counter(action, player) {
        var _local1;
        if (player._name == "f4") {
            if (action == "gunshoot") {
                score_f1 = score_f1 + 20;
            }
            if (action == "misslesoot") {
                score_f1 = score_f1 + 50;
            }
            if ((action == "kill") && (!player.destroyed)) {
                score_f1 = score_f1 + 100;
                gunned_f1++;
                player.destroyed = true;
                _local1 = 0;
                while (_local1 < rating_kils.length) {
                    if (rating_kils[_local1] > gunned_f1) {
                        break;
                    }
                    _local1++;
                }
                if (!multiplay) {
                    game_play_f1.raiting.text = rating_list[_local1];
                }
            }
            game_play_f1.score.text = score_f1;
            game_play_f1.gunned.text = gunned_f1;
            damager_f4.damage_scaler._xscale = player.damage;
        } else {
            if (action == "gunshoot") {
                score_f4 = score_f4 + 3;
            }
            if (action == "misslesoot") {
                score_f4 = score_f4 + 4;
            }
            if ((action == "kill") && (!player.destroyed)) {
                score_f4 = score_f4 + 5;
                gunned_f4++;
                player.destroyed = true;
                _local1 = 0;
                while (_local1 < rating_kils.length) {
                    if (rating_kils[_local1] > gunned_f4) {
                        break;
                    }
                    _local1++;
                }
            }
            game_play_f4.score.text = score_f4;
            game_play_f4.gunned.text = gunned_f4;
            damager_f1.damage_scaler._xscale = player.damage;
        }
    }
    // unexpected jump
    // unexpected jump

    function end_game() {
        _root.createEmptyMovieClip("flayers", 100);
        _root.createEmptyMovieClip("smokers", 101);
        _root.createEmptyMovieClip("shadows", 102);
        _root.createEmptyMovieClip("destruct", parabox.getDepth());
        _root.createEmptyMovieClip("destruct", repire_box.getDepth());
        game_play_f1._visible = false;
        game_play_f4._visible = false;
        zeppelin._visible = false;
        gameover();
    }
    function start_game() {
        _root.createEmptyMovieClip("flayers", 100);
        _root.createEmptyMovieClip("smokers", 101);
        _root.createEmptyMovieClip("shadows", 102);
        _root.attachMovie("zeppelin", "zeppelin", 23);
        game_play_f1._visible = true;
        game_play_f4._visible = true;
        damager_f1._visible = true;
        damager_f4._visible = true;
        zeppelin._visible = true;
        zeppelin._x = right_margin;
        repire_on = false;
        zeppelin._y = 30;
        zeppelin.onEnterFrame = function () {
            this._x = this._x - 0.4;
            if (this._x < -120) {
                this._visible = 0;
            }
        };
        start_left();
        start_right();
        init_score();
        for (alef in flayers) {
            flayers[alef].onEnterFrame = fly;
            flayers[alef].engine_power = 0;
        }
        if (restart) {
            multyplayStart();
        }
    }
    function start_left() {
        flayers.attachMovie("f3", "f1", 100);
        flayers.f1._y = bottom_margin + 10;
        flayers.f1._x = 50;
        flayers.f1._rotation = 168;
        flayers.f1.direct = (Math.PI/2);
        flayers.f1.speed = 0;
        flayers.f1.damage = 0;
        flayers.f1.gun_counter = 1;
        flayers.f1.missle_counter = 1;
        damager_f1.damage_scaler._xscale = 0;
        flayers.f1.gotoAndStop(flayers.f1._totalframes);
        _root.shadows.attachMovie("shadow", "shadow_f1", 0);
        _root.shadows.shadow_f1._y = bottom_margin;
        _root.shadows.shadow_f1.onEnterFrame = function () {
            this._x = _root.flayers.f1._x;
            this._rotation = (-_root.flayers.f1._rotation) + 180;
        };
    }
    function start_right(launch) {
        flayers.attachMovie("f5", "f4", 101);
        flayers.f4.gotoAndStop(1);
        flayers.f4.damage = 0;
        flayers.f4.direct = 0;
        flayers.f4.speed = 0;
        flayers.f4._rotation = 12;
        flayers.f4._y = bottom_margin + 10;
        flayers.f4._x = right_margin - 50;
        damager_f4.damage_scaler._xscale = 0;
        flayers.f4.gun_counter = 0;
        layers.f4.missle_counter = 0;
        opponent_color = new Color(flayers.f4);
        if (launch) {
            flayers.f4.onEnterFrame = fly;
            flayers.f4.engine_power = 0;
        }
        _root.shadows.attachMovie("shadow", "shadow_f4", 1);
        _root.shadows.shadow_f4._xscale = -100;
        _root.shadows.shadow_f4._y = bottom_margin;
        _root.shadows.shadow_f4.onEnterFrame = function () {
            this._x = _root.flayers.f4._x;
            this._rotation = -_root.flayers.f4._rotation;
        };
    }
    function fly() {
        var _local6;
        var _local3;
        var _local10;
        var _local9;
        var _local5;
        var _local8;
        if (this.stall_force == undefined) {
            this.stall_force = min_stall_force;
        }
        if (this.speed == undefined) {
            this.speed = 0;
        }
        _local9 = ((this.speed * Math.cos((this._rotation * Math.PI) / 180)) * this._xscale) / 100;
        this._x = this._x - _local9;
        _local10 = ((this.speed * Math.sin((this._rotation * Math.PI) / 180)) * this._xscale) / 100;
        this._y = this._y - _local10;
        _local3 = ((this.engine_power * Math.cos((this._rotation * Math.PI) / 180)) * this._xscale) / 200;
        this._x = this._x - _local3;
        _local6 = ((this.engine_power * Math.sin((this._rotation * Math.PI) / 180)) * this._xscale) / 200;
        this._y = this._y - _local6;
        if (this._y < (top_margin + 30)) {
            _local5 = (-((top_margin + 30) - this._y)) / 10;
        } else {
            _local5 = 0;
        }
        if (Math.abs(_local9 + _local3) < 3.7) {
            if (this._y <= (bottom_margin - 3)) {
                this.stall_force = this.stall_force + (0.03 + (this.stall_force * 0.001));
            } else {
                this.stall_force = 1.5;
            }
        } else {
            this.stall_force = this.stall_force - 0.3;
        }
        if (this.stall_force < min_stall_force) {
            this.stall_force = min_stall_force;
        }
        if (this.stall_force > 1) {
            this._y = this._y - (_local5 - this.stall_force);
        } else {
            this._y = this._y - _local5;
        }
        if (this._y < bottom_margin) {
            _local8 = Math.sqrt((2 * _local3) * _local3);
        } else {
            _local8 = Math.sqrt((_local3 * _local3) + (_local6 * _local6));
        }
        if (((this._y < bottom_margin) && (play_sound)) && (!on_fly)) {
            launch_sound.stop();
            f_sound.setVolume(16);
            f_sound.start(0, 1000);
            on_fly = true;
        }
        this.dx = _local3;
        this.dy = _local6;
        this.speed_counter.text = this.speed;
        this.speed = ((50 * this.speed) / 51) + (_local8 / 51);
        if (this._name == "f1") {
            my_control(this);
        } else {
            enemy_control(this);
        }
        if ((this.damage > rep_damage) && (!repire_on)) {
            repire_box_activated();
        }
        if (this._x < -30) {
            this._x = right_margin;
        }
        if (this._y > (bottom_margin + 1)) {
            var _local4 = this._rotation;
            var _local7 = (((_local6 + _local10) + _local5) + this.stall_force) * Math.sin((this._rotation * Math.PI) / 180);
            if (this._rotation < 0) {
                _local4 = (this._rotation = this._rotation + 360);
            }
            if ((_local4 >= 90) && (_local4 < 270)) {
                this._rotation = 180;
            } else {
                this._rotation = 0;
            }
            if ((this._name == "f4") && ((this._rotation == 180) || (_local4 > 20))) {
                _local7 = 50;
            }
            if ((this._name == "f1") && ((this._rotation == 0) || (_local4 < 160))) {
                _local7 = 50;
            }
            this._y = bottom_margin;
            if (_local7 > 0.4) {
                _root.smokers.attachMovie("explosion", "blow", 300);
                _root.smokers.blow._x = this._x;
                _root.smokers.blow._y = this._y;
                _root.smokers.blow._xscale = 100;
                _root.smokers.blow._yscale = 100;
                _root.smokers.blow.onEnterFrame = function () {
                    if (this._currentframe == this._totalframes) {
                        this._parent.createEmptyMovieClip("destruct", this.getDepth());
                    }
                };
                this.damage = max_damage;
                destructor(this);
            }
        }
        if (this._x > right_margin) {
            this._x = -30;
        }
        put_smouke(this);
    }
    function put_smouke(my) {
        if (smouke_counter[my._name] != undefined) {
            smouke_counter[my._name]++;
        } else {
            smouke_counter[my._name] = 0;
        }
        if ((smouke_counter[my._name] % 2) != 0) {
            return(undefined);
        }
        var _local4 = (("sm_" + my._name) + "_") + smouke_counter[my._name];
        _root.smokers.attachMovie("smouker", _local4, smouke_depth_counter++);
        _root.smokers[_local4]._x = my._x;
        _root.smokers[_local4]._y = my._y;
        _root.smokers[_local4]._rotation = 90 * Math.random();
        _root.smokers[_local4]._xscale = (_root.smokers[_local4]._yscale = 60);
        _root.smokers[_local4].onEnterFrame = function () {
            this._y--;
            this._xscale = this._xscale + 2;
            this._yscale = this._yscale + 2;
            this._alpha = this._alpha - 4;
            if (this._alpha < 10) {
                this._parent.createEmptyMovieClip("destruct", this.getDepth());
            }
        };
        if (my.damage > (max_damage * 0.8)) {
            s_color = new Color(_root.smokers[_local4]);
            s_color.setRGB(3355443);
        }
        if (my.damage >= max_damage) {
            s_color = new Color(_root.smokers[_local4]);
            s_color.setRGB(0);
        }
        if (smouke_counter[my._name] > 100) {
            smouke_counter[my._name] = 0;
        }
        if (smouke_depth_counter > 300) {
            smouke_depth_counter = 0;
        }
    }
    function my_control(my) {
        var _local2 = my.speed / 9;
        if (my.engine_power > 2) {
            my.engine_power = my.engine_power - power_step;
        }
        if (Key.isDown(38) && (my.engine_power < max_power)) {
            my.engine_power = my.engine_power + (power_step * 3);
        }
        if (Key.isDown(37)) {
            my._rotation = my._rotation - (control_stearing * _local2);
        }
        if (Key.isDown(39) && (my._y < (bottom_margin - 2))) {
            my._rotation = my._rotation + (control_stearing * _local2);
        }
        if (Key.isDown(40) && (my.engine_power > 2)) {
            my.engine_power = my.engine_power - power_step;
        }
        if (Key.isDown(190)) {
            if ((getTimer() - missle_lasttime) >= missle_timeout) {
                missle_lasttime = getTimer();
                fire_missle(my);
            }
        }
        if (Key.isDown(188)) {
            if ((getTimer() - gun_lasttime) >= gun_timeout) {
                if (my.gun_counter > 5) {
                    gun_lasttime = getTimer();
                }
                fire_gun(my);
            } else {
                my.gun_counter = 0;
            }
        }
    }
    function fire_gun(my) {
        my.gun_counter = my.gun_counter + 2;
        var _local6 = my._parent[(("gun_" + my._name) + "_") + (my.gun_counter - 2)].range;
        var _local5 = (("gun_" + my._name) + "_") + my.gun_counter;
        my._parent.attachMovie("gunfire", _local5, my.gun_counter + 200);
        my._parent[_local5].play();
        my._parent[_local5]._x = my._x;
        my._parent[_local5]._y = my._y;
        my._parent[_local5]._rotation = my._rotation;
        my._parent[_local5].range = range;
        if (play_sound) {
            gun_shoot.start(0, 4);
        }
        my._parent[_local5].onEnterFrame = function () {
            var _local3;
            this._x = this._x - (gun_speed * Math.cos((this._rotation * Math.PI) / 180));
            this._y = this._y - (gun_speed * Math.sin((this._rotation * Math.PI) / 180));
            for (_local3 in _root.flayers) {
                if (((_root.flayers[_local3].hitTest(this) && (_local3 != my._name)) && ((_local3 == "f1") || (_local3 == "f4"))) && (this.range < range)) {
                    _root.flayers[_local3].attachMovie("explosion", "blow", 1);
                    var _local4 = new Sound(_root.flayers[_local3]);
                    _local4.attachSound("_sfxRicochet");
                    _local4.volume(75);
                    if (play_sound) {
                        _local4.start(0, 1);
                    }
                    _root.flayers[_local3].blow._xscale = (_root.flayers[_local3].blow._yscale = 100);
                    _root.flayers[_local3].blow.onEnterFrame = function () {
                        if (this._currentframe == this._totalframes) {
                            this._parent.createEmptyMovieClip("destruct", this.getDepth());
                        }
                    };
                    _root.flayers[_local3].damage++;
                    score_counter("gunshoot", _root.flayers[_local3]);
                    if (_root.flayers[_local3].damage > max_damage) {
                        destructor(_root.flayers[_local3]);
                    }
                    break;
                }
            }
            if ((this._y > bottom_margin) || ((this.range--) <= 0)) {
                this._parent.createEmptyMovieClip("destruct", this.getDepth());
            }
        };
    }
    function fire_missle(my) {
        var _local5 = my._parent[(("missle_" + my._name) + "_") + (my.missle_counter - 1)].range;
        if (_local5 != undefined) {
            if (_local5 > (range - 10)) {
                my.missle_counter--;
                return(undefined);
            }
        } else {
            my.missle_counter = my.missle_counter % 2;
        }
        missle_name = "missle_" + my._name;
        if (my._parent[missle_name] != undefined) {
            return(undefined);
        }
        my._parent.attachMovie("missle", missle_name, my.missle_counter + 300);
        if (missle_counter >= 5) {
            missle_counter = 0;
        }
        my._parent[missle_name].m_sound = new Sound(my._parent[missle_name]);
        if (play_sound) {
            my._parent[missle_name].m_sound.attachSound("poletsnaryada.wav");
        }
        my._parent[missle_name].m_sound.start(0, 1);
        my._parent[missle_name]._x = my._x;
        my._parent[missle_name]._y = my._y;
        my._parent[missle_name]._rotation = my._rotation;
        my._parent[missle_name].range = range;
        m_color = new Color(my._parent[missle_name]);
        m_color.setRGB(3355443);
        my._parent[missle_name].onEnterFrame = function () {
            var _local3;
            this._x = this._x - (missle_speed * Math.cos((this._rotation * Math.PI) / 180));
            this._y = this._y - (missle_speed * Math.sin((this._rotation * Math.PI) / 180));
            for (_local3 in _root.flayers) {
                if (((_root.flayers[_local3].hitTest(this) && ((_local3 == "f1") || (_local3 == "f4"))) && (_local3 != my._name)) && (this.range < range)) {
                    this.range = 0;
                    _root.flayers[_local3].attachMovie("explosion", "blow", 1);
                    var _local4 = new Sound(_root.flayers[_local3]);
                    _local4.attachSound("expl.mp3");
                    if (play_sound) {
                        _local4.start(0, 1);
                    }
                    _root.flayers[_local3].blow._xscale = (_root.flayers[_local3].blow._yscale = 100);
                    _root.flayers[_local3].blow.onEnterFrame = function () {
                        if (this._currentframe == this._totalframes) {
                            this._parent.createEmptyMovieClip("destruct", this.getDepth());
                        }
                    };
                    _root.flayers[_local3].damage = _root.flayers[_local3].damage + 20;
                    score_counter("misslesoot", _root.flayers[_local3]);
                    if (_root.flayers[_local3].damage > max_damage) {
                        destructor(_root.flayers[_local3]);
                    }
                    break;
                }
            }
            if (this.range < (range - 20)) {
                this._parent[this._name.split("_")[1]].missle._visible = true;
            }
            if (((this._y < top_margin) || (this._y > bottom_margin)) || ((this.range--) <= 0)) {
                this._parent[this._name.split("_")[1]].missle._visible = true;
                this._parent.createEmptyMovieClip("destruct", this.getDepth());
            }
        };
    }
    function destructor(target) {
        if (target._y < (bottom_margin - 100)) {
            target._parent.attachMovie("paratooper", "paratooper", 199);
            target._parent.paratooper._xscale = (target._parent.paratooper._yscale = 50);
            target._parent.paratooper._x = target._x * 0.99;
            target._parent.paratooper._y = target._y;
            target._parent.paratooper.onEnterFrame = function () {
                this._y++;
                this._x = this._x + 0.2;
                if (this._y > bottom_margin) {
                    stopAllSounds();
                    this._parent.createEmptyMovieClip("destruct", this.getDepth());
                }
            };
        } else {
            stopAllSounds();
        }
        target.attachMovie("flame", "flame", 99);
        target.flame._xscale = (target.flame._yscale = 50);
        var _local5 = new Sound();
        _local5.attachSound("expl2.mp3");
        if (play_sound) {
            _local5.start(0, 1);
        }
        target.onEnterFrame = function () {
            this._y = this._y + 3;
            put_smouke(this);
            this._y = this._y + 3;
            put_smouke(this);
            this._rotation = -90;
            if (this._y > (bottom_margin + 5)) {
                if (this.burn_counter == undefined) {
                    this.burn_counter = 0;
                    _root.shadows["shadow_" + this._name]._visible = false;
                }
                this._y = bottom_margin + 5;
                if ((this.burn_counter++) < 50) {
                    return(undefined);
                }
                if (this._parent.paratooper != undefined) {
                    return(undefined);
                }
                if (this._name == "f4") {
                    if (!multyplay) {
                        start_right(true);
                        f_sound.start(0, 1000);
                    } else {
                        end_game();
                    }
                }
                if (this._name == "f1") {
                    end_game();
                }
            }
        };
        score_counter("kill", target);
        var _local4;
        for (_local4 in target.plane) {
            target.plane[_local4].dx = missle_speed * (Math.random() - 0.5);
            target.plane[_local4].dy = missle_speed * (Math.random() - 0.5);
            target.plane[_local4].dr = 5 * Math.random();
            target.plane[_local4].life_counter = 20 + (30 * Math.random());
            target.plane[_local4].onEnterFrame = function () {
                this._x = this._x + this.dx;
                this._y = this._y + this.dy;
                this._rotation = this._rotation + this.dr;
                if ((this.life_counter--) == 0) {
                    this._visible = false;
                    this.onEnterFrame = null;
                }
            };
        }
    }
    stop();
    play_sound = true;
    _global.sounds = 0;
    var won_f1 = 0;
    var won_f4 = 0;
    var restart = 0;
    var num_rounds = 5;
    max_power = 4;
    top_margin = 10;
    left_margin = 0;
    right_margin = 600;
    bottom_margin = 400;
    missle_speed = 20;
    range = 50;
    missle_counter = 0;
    missle_timeout = 2100;
    missle_lasttime = 0;
    gun_lasttime = 0;
    gun_timeout = 700;
    min_stall_force = 0;
    gun_speed = 29;
    gun_counter = 0;
    max_damage = 100;
    smouke_counter = new Object();
    smouke_depth_counter = 0;
    dy = 0;
    power_step = 0.05;
    control_stearing = 17;
    repire_on = false;
    rep_damage = 65;
    rating_list = new Array("Rookie", "Officer", "Squadron Leader", "Wing Commander", "Air Commodore", "Air Chief Marshal");
    rating_kils = new Array(2, 5, 9, 15, 25);
    play_intro();
    game_play_f1._visible = false;
    game_play_f4._visible = false;
    opponent_color_transform = new Object();
    opponent_color_transform = {ra:"100", rb:"9", ga:"100", gb:"-65", ba:"100", bb:"-28", aa:"100", ab:"0"};
    s1 = new Object();
    gun_shoot = new Sound();
    gun_shoot.attachSound("pulemet");
    launch_sound = new Sound();
    launch_sound.attachSound("_sfxEngineLowLoop");
    f_sound = new Sound();
    f_sound.attachSound("_sfxEngineLoop");
    cover_sound = new Sound();
    cover_sound.attachSound("covermusic");
    ending_sound = new Sound();
    ending_sound.attachSound("endmusic");
    launch_sound.setVolume(16);
    keyListener.onKeyDown = function () {
        if ((Key.getCode() == 77) || (Key.getCode() == 109)) {
            if (_root.play_sound) {
                _root.play_sound = false;
                _root.f_sound.stop();
                _root.launch_sound.stop();
            } else if (!play_sound) {
                _root.play_sound = true;
                _root.f_sound.start(0, 1000);
                _root.launch_sound.start(0, 1000);
            }
        }
    };
    Key.addListener(keyListener);
    pauseListener.onKeyDown = function () {
        if ((Key.getCode() == 80) || (Key.getCode() == 112)) {
            _root.pause_bar = null;
            _root.pause_bar = new Object();
            _root.pause_game(_root, _root.pause_bar, 0);
        }
    };
    Key.addListener(pauseListener);
    // unexpected jump
    // unexpected jump

    function multyplayStart() {
        cover_sound.stop();
        this._parent._parent._visible = false;
        multyplay = true;
        game_play_f4._visible = true;
        on_fly = false;
        pause_block.gotoAndStop(2);
        pause_block._visible = false;
        if (play_sound) {
            launch_sound.start(0, 1000);
        }
        launch_sound.setVolume(8);
        f_sound.setVolume(8);
        showIns2();
    }
    function showIns() {
        if (!restart) {
            _root.attachMovie("how_to_play_1", "how_to_play", 200);
            _root.how_to_play.menu.onRelease = function () {
                start_game();
                init_score();
                this._parent.removeMovieClip();
            };
        } else {
            restart = false;
            start_game();
            init_score();
        }
    }
    function showIns2() {
        if (!restart) {
            _root.attachMovie("how_to_play2", "how_to_play_2", 200);
            _root.how_to_play_2.menu.onRelease = function () {
                pause_block._visible = true;
                start_game();
                init_score();
                this._parent.removeMovieClip();
            };
        } else {
            pause_block._visible = true;
            restart = false;
            start_game();
            init_score();
        }
    }
    play_control.p_buttons.play.onRelease = function () {
        this._parent._parent._visible = false;
        cover_sound.stop();
        multyplay = false;
        game_play_f4._visible = false;
        on_fly = false;
        if (play_sound) {
            launch_sound.start(0, 1000);
        }
        showIns();
    };
    play_control.p_buttons.multy_play.onRelease = multyplayStart;
    play_control.p_buttons.about.onRelease = function () {
        this._parent._parent._visible = false;
        _root.attachMovie("about", "about", 200);
        _root.about._x = 100;
        _root.about._y = 80;
        _root.about.close.onRelease = function () {
            this._parent._visible = false;
            _root.play_control._visible = true;
        };
    };
    play_control.p_buttons.play_more.onRelease = function () {
        getURL ("http://www.freeonlinegames.com/?battleoverberlin", "_blank");
    };
    // unexpected jump
    // unexpected jump

    function enemy_control(my) {
        if (multyplay) {
            return(human_control(my));
        }
        var _local9 = _root.flayers.f1;
        if (my.engine_power < max_power) {
            my.engine_power = my.engine_power + power_step;
        }
        var _local8;
        var _local12 = my._x - _local9._x;
        var _local11 = my._y - _local9._y;
        var _local4 = (Math.atan((-_local12) / _local11) * 180) / Math.PI;
        if (_local11 > 0) {
            _local4 = _local4 + 90;
        } else {
            _local4 = _local4 - 90;
        }
        var _local6;
        if (my._y < 50) {
            _local6 = 0;
        } else {
            _local6 = 12;
        }
        var _local2 = my._rotation;
        _local2 = _local2 % 360;
        if (_local2 < 0) {
            _local2 = _local2 + 360;
        }
        var _local7 = my.speed / 9;
        if ((((my._y > (bottom_margin - 20)) || (_local9.damage > max_damage)) || (my.stall_force > 3)) || ((my.stall_force > 1) && (my._y > (bottom_margin - 100)))) {
            delta_rotation = 0;
            command_delay = 0;
            if ((_local2 < 90) || (_local2 > 270)) {
                if (_local2 < 90) {
                    _local8 = _local2 - ((_local7 * (_local2 - _local6)) / 5);
                } else {
                    _local8 = _local2 + ((_local7 * ((360 - _local2) + _local6)) / 5);
                }
            } else {
                _local8 = _local2 - ((_local7 * ((_local2 - 180) + _local6)) / 5);
            }
            attack_delay = 60;
        } else if ((attack_delay--) <= 0) {
            if ((command_delay--) <= 0) {
                var _local5;
                var _local10 = 1;
                delta_rotation = _local2 - _local4;
                _local5 = Math.abs(delta_rotation);
                if (delta_rotation > 180) {
                    delta_rotation = -180;
                }
                _local5 = Math.abs(delta_rotation);
                if ((_local5 != 0) && (Math.random() > 0.7)) {
                    _local10 = delta_rotation / _local5;
                }
                command_delay = 80;
                var _local13 = _local5 < 90;
                if (_local5 > control_stearing) {
                    delta_rotation = control_stearing * _local10;
                }
                if (my._y > (bottom_margin - 140)) {
                    if ((_local2 < 90) || (_local2 > 270)) {
                        delta_rotation = Math.abs(delta_rotation);
                    } else {
                        delta_rotation = -Math.abs(delta_rotation);
                    }
                }
                if (my._y < 50) {
                    if ((_local2 < 90) || (_local2 > 270)) {
                        delta_rotation = -Math.abs(delta_rotation);
                    } else {
                        delta_rotation = Math.abs(delta_rotation);
                    }
                }
            }
            _local8 = _local2 + (Math.abs(_local7) * delta_rotation);
        }
        my._rotation = _local8;
        if ((Math.abs(my._rotation - _local4) < 16) && (my._y < (bottom_margin - 20))) {
            command_delay = 10;
            if ((_local2 < 215) || (_local2 > 325)) {
                delta_rotation = Math.random() * 3;
            }
            if (Math.random() > 0.5) {
                if ((getTimer() - missle_lasttime_2nd) >= missle_timeout) {
                    missle_lasttime_2nd = getTimer();
                    fire_missle(my);
                }
            } else if ((getTimer() - gun_lasttime_2nd) >= (gun_timeout * 2)) {
                if (my.gun_counter > 5) {
                    gun_lasttime_2nd = getTimer();
                }
                fire_gun(my);
            } else {
                my.gun_counter = 0;
            }
        }
    }
    function human_control(my) {
        var _local2 = Math.sqrt((my.dy * my.dy) + (my.dx * my.dx)) / 9;
        if (my.engine_power > 2) {
            my.engine_power = my.engine_power - power_step;
        }
        if (Key.isDown(68) && (my._y < (bottom_margin - 2))) {
            my._rotation = my._rotation - (control_stearing * _local2);
        }
        if (Key.isDown(65)) {
            my._rotation = my._rotation + (control_stearing * _local2);
        }
        if (Key.isDown(87) && (my.engine_power < max_power)) {
            my.engine_power = my.engine_power + (power_step * 3);
        }
        if (Key.isDown(83) && (my.engine_power > 2)) {
            my.engine_power = my.engine_power - power_step;
        }
        if (Key.isDown(86)) {
            if ((getTimer() - missle_lasttime_2nd) >= missle_timeout) {
                missle_lasttime_2nd = getTimer();
                fire_missle(my);
            }
        }
        if (Key.isDown(67)) {
            if ((getTimer() - gun_lasttime_2nd) >= gun_timeout) {
                if (my.gun_counter > 5) {
                    gun_lasttime_2nd = getTimer();
                }
                fire_gun(my);
            } else {
                my.gun_counter = 0;
            }
        }
    }
    missle_lasttime_2nd = 0;
    gun_lasttime_2nd = 0;
    delta_rotation = 0;
    // unexpected jump
    // unexpected jump

    function play_intro() {
        last_word._visible = false;
        multyplay = 0;
        damager_f1._visible = true;
        game_play_f1._visible = true;
        damager_f4._visible = true;
        game_play_f4._visible = false;
        _root.createEmptyMovieClip("destruct", 11);
        _root.createEmptyMovieClip("destruct", 12);
    }
    // unexpected jump
    // unexpected jump

    function repire_box_activated() {
        repire_on = true;
        var _local3 = (((right_margin - left_margin) / 2) + (100 - (200 * Math.random()))) + left_margin;
        _root.attachMovie("parabox", "parabox", 25);
        _root.parabox._x = _local3;
        _root.parabox.onEnterFrame = function () {
            if (this._y < bottom_margin) {
                this._y = this._y + 1.3;
            } else {
                this._parent.attachMovie("repire_box", "repire_box", this.getDepth() + 1);
                repire_box._x = this._x;
                repire_box._y = this._y;
                repire_box.onEnterFrame = function () {
                    if (this._visible) {
                        for (alef in _root.flayers) {
                            if (_root.flayers[alef].hitTest(this) && ((alef == "f1") || (alef == "f4"))) {
                                _root.flayers[alef].damage = Math.round(_root.flayers[alef].damage * 0.6);
                                update_damage_counter();
                                this.paradelay = (1000 * Math.random()) + 300;
                                this._visible = false;
                            }
                        }
                    } else if (this.paradelay > 0) {
                        this.paradelay--;
                    } else {
                        repire_on = false;
                        this._parent.createEmptyMovieClip("destruct", this.getDepth());
                    }
                };
                this._parent.createEmptyMovieClip("destruct", this.getDepth());
            }
        };
    }
    // unexpected jump
    // unexpected jump

    function gameover() {
        pause_block.gotoAndStop(1);
        if (!multyplay) {
            _root.game_over_pad.attachMovie("gameover", "game_over", 11);
        } else {
            _root.ending_sound.start(0, 1000);
            if (game_play_f1.score.text > game_play_f4.score.text) {
                won_f1++;
            } else {
                won_f4++;
            }
            game_play_f4.raiting.text = won_f4;
            game_play_f1.raiting.text = won_f1;
            if (won_f1 >= num_rounds) {
                _root.game_over_pad.attachMovie("gameover", "game_over", 11);
                _root.game_over_pad.attachMovie("whoWon", "whoWins", 12);
                restart = 0;
                won_f4 = 0;
                won_f1 = 0;
            } else if (won_f4 >= num_rounds) {
                _root.game_over_pad.attachMovie("gameover", "game_over", 11);
                _root.game_over_pad.attachMovie("whoWon", "whoWins", 12);
                _root.game_over_pad.whoWins.gotoAndStop(2);
                restart = 0;
                won_f4 = 0;
                won_f1 = 0;
            } else {
                restart = 1;
                start_game();
            }
        }
        _root.game_over_pad.game_over.onEnterFrame = function () {
            if (this._currentframe == this._totalframes) {
                if (!multyplay) {
                    _root.game_over_pad.game_over.removeMovieClip();
                    stopAllSounds();
                    _root.ending_sound.start(0, 9999);
                    _root.game_play_f1._visible = 0;
                    _root.game_play_f4._visible = 0;
                    _root.damager_f1._visible = 0;
                    _root.damager_f4._visible = 0;
                    _root.last_word.score.text = "You Scored: ";
                    _root.last_word.score2.text = game_play_f1.score.text;
                    _root.last_word._visible = true;
                    _root.game_over_pad.game_over.removeMovieClip();
                    _root.last_word.ok.onRelease = function () {
                        var _local2 = new LoadVars();
                        _local2.score = _root.score_f1;
                        _local2.onLoad = function () {
                            getURL ("http://www.freeonlinegames.com/scoreboard.php", "_blank");
                        };
                        _local2.gamer = 10;
                        _local2.id = random(9999999);
                        _local2.toString();
                        _local2.sendAndLoad("http://www.freeonlinegames.com/scoreboard/score_c.php", _local2, "POST");
                        _root.last_word.ok.enabled = false;
                    };
                    _root.last_word.main_menu.onRelease = function () {
                        _root.ending_sound.stop();
                        _root.cover_sound.start(0, 9999);
                        _root.last_word.ok.enabled = true;
                        _root.game_over_pad.game_over.removeMovieClip();
                        _root.last_word._visible = false;
                        play_control._visible = true;
                    };
                    _root.last_word.more_games.onRelease = function () {
                        getURL ("http://FreeGamesForYourWebsite.com/?battleoverberlin", "_blank");
                    };
                    _root.last_word.play_more.onRelease = function () {
                        getURL ("http://www.freeonlinegames.com/?battleoverberlin", "_blank");
                    };
                } else {
                    _root.last_word._visible = false;
                    play_control._visible = true;
                }
            }
        };
    }
    // unexpected jump
    // unexpected jump

    cover_sound.start(0, 9999);
    stop();


//----------------------------------------------------------------------
//Frame 15
//----------------------------------------------------------------------
    function updateScoreboard(sNum) {
        xmlPlayer = new XML();
        xmlPlayer.ignoreWhite = true;
        xmlPlayer.onLoad = function (success) {
            if (success) {
                _root["mcScoreboard" + sNum].mcLoading._visible = false;
                myPlayer = xmlPlayer.firstChild.childNodes;
                ctr2 = 0;
                while (ctr2 < myPlayer.length) {
                    thisPlayer = _root["mcScoreboard" + sNum].sboard.mcScoreHolder.mcScore.duplicateMovieClip("mcScore" + ctr2, ctr2);
                    thisPlayer._y = ctr2 * thisPlayer._height;
                    thisPlayer._visible = true;
                    if ((ctr2 % 2) > 0) {
                        thisPlayer.gotoAndStop(2);
                    }
                    thisPlayer.txtNumber.text = (ctr2 + 1) + ")";
                    thisPlayer.txtNickname.text = myPlayer[ctr2].attributes.player;
                    thisPlayer.txtScore.text = myPlayer[ctr2].attributes.score;
                    ctr2++;
                }
                _root["mcScoreboard" + sNum].sboard.mcScoreHolder.item = myPlayer.length;
                _root["mcScoreboard" + sNum].sboard.mcScoreHolder.speedy = 0;
                _root["mcScoreboard" + sNum].sboard.mcScoreHolder.desty = 0;
                _root["mcScoreboard" + sNum].sboard.mcScoreHolder.onEnterFrame = function () {
                    if ((this.desty < 0) && (this._parent.dir == "up")) {
                        this.desty = this.desty + 10;
                        if (this.desty > 0) {
                            this.desty = 0;
                        }
                    }
                    if ((this.desty > (this._parent.mcBlock._height - (this.mcScore._height * this.item))) && (this._parent.dir == "down")) {
                        this.desty = this.desty - 10;
                        if (this.desty < (this._parent.mcBlock._height - (this.mcScore._height * this.item))) {
                            this.desty = this._parent.mcBlock._height - (this.mcScore._height * this.item);
                        }
                    }
                    this.speedy = (this.desty - this._y) + (this.speedy * 0.4);
                    this._y = this._y + this.speedy;
                };
            }
            if (sNum == 1) {
                updateScoreboard(2);
            }
        };
        if (sNum == 1) {
            xmlPlayer.load((((("http://" + _root.Dsource) + ".freeonlinegames.com/scoreboard/getTopPlayer.php?id=") + _root.gameID) + "&rand=") + random(999999));
        } else if (sNum == 2) {
            xmlPlayer.load(((((("http://" + _root.Dsource) + ".freeonlinegames.com/scoreboard/getTopPlayer.php?id=") + _root.gameID) + "&rand=") + random(999999)) + "&filt=1");
        }
    }
    stop();
    var gameID = 10;
    Dsource = "www";
    mcScoreboard1.sboard.dir = "stop";
    mcScoreboard2.sboard.dir = "stop";
    mcScoreboard1.sboard.mcScoreHolder.mcScore._visible = false;
    mcScoreboard2.sboard.mcScoreHolder.mcScore._visible = false;
    updateScoreboard(1);
    // unexpected jump
    // unexpected jump




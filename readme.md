This is a dogfight simulator with a Reinforcement Learning agent. 

To run the code, type
```bash
$ pip3 install -r requirement.txt
$ python3 game.py
```
to start the program.

Or,
```
curl -L -o dogfight.zip http://github.com/QifanYang-bw/Dogfight/archive/master.zip
unzip -a dogfight.zip
cd Dogfight-master
pip3 install -r requirements.txt
python3 game.py
```

Change the playerlist array in const.py to switch player.

Keyboard settings for player 1:
- Arrow keys for direction control
- Comma(,) for fire

Keyboard settings for player 2:
- WASD for direction control
- v for fire

Each player have 20 hp, and a successful hit takes away 2 hp.

* The latest version of python3 in MacOS installed by brew might not support pygame. One of the solutions is to install the python3 package on the [official website](https://www.python.org/downloads/) instead of brew.

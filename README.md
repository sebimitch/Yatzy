# Yatzy
My implementation of the dice game Yatzy, as a text (terminal) game. Play free/forced Yatzy with 1-4 players, where the players could be either human or bot.

![](Yatzy.gif)

## Usage
Tested on Python version "3.7.3"
```
python yatzy.py
```

## Possible improvements
- While the game mode "Free Yatzy" works with bots, the current implementation is just
following the board, similar to "Forced Yatzy". Ideally the program would determine what
category ("Aces", "One pair", etc.) the current dice setup would be best to aim towards
for the next throw(s), and once there are no more throws, the best category to put points in.

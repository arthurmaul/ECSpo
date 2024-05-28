# stdlib
from types import SimpleNamespace # for simple dummy objects.

#lib
from mecs2 import *

def movement_system(): # translates velocity onto position.
    positions, velocities = query('position', 'velocity')
    for p, v in zip(positions, velocities):
        p.x += v.x
        p.y += v.y

def input_system(): # gets input to allow exit.
    if input('continue? > ') == EXIT: return EXIT

def draw_system(): # prints data to the screen so we can see whats going on.
    positions, velocities = query('position', 'velocity')
    for p, v in zip(positions, velocities):
        print(f'pos: {p} | vel: {v}')

# schedule all systems.
schedule('Dispatch', input_system)
schedule('Update', movement_system)
schedule('Draw', draw_system)

# create out components.
class Vector2(SimpleNamespace): pass

# create out entities.
attach('position', 'player', Vector2(x=0, y=0))
attach('velocity', 'player', Vector2(x=3, y=5))
attach('sprite', 'player', 'player.png')

attach('position', 'player2', Vector2(x=4, y=5))
attach('velocity', 'player2', Vector2(x=7, y=19))
attach('sprite', 'player2', 'player2.png')

attach('position', 'orc1', Vector2(x=5, y=9))
attach('velocity', 'orc1', Vector2(x=2, y=1))
attach('sprite', 'orc1', 'player.png')

attach('position', 'orc2', Vector2(x=7, y=7))
attach('sprite', 'orc2', 'player.png')

# run the main loop.
main()
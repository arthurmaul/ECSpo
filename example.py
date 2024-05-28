# stdlib
from types import SimpleNamespace # for simple dummy objects.

#lib
import package as engine

def movement_system(): # translates velocity onto position.
    positions, velocities = engine.query('position', 'velocity')
    for p, v in zip(positions, velocities):
        p.x += v.x
        p.y += v.y

def input_system(): # gets input to allow exit.
    if input('continue? > ') == engine.EXIT: return engine.EXIT

def draw_system(): # prints data to the screen so we can see whats going on.
    positions, velocities = engine.query('position', 'velocity')
    for p, v in zip(positions, velocities):
        print(f'pos: {p} | vel: {v}')

# schedule all systems.
(engine.schedule
    ('Dispatch', input_system)
    ('Update', movement_system)
    ('Draw', draw_system))

# create out components.
class Vector2(SimpleNamespace): pass

# create out entities.
(engine.attach
    ('position', 'player', Vector2(x=0, y=0))
    ('velocity', 'player', Vector2(x=3, y=5))
    ('sprite', 'player', 'player.png')
    
    ('position', 'player2', Vector2(x=4, y=5))
    ('velocity', 'player2', Vector2(x=7, y=19))
    ('sprite', 'player2', 'player2.png')
    
    ('position', 'orc1', Vector2(x=5, y=9))
    ('velocity', 'orc1', Vector2(x=2, y=1))
    ('sprite', 'orc1', 'player.png')
    
    ('position', 'orc2', Vector2(x=7, y=7))
    ('sprite', 'orc2', 'player.png'))

# run the main loop.
engine.main()

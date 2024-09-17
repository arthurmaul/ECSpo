from dataclasses import dataclass

import mecs as engine
from mecs import Storage, Template, View, Channel, Scene

@dataclass
class Vec2:
    x: float
    y: float


world = Storage()

pos = world.pool("position") # position
vel = world.pool("velocity") # velocity
frz = world.tag("frozen") # frozen

movable = (Template(world)
    .set(pos, Vec2, 0, 0)
    .set(vel, Vec2, 5, 5))

moveables = (View(world)
    .select(pos, vel, world.EID)
    .where(pos, vel)
    .unless(frz)
    .build())

knight1 = movable.build("knight 1")
goblin1 = movable.build("g1")
goblin2 = movable.build("g2")
goblin3 = movable.build("g3")
world.set(goblin3, frz)

print(world)

launch = Channel()
@launch
def say_hello():
    print("Hello tester! Welcome to the sim :)")


events = Channel()
def input_system():
    match input('> '):
        case "quit" | "q":
            engine.quit()
events.connect(input_system)


@(update := Channel())
def movement_system():
    for pos, vel, _ in moveables:
        pos.x += vel.x
        pos.y += vel.y


@(render := Channel())
def draw_system():
    for pos, vel, eid in moveables:
        print(f'{eid}(pos: {pos}, vel: {vel})')


@(finish := Channel())
def say_byebye():
    print("Bye tester! Hope you had fun :)")


scene = Scene(
    launch,
    Channel(
        events,
        update,
        render),
    finish)
scene.enter()

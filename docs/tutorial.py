# dataclasses allow for component creation with less boilerplate
from dataclasses import dataclass

# First we import mecs itself.
# I use the alias engine, but its up to you.
import mecs as engine

# Next I normally pull in a few modules for convinience.
# You can easily use `engine.<function | Class>` if you want.
from mecs import Storage, Template, Observer, Channel, Scene


# A simple way to test things is with a movement system.
# For that, this simple vector with 2 members is fine.
@dataclass
class Vec2:
    x: float
    y: float


"""
Storage
===========
In order to use the ecs, we need to instantiate a storage object.
This will hold our components for us, organized by the entity.
"""
# WARNING: All data is localized to a storage, so if you use multiple, make sure you are accessing the right one!

world = Storage()

"""
Pools & Tags
================
Theres a number of ways we can store data in the ecs.
Pools store component data. They can hold any data type.
Tags are simple added to the list of components an entity owns.
This allows us to filter entities with them, but they dont store anything.
"""
# NOTE: By passing in a string, we can explcitly state what we want the component to be identified as.

pos = world.pool("position")
vel = world.pool("velocity")
frozen = world.tag("frozen")

"""
Templates
=============
Templates allow us to avoid repetative assignments when constructing entities.
We can define what classes and values they will use, and simply build them on demand.
"""
# NOTE: Templates are bound to a storage, but they can be reparented with the `template.root(<storage>)` method.

movable = (Template(world)
    .set(pos, Vec2, 0, 0)
    .set(vel, Vec2, 5, 5))

"""
Observers
========
Observers are updated every time a component is set or removed, and are iterable, allowing you to access matching entities.
You may also specify component data to recieve instead using `.select` method.
The order of the component ids when you call the select method is the order they will be returned to you in.
You may also specify filters based on the `.where` and `.unless` methods.
"""
# NOTE: If the observer is created after entities are in the storage, you must use the `Observer.scan()` method to gather existing matches.

moveables = (Observer(world)
    .select(pos, vel, world.EID)
    .where(pos, vel)
    .unless(frozen)
    .build())

knight1 = movable.build("knight 1")
goblin1 = movable.build("g1")
goblin2 = movable.build("g2")
goblin3 = movable.build("g3")
world.set(goblin3, frozen)


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


def run():
    scene = Scene(
        launch,
        Channel(
            events,
            update,
            render),
        finish)
    
    scene.enter()


if __name__ == "__main__":
    run()


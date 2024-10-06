# ECSPO: The Pythonic Entity Framework.
# ========================================
# AUTHOR: Arthur Maul II
# DATE: 2024.10.5

# Intro.
# =========
# Ecspo is an entity component system written in python.
# It has no dependencies and is meant to be as simple as possible,
# while maintaining an ergonomic api.
# 
# This example servers as a quickstart guide for the library.
# For an in depth guide, see the manual.


# Imports.
# ===========
# For this demo ill be importing dataclasses,
# which allow for component creation with less boilerplate.
from dataclasses import dataclass

# I will also pull in the lib modules directly for convinience.
# You can easily use `engine.<function or Class>` if you want.
from ecspo import (
    Storage,
    Prototype,
    Observer,
    Channel,
    Scene,
    shutdown
)


# Components
# ============= 
# Components are classes with only data.
# They represent some piece of information an entity owns.
# What components an entity owns will determine how it behaves.

# A simple way to test things is with a movement system.
# For that, this simple 2d vector with 2 members is fine.


@dataclass
class Vec2:
    x: float = 0
    y: float = 0


# Storage
# ==========
# In order to use the ecs, we need to instantiate a storage object.
# This will hold our components for us, organized by the entity.
# WARNING: All data, is localized to a storage, so if you use multiple, always make sure you are accessing the right one!


world = Storage()


# Pools & Tags
# ================
# Theres a number of ways we can store data in the ecs.
# Pools store component data. They can hold any data type.
# Tags are simple added to the list of components an entity owns.
# This allows us to filter entities with them, but they dont store anything.
# NOTE: By passing in a string, we can explcitly state what we want the component to be identified as internally.

position = world.pool("position")
velocity = world.pool("velocity")
frozen = world.tag("frozen")

# Entities
# ===========


e1 = world.spawn("e1")
world.set(e1, position, Vec2(10, 10))
world.set(e1, velocity, Vec2(5, 5))
world.set(e1, frozen)

e2 = world.handle("e2")
e2.set(position, Vec2(10, 10))
e2.set(velocity, Vec2(5, 5))

# Prototypes
# ============
# Prototypes allow us to avoid repetitive assignments when constructing entities.
# We can define a prototypal entitiy and what classes and values they will use, and simply clone them on demand.
# NOTE: Prototypes are bound to a storage, but they can be reparented with the `<prototype>.reparent(<storage>)` method.


base = (Prototype(world)
    .set(position, Vec2, 0, 0)
    .set(velocity, Vec2, 5, 5))

e3 = base.clone("e3")
e4 = base.clone("e4")


# Observers
# ============
# Observers are updated every time a component is set or unset, and are iterable, allowing you to access matching entities.
# You may also specify component data to recieve instead using `.select` method.
# The order of the component ids when you call the select method is the order they will be returned to you in.
# You may also specify filters based on the `.where` and `.unless` methods.
# NOTE: If the observer is created after entities are in the storage, you must use the `Observer.search()` method to gather existing matches.


moving = (Observer(world)
    .where(position, velocity)
    .unless(frozen)
    .build())
moving.search()


# Channels
# ===========
# Channels are subscription lists.
# You can connect functions using a predefined channel as a decorator... 
#     @<channel>
#     <function def...>
# can define a channel and use it as a decorator in one line...
#     @<name> := Channel()
# can pass functionss into the channel on creation...
#     <name> := Channel(<functions...>)
# or even use the channel.connect method.
#     <channel>.connect(function)
#
# I prefer to declare all my channels at the top, and then use the decorator.
# Its up to you to decide in your own projects :)


launch = Channel()
events = Channel()
update = Channel()
render = Channel()
finish = Channel()


# Systems
# ==========
# Systems are plain functions.
# Each system must be subscribe to a channel to run.
# Any time an event is sent to a channel,
# all systems listening to that channel will be triggered.


@launch
def say_hello():
    """
    Displays a message to the user on simulation startup.
    """
    print("Hello tester! Welcome to the sim :)")


@events
def input_system():
    """
    Checks for user input and handles any commands.
    """
    match input('> '):
        case "quit" | "q":
            shutdown()


@update
def movement_system():
    """
    Gathers positions and velocities and maps velocity onto position.
    """
    # we can interate over observers using select to access specific components.
    for pos, vel in moving.select(position, velocity):
        pos.x += vel.x
        pos.y += vel.y


@render
def draw_system():
    """
    Gathers positions, velocities, and their associated ids and displays them on the screen.
    """
    # we can interate over observers to access entities.
    for eid in moving:
        print(f'{eid}(pos: {world.get(eid, position)}, vel: {world.get(eid, velocity)})')


@finish
def say_byebye():
    """
    Displays a message to the user on simulation shutdown. 
    """
    print("Bye tester! Hope you had fun :)")


def run():
    """
    Constructs the scenes and runs the main loop.
    """
    # Scenes
    # =========
    # Scenes are what actually runs the simulation
    # They each have a schedule, consiting of a startup, a loop, and a shutdown, in that order.
    scene = Scene(
        # We can add channels directly to a scene ...
        launch,
        # or nest them in other channels to create more complex scenes.
        Channel(
            events,
            update,
            render),
        finish)

    # Once a scene has been configured with its schedule, you enter it with <scene>.enter()
    # Calling enter on a scene will start its event loop,
    # which will run until shutdown or leave is called
    scene.enter()


if __name__ == "__main__":
    run()


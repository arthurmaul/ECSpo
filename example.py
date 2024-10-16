# ECSPO: A Pythonic Entity Framework.
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
    Table,
    Query,
    Channel
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


# Table
# ==========
# In order to use the ecs, we need to instantiate a table object.
# This will hold our components for us, organized by entity id.
# WARNING: All data, is localized to a table, so if you use multiple, always make sure you are accessing the right one!


world = Table()


# Pools & Tags
# ================
# Theres a number of ways we can store data in the ecs.
# Pools store component data. They can hold any data type.
# Tags are simple other entities added to the list of components an entity owns.
# This allows us to filter entities with them, but they dont store anything.
# NOTE: By passing in a string, we can explcitly state what we want the component to be identified as internally.


position = world.pool("position")
velocity = world.pool("velocity")
frozen = world.spawn("frozen")


# Entities
# ===========
# Entities are identifiers used to access component data.
# Instead of holding attributes, they simply are a unique key
# This key used to associate data with the entity


e1 = world.spawn("e1")
world.set(e1, position, Vec2(10, 10))
world.set(e1, velocity, Vec2(5, 5))
# world.tag(e1, frozen)


# Prototypes
# ============
# We can use entities as prototypes for other entities
# We can simply define it components and tags and clone it as necessary
# WARNING: Prototypes must be duplicated to be shared between tables as theyre entities.


e2 = world.clone(e1, "e2")
e3 = world.clone(e1, "e3")
e4 = world.clone(e1, "e4")


# Observers
# ============
# Queries collect entities based on a specified filter strategy, storing all matches until rebuilt.
# You specify the filter strategy with the `.where` and `.unless` methods.
# Queries can be iterated over to access all the matching entity ids found in the last build.
# You may also get specific component data to recieve instead using `.select` method.
# The order of the component ids when you call the select method is the order they will be returned to you in.
# NOTE: Unless the entity composition never changes after the query creation, you must use the `query.build()` method to gather updated matches.


moving = (Query(world)
    .where(position, velocity)
    .unless(frozen)
    .build())


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
            finish.emit()
            exit()


@update
def movement_system():
    """
    Gathers positions and velocities and maps velocity onto position.
    """
    # we can interate over observers using select to access specific components.
    for pos, vel in moving.build().select(position, velocity):
        pos.x += vel.x
        pos.y += vel.y


@render
def draw_system():
    """
    Gathers positions, velocities, and their associated ids and displays them on the screen.
    """
    # we can interate over observers to access entities.
    for eid in moving.build():
        print(f'{eid}(pos: {world.get(eid, position)}, vel: {world.get(eid, velocity)})')


@finish
def say_byebye():
    """
    Displays a message to the user on simulation shutdown. 
    """
    print("Bye tester! Hope you had fun :)")


def main():
    """
    Runs the main loop.
    """
    launch.emit()
    while True:
        events.emit()
        update.emit()
        render.emit()
        

if __name__ == "__main__":
    main()


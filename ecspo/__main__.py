from channel  import Channel
from observer import Observer
from scene    import Scene, shutdown
from storage  import Storage, Entity, Prototype
# dataclasses allow for component creation with less boilerplate
from dataclasses import dataclass

# First we import ecspo itself.
# I use the alias engine, but its up to you.
import ecspo as engine

# Next I normally pull in a few modules for convinience.
# You can easily use `engine.<function or Class>` if you want.
from ecspo import Storage, Prototype, Observer, Channel, Scene


# A simple way to test things is with a movement system.
# For that, this simple vector with 2 members is fine.
@dataclass
class Vec2:
    x: float = 0
    y: float = 0


# Storage
# ==========
# In order to use the ecs, we need to instantiate a storage object.
# This will hold our components for us, organized by the entity.
# WARNING: All data is localized to a storage, so if you use multiple, always make sure you are accessing the right one!

world = Storage()

# Pools & Tags
# ================
# Theres a number of ways we can store data in the ecs.
# Pools store component data. They can hold any data type.
# Tags are simple added to the list of components an entity owns.
# This allows us to filter entities with them, but they dont store anything.
# NOTE: By passing in a string, we can explcitly state what we want the component to be identified as.

pos    = world.pool("position")
vel    = world.pool("velocity")
frozen = world.tag("frozen")

# Observers
# ============
# Observers are updated every time a component is set or removed, and are iterable, allowing you to access matching entities.
# You may also specify component data to recieve instead using `.select` method.
# The order of the component ids when you call the select method is the order they will be returned to you in.
# You may also specify filters based on the `.where` and `.unless` methods.
# NOTE: If the observer is created after entities are in the storage, you must use the `Observer.scan()` method to gather existing matches.

moveables = (Observer(world)
    .select(pos, vel, world.EID)
    .where(pos, vel)
    .unless(frozen)
    .init())

# Prototypes
# ============
# Templates allow us to avoid repetitive assignments when constructing entities.
# We can define a prototypal entitiy and what classes and values they will use, and simply clone them on demand.
# NOTE: Prototypes are bound to a storage, but they can be reparented with the `template.reparent(<storage>)` method.

movable = (Prototype(world)
    .set(pos, Vec2, 0, 0)
    .set(vel, Vec2, 5, 5))

knight1 = movable.clone("k1")
goblin1 = movable.clone("g1")
goblin2 = movable.clone("g2")
goblin3 = movable.clone("g3")
# world.set(goblin3, frozen)
world.get(goblin3, pos).x = 100

# Systems
# ==========
# Systems are plain functions.
# Each system must be subscribe to a channel.
# Any time an event is sent to a channel,
# all systems listening to that channel will be triggered.

# You can register systems using a predefined channel as a decorator ... 
#     @<channel>
# can define a channel and use it as a decorator in one line ...
#     @<name> := Channel()
# can pass systems into the channel on creation ...
#     <name> := Channel(<systems...>)
# or even use the channel.connect method.
#     <channel>.connect(system)

# I prefer to declare all my channels at the top, and then use the decorator.
# Its up to you to decide in your own projects :)


launch = Channel()
events = Channel()
update = Channel()
render = Channel()
finish = Channel()

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
            engine.shutdown()


@update
def movement_system():
    """
    Gathers positions and velocities and maps velocity onto position.
    """
    for pos, vel, _ in moveables:
        pos.x += vel.x
        pos.y += vel.y


@render
def draw_system():
    """
    Gathers positions, velocities, and their associated ids and displays them on the screen.
    """
    # we can interate over observers to access data in our systems
    for pos, vel, eid in moveables: 
        print(f'{eid}(pos: {pos}, vel: {vel})')


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
    scene = Scene(
        # We can add observers directly to a scene ...
        launch,
        # or nest them in other observers to create more complex scenes.
        Channel(
            events,
            update,
            render),
        finish)

    # Calling enter on a scene will start its event loop.
    scene.enter()


if __name__ == "__main__":
    run()


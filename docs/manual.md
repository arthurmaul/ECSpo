# ECSPO: A Pythonic Entity Framework.
author: Arthur Maul II

---

## Intro.
Ecspo is an entity component system written in python.
It has no dependencies and is meant to be as simple as possible,
while maintaining an ergonomic api.

This first part of the manual servers as a quickstart guide for the library.

The second part will serve as a reference.

### Modules
I prefer to pull in the lib modules directly for convinience.

```py
from ecspo import (
    Table,
    Query,
    Channel
)
```

You can easily import the lib itself under an alias and use `alias.function` or `alias.class` if you want.

### Components
Components are classes with only data.
They represent some piece of information an entity owns.
What components an entity owns will determine how it behaves.

For example, this simple 2d vector with 2 members is fine.

```py
@dataclass
class Vec2:
    x: float = 0
    y: float = 0
```

You can also use primitives like ints, strings, and even lists and dictionaries.

### Table
In order to use the ecs, we need to instantiate a table object.
This will hold our components for us, organized by entity id.

```py
world = Table()
```

Dont forget, all data is localized to a table, so if you use multiple, always make sure you are accessing the right one!

### Pools & Tags
Theres a number of ways we can store data in the ecs.
Pools store component data. They can hold any data type.
Tags are simple other entities added to the list of components an entity owns.
This allows us to filter entities with them, but they dont store anything.


```py
position = world.pool("position")
velocity = world.pool("velocity")
frozen = world.spawn("frozen")
```

By passing in a string, we can explcitly state what we want the component to be identified as internally.

### Entities
Entities are identifiers used to access component data.
Instead of holding attributes, they simply are a unique key
This key used to associate data with the entity

```py
e1 = world.spawn("e1")
world.set(e1, position, Vec2(10, 10))
world.set(e1, velocity, Vec2(5, 5))
world.tag(e1, frozen)
```

### Prototypes
We can use entities as prototypes for other entities
We can simply define it components and tags and clone it as necessary

Prototypes must be duplicated to be shared between tables as theyre entities.

```py
e2 = world.clone(e1, "e2")
e3 = world.clone(e1, "e3")
e4 = world.clone(e1, "e4")
```

### Queries
Queries collect entities based on a specified filter strategy, storing all matches until rebuilt.
You specify the filter strategy with the `.where` and `.unless` methods.
Queries can be iterated over to access all the matching entity ids found in the last build.
You may also get specific component data to recieve instead using `.select` method.
The order of the component ids when you call the select method is the order they will be returned to you in.

```py
moving = (Query(world)
    .where(position, velocity)
    .unless(frozen)
    .build())
```

Be careful! Unless the entity composition never changes after the query creation, you must use the `query.build()` method to gather updated matches.

### Channels
Channels are subscription lists.
You can connect functions using a predefined channel as a decorator... 

```py
@channel
def system():
    ...
```

can define a channel and use it as a decorator in one line...

```py
@name := Channel()
def system():
    ...
```

can pass functionss into the channel on creation...

```py
name := Channel(system1, system2, ...)
```

or even use the channel.connect method manually.

```py
channel.connect(system)
```

I prefer to declare all my channels at the top, and then use the decorator.
Its up to you to decide in your own projects :)

```py
# The set of phases I usually define for the simulation.
launch = Channel()
events = Channel()
update = Channel()
render = Channel()
finish = Channel()
```

# Systems
Systems are plain functions.
Each system must be subscribe to a channel to run.
Any time an event is sent to a channel,
all systems listening to that channel will be triggered.

```py
@events
def input_system():
    match input('> '):
        case "quit" | "q":
            finish.emit()
            exit()

@update
def movement_system():
    for pos, vel in moving.build().select(position, velocity):
        pos.x += vel.x
        pos.y += vel.y

@render
def draw_system():
    ...

def main():
    launch.emit()
    while True:
        events.emit()
        update.emit()
        render.emit()
```

---

## Reference

| Method | Parameters | Return | Description |
| --- | --- | --- | --- |
| Table |
| | | |


# Mecs
## An ecs implementation for game development in python
- implementation focusing on basic data structures and functions
- intuitive api with minimal boilerplate and fast startup
- easy to understand src code, with a focus on simplicity and readability
- built as a simple implementation of ecs
- generic api, allowing use in game dev, app dev, or other applications
---

## Installation
the easiest way to get up and running is to start you vm of choice and then to use pip
  
```
pip install py-mecs
```

it can then be imported using the library name under whatever alias you want

```py
import mecs as engine
```

## Getting started
1. You can find the docs for contributors [here](docs/for_contributors/getting_started.md) and for users [here](docs/for_users/getting_started.md)
2. The [reference](docs/reference/index.md) and an [example](example.py) are provided to lay out the feature set of the library once you've got the basics down
3. Still have questions? im at arthurmiiengineering@gmail.com, you can shoot me an email!

## Features
- [x] Entity creation/deletion
- [x] Component attachment/detachment
- [ ] Batch addition
- [ ] Blueprints
- [ ] Entity handle class
- [x] single/multi component queries
- [ ] relationships
- [ ] tags
- [x] system schedule
- [ ] custom scheduling
- [ ] async scheduling

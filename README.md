# Mecs
## An ecs implementation for game development in python
- implementation focusing on basic data structures and functions
- intuitive api with minimal boilerplate and fast startup
- easy to understand src code, with a focus on simplicity and readability
- built as a simple implementation of ecs
- generic api, allowing use in game dev, app dev, or other applications
---
<details>

## <summary> installation
the easiest way to get up and running is to start you vm of choice and then to use pip
  
```
pip install py-mecs
```

it can then be imported using the library name under whatever alias you want

```py
import mecs as engine
```

</details>

## configuration
- the exit keyword can be set directly by doing `mecs.EXIT = new_exit_code`
- more coming soon!
## features
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

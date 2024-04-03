"""MECS-2: A minimal ecs in 50 lines, version 2. Written by Arthur Maul."""
from functools import reduce
from collections import defaultdict

owners    = defaultdict(list)
registry  = defaultdict(dict)
resources = dict()
queue     = defaultdict(dict)
EXIT      = 'exit'

def attach(cid, eid, component):
    owners[eid].append(cid)
    registry[cid][eid] = component

def detach(cid, eid):
    owners[eid].remove(cid)
    registry[cid].pop(eid)

def delete(eid):
    [detach(cid, eid) for cid in owners[eid]]

def query(*cids):
    eids        = [set(registry[cid]) for cid in cids]
    common_eids = reduce(lambda accumulator, value: accumulator & value, eids)
    components  = [[registry[cid][eid] for eid in common_eids] for cid in cids]
    return components

def store(**resources):
    resources.update(resources)

def resource(key):
    return resources[key]

def schedule(stage, system, slot: int = 1000) -> None:
    if not slot in queue[stage]: queue[stage][slot] = list()
    queue[stage][slot].append(system)

def run(stage):
    ordered = dict(sorted(queue[stage].items()))
    output  = [[system() for system in systems] for slot, systems in ordered.items()]
    for values in output:
        if EXIT in values: return EXIT

def main():
    run('StartUp')
    while True:
        stages = ('Dispatch', 'PreUpdate', 'Update', 'PostUpdate', 'Draw')
        output = [run(stage) for stage in stages]
        if EXIT in output: break
    run('ShutDown')

if __name__ == '__main__':
    from types import SimpleNamespace

    def movement_system():
        positions, velocities = query('position', 'velocity')
        for p, v in zip(positions, velocities):
            p.x += v.x
            p.y += v.y

    def input_system():
        if input('continue? > ') == EXIT: return EXIT

    def draw_system():
        positions, velocities = query('position', 'velocity')
        for p, v in zip(positions, velocities):
            print(f'pos: {p} | vel: {v}')

    schedule('Dispatch', input_system)
    schedule('Update', movement_system)
    schedule('Draw', draw_system)

    class Vector2(SimpleNamespace): pass

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

    main()
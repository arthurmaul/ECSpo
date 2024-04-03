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
    common_eids = common_eids = eids[0].intersection(eid[1:])
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

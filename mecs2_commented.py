'''MECS-2: A minimal ecs in 50 lines, version 2. Written by Arthur Maul.'''
from collections import defaultdict

owners    = defaultdict(list)
registry  = defaultdict(dict)
resources = dict()
queue     = defaultdict(dict)
EXIT      = 'exit'

def attach(cid, eid, component):
    '''Adds a component under an entity id and stores the component id under that entity id.'''
    owners[eid].append(cid)
    registry[cid][eid] = component

def detach(cid, eid):
    '''Removes both the reference to the component and the component itself from the entity id.'''
    owners[eid].remove(cid)
    registry[cid].pop(eid)

def delete(eid):
    '''Removes all the components of an entity.'''
    [detach(cid, eid) for cid in owners[eid]]

def query(*cids):
    '''Returns a set of arrays, in the order of component ids provided, with each holding the components of that type.'''
    eids        = [set(registry[cid]) for cid in cids]
    common_eids = common_eids = eids[0].intersection(eid[1:])
    components  = [[registry[cid][eid] for eid in common_eids] for cid in cids]
    return components

def store(**resources):
    '''Stores a resource to be accessed via the "resource" function.'''
    resources.update(resources)

def resource(key):
    '''Returns a resource stored in the dictionary.'''
    return resources[key]

def schedule(stage, system, slot: int = 1000) -> None:
    '''Adds a system under a stage, with a slot if provided.'''
    if not slot in queue[stage]: queue[stage][slot] = list()
    queue[stage][slot].append(system)

def run(stage):
    '''Runs all the systems in a stage in ascending order, first based on slot, then based on registration order.'''
    ordered = dict(sorted(queue[stage].items()))
    output  = [[system() for system in systems] for slot, systems in ordered.items()]
    for values in output:
        if EXIT in values: return EXIT

def main():
    '''Provides 7 base events and runs them in proper order, provided an exit to be used to break out of the gameloop.'''
    run('StartUp')
    while True:
        stages = ('Dispatch', 'PreUpdate', 'Update', 'PostUpdate', 'Draw')
        output = [run(stage) for stage in stages]
        if EXIT in output: break
    run('ShutDown')

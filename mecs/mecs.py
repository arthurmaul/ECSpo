"""MECS: A minimal ecs. Written by Arthur Maul II."""


from collections import defaultdict

from uuid import uuid4


class RecursiveSubscription(Exception):
    ...


context = list()

class Scene:    
    def __init__(self, startup, updates, cleanup):
        self.running = False
        self.startup = startup
        self.updates = updates
        self.cleanup = cleanup

    def enter(self):
        self.startup.emit()
        self.running = True
        context.append(self)
        while self.running:
            self.updates.emit()
        self.cleanup.emit()

    def exit(self):
        context.remove(self)
        self.running = False

def exit():
    context[-1].exit()

def swap(scene):
    context[-1] = scene

def shutdown():
    for scene in context.copy():
        scene.exit()


class Channel:
    def __init__(self, *responders, signal=None):
        self.signal = signal or str(uuid4())
        self.responders = list(responders)
        self.active = False
        
    def __iter__(self):
        yield from self.responders

    def __call__(self, responder):
        self.connect(responder)
        
    def connect(self, responder):
        self.responders.append(responder)
        
    def emit(self, *args, **kwargs):
        if self.active:
            raise RecursiveSubscription(f"Recursive signal to {self.signal} channel was detected (likely caused by the channel having itself as one of the responders or one of the responder channels had this channel as a responder creating a cycle of emitting signals forever)")
        self.active = True
        return [responder.emit(*args, **kwargs)
            if isinstance(responder, type(self))
            else responder(*args, **kwargs)
            for responder in self.responders]
        self.active = False


class Storage:
    def __init__(self):
        self.eindex = dict() # entities
        self.cindex = dict() # components
        self.iobs = dict() # including observers
        self.eobs = dict() # excluding observers
        self.EID = self.pool("_EID")

    def handle(self, eid=None):
        if not eid:
            eid = self.spawn()
        if not eid in self.eindex:
            eid = self.spawn(eid)
        return Entity(self, eid)

    def spawn(self, eid=None):
        eid = eid or str(uuid4())
        self.eindex[eid] = set()
        self.set(eid, self.EID, eid)
        return eid
    
    def despawn(self, eid):
        for cid in self.eindex[eid]:
            self.unset(cid, eid)
        self.eindex.pop(eid)

    def pool(self, cid=None):
        cid = cid or str(uuid4())
        self.iobs[cid] = set()
        self.eobs[cid] = set()
        self.cindex[cid] = dict()
        return cid

    def tag(self, cid=None):
        cid = cid or str(uuid4())
        self.iobs[cid] = set()
        self.eobs[cid] = set()
        return cid
    
    def release(self, cid):
        if cid in self.cindex:
            for eid in self.cindex[cid]:
                self.unset(eid, cid)
        self.vindex.pop(cid)
        self.cindex.pop(cid)

    def set(self, eid, cid, obj=None):
        if obj:
            self.cindex[cid][eid] = obj
        self.eindex[eid].add(cid)
        for obs in self.iobs[cid]:
            obs.check(eid)
        for obs in self.eobs[cid]:
            obs.reject(eid)

    def unset(eid, cid):
        if cid in self.cindex:
            self.cindex[cid].pop(eid)
        self.eindex[eid].remove(cid)
        for obs in self.iobs[cid]:
            obs.reject(eid)
        for obs in self.eobs[cid]:
            obs.check(eid)

    def get(self, eid, cid):
        if not cid in self.cindex:
            return
        return self.cindex[cid][eid]

    def has(self, eid, cid):
        return cid in self.eindex[eid]


class Entity:
    def __init__(self, storage, eid):
        self.eid = eid
        self.storage = storage

    def set(self, cid, obj=None):
        self.storage.set(self.eid, cid, obj)

    def unset(self, cid):
        self.storage.unset(self.eid, cid)

    def get(self, cid):
        self.storage.get(self.eid, cid)

    def has(self, cid):
        self.storage.has(self.eid, cid)

    def despawn(self):
        self.storage.despawn(self.eid)


class Template:
    def __init__(self, storage):
        self.template = list()
        self.storage = storage

    def root(self, storage):
        self.storage = storage
        return self

    def set(self, cid, cls, *args, **kwargs):
        self.template.append((cid, cls, args, kwargs))
        return self

    def build(self, eid=None):
        if not self.storage:
            return
        eid = self.storage.spawn(eid)
        for cid, cls, args, kwargs in self.template:
            self.storage.set(eid, cid, cls(*args, **kwargs))
        return eid


class Observer:
    def __init__(self, storage):
        self.storage = storage
        self.eids = set()
        self.cids = list()
        self.include = set()
        self.exclude = set()

    def __iter__(self):
        yield from ((self.storage.get(eid, cid)
            for cid in self.cids)
            for eid in self.eids)

    def select(self, *cids):
        self.cids.extend(cids)
        return self

    def deselect(self, *cids):
        for cid in cids:
            self.cids.remove(cid)
        return self

    def where(self, *cids):
        self.include.update(cids)
        return self

    def unless(self, *cids):
        self.exclude.update(cids)
        return self

    def accept(self, eid):
        if eid in self.eids:
            return None
        self.eids.add(eid)

    def reject(self, eid):
        if not eid in self.eids:
            return None
        self.eids.remove(eid)

    def check(self, eid):
        qualifies = (self.storage.has(eid, cid)
            for cid in self.include)
        disqualifies = (self.storage.has(eid, cid)
            for cid in self.exclude)
        if all(qualifies) and not any(disqualifies):
            self.accept(eid)
            return None
        self.reject(eid)
        return self

    def build(self):
        for cid in self.include:
            self.storage.iobs[cid].add(self)
        for cid in self.exclude:
            self.storage.eobs[cid].add(self)
        return self

    def scan(self):
        for cid in self.include:
            for eid in self.storage.cindex[cid]:
                self.check(eid)


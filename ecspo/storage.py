from uuid import uuid4


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

    def unset(self, eid, cid):
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
        return self

    def unset(self, cid):
        self.storage.unset(self.eid, cid)
        return self

    def get(self, cid):
        return self.storage.get(self.eid, cid)

    def has(self, cid):
        return self.storage.has(self.eid, cid)

    def despawn(self):
        self.storage.despawn(self.eid)
        return self


class Prototype:
    def __init__(self, root):
        self.data = list()
        self.root = root

    def extends(self, prototype):
        self.data.extend(prototype.data)

    def reparent(self, root):
        self.root = root
        return self

    def set(self, cid, cls, *args, **kwargs):
        self.data.append((cid, cls, args, kwargs))
        return self

    def clone(self, eid=None):
        eid = self.root.spawn(eid)
        for cid, cls, args, kwargs in self.data:
            self.root.set(eid, cid, cls(*args, **kwargs))
        return eid


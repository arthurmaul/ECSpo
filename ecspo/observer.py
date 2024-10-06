class Observer:
    def __init__(self, storage):
        self.storage = storage
        self.include = set()
        self.exclude = set()
        self.eids = set()

    def __iter__(self):
        yield from self.eids

    def select(self, *cids):
        yield from (tuple(self.storage.get(eid, cid)
            for cid in cids)
            for eid in self)

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

    def search(self):
        for cid in self.include:
            for eid in self.storage.cindex[cid]:
                self.check(eid)


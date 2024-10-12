class Query:
    def __init__(self, table):
        self.table = table
        self.results = set()
        self.incl = set()
        self.excl = set()

    def __iter__(self):
        yield from self.results

    def select(self, *cids):
        yield from (tuple(self.table.get(eid, cid)
            for cid in cids)
            for eid in self)

    def where(self, *cids):
        self.incl.update(cids)
        return self

    def unless(self, *cids):
        self.excl.update(cids)
        return self

    def build(self):
        pools = [set(self.table.cmap[CID])
            for CID in self.incl
            if CID in self.table.cmap] 
        results = set.intersection(*pools)
        self.results = {EID
            for EID in results
            if all([CID
                not in self.table.emap[EID]
                for CID in self.excl])}
        return self


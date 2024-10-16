class Query:
    def __init__(self, table):
        self.table = table
        self.results = set()
        self.included = set()
        self.excluded = set()

    def __iter__(self):
        yield from self.results

    def select(self, *cids):
        yield from (tuple(self.table.get(eid, cid)
            for cid in cids)
            for eid in self)

    def where(self, *cids):
        self.included.update(cids)
        return self

    def unless(self, *cids):
        self.excluded.update(cids)
        return self

    def build(self):
        pools = (set(self.table.cmap[CID]) for CID in self.included if CID in self.table.cmap)
        results = set.intersection(*pools)
        self.results = {EID for EID in results if all((CID not in self.table.emap[EID] for CID in self.excluded))}
        return self


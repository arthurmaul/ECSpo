from uuid import uuid4
from copy import copy


class InvalidTag(Exception):
    pass


class InvalidPool(Exception):
    pass


class EntityDataNotFound(Exception):
    pass


class ComponentMapNotFound(Exception):
    pass


class Table:
    def __init__(self):
        self.emap = dict()
        self.cmap = dict()

    def spawn(self, EID=None):
        EID = EID or str(uuid4())
        self.emap[EID] = set()
        return EID
    
    def despawn(self, EID):
        for CID in self.emap[EID]:
            self.unset(CID, EID)
        self.emap.pop(EID)

    def pool(self, CID=None):
        CID = self.spawn(CID)
        self.cmap[CID] = dict()
        return CID

    def release(self, CID):
        if CID in self.cmap:
            for EID in self.cmap[CID]:
                self.unset(EID, CID)
            self.cmap.pop(CID)
        self.despawn(CID)

    def set(self, EID, CID, obj):
        if CID not in self.cmap:
            raise InvalidPool(f"Attempted pool operation on entity {EID} with tag component {CID}.")
        self.cmap[CID][EID] = obj
        self.emap[EID].add(CID)

    def unset(self, EID, CID):
        if CID not in self.cmap:
            raise InvalidPool(f"Attempted pool operation on entity {EID} with tag component {CID}.")
        self.cmap[CID].pop(EID)
        self.emap[EID].remove(CID)

    def tag(self, EID, CID):
        if CID in self.cmap:
            raise InvalidTag(f"Attempted tag operation on entity {EID} with pool component {CID}.")
        self.emap[EID].add(CID)

    def untag(self, EID, CID):
        if CID in self.cmap:
            raise InvalidTag(f"Attempted tag operation on entity {EID} with pool component {CID}.")
        self.emap[EID].remove(CID)

    def get(self, EID, CID):
        if not CID in self.cmap:
            raise ComponentMapNotFound(f"Component of type {CID} not found in the component map")
        if not EID in self.cmap[CID]:
            raise EntityDataNotFound(f"No associated component of type {CID} found for entity {EID}.")
        return self.cmap[CID][EID]

    def copy(self, EID1, EID2):
        for CID in self.emap[EID1]:
            if CID not in self.cmap:
                continue
            self.set(EID2, CID, copy(self.get(EID1, CID)))

    def clone(self, EID1, EID2=None):
        EID = self.spawn(EID2)
        self.copy(EID1, EID)
        return EID


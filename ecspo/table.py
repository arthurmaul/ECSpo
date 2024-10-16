from uuid import uuid4
from copy import copy


class InvalidEntity(TypeError):
    pass


class EntityNotFound(KeyError):
    pass


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
        try:
            self.emap[EID] = set()
        except TypeError:
            raise InvalidEntityId(f"The entity ID {EID} is not hashable. Try using a string or an integer ID instead.")
        return EID
    
    def despawn(self, EID):
        try:
            for CID in self.emap[EID]:
                self.unset(CID, EID)
        except KeyError:
            raise EntityNotFound(f"The entity ID {EID} was not found in the entity map. Make sure it was spawned, and not despawned twice.")
        self.emap.pop(EID)

    def pool(self, CID=None):
        CID = self.spawn(CID)
        try:
            self.cmap[CID] = dict()
        except KeyError:
            ...
        return CID

    def release(self, CID):
        if CID in self.cmap:
            try:
                for EID in self.cmap[CID]:
                    self.unset(EID, CID)
            except KeyError:
                raise ComponentNotFound(f"The component with entity ID {CID} was not found in the entity map. Did you forget to create it?")
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


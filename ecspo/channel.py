from uuid import uuid4


class RecursiveSubscription(Exception):
    ...


class Channel:
    def __init__(self, *responders, ID=None):
        self.ID = ID or str(uuid4())
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
            raise RecursiveSubscription(f"Recursive signal to {self.ID} channel was detected (likely caused by the channel having itself as one of the responders or one of the responder channels had this channel as a responder)")
        self.active = True
        response = [responder.emit(*args, **kwargs)
            if isinstance(responder, type(self))
            else responder(*args, **kwargs)
            for responder in self.responders]
        self.active = False
        return response


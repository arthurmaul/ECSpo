from uuid import uuid4


class RecursiveConnection(Exception):
    ...


class Channel:
    def __init__(self, *recievers):
        self.recievers = list(recievers)
        self.active = False
        
    def __iter__(self):
        yield from self.recievers

    def __call__(self, reciever):
        self.connect(reciever)
        return reciever
        
    def connect(self, reciever):
        self.recievers.append(reciever)
        return self
        
    def emit(self, *args, **kwargs):
        if self.active:
            raise RecursiveConnection(f"Ensure neither the channel itself or any of its reciever channels have this channel as a reciever.")
        self.active = True
        response = [reciever.emit(*args, **kwargs)
            if isinstance(reciever, type(self))
            else reciever(*args, **kwargs)
            for reciever in self.recievers]
        self.active = False
        return response


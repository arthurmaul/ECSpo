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

    def leave(self):
        context.remove(self)
        self.running = False

def leave():
    context[-1].leave()

def change(scene):
    context[-1] = scene

def shutdown():
    for scene in context.copy():
        scene.leave()


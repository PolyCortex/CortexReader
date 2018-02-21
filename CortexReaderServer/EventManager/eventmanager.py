from events import Event, EventTypes

class EventManager:
    def updateManagedEvents(self):
        pss
    def notify(self, event, *params):
        self.events[event](*params)
    def register_event(self, event):
        self.events.append(event)
    def __init__(self):
        self.events = []
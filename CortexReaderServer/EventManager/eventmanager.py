from events import Event, EventTypes, UpdateTypes

class EventManager:
    def updateManagedEvents(self, indice):
        self.updateEvent[self._events[indice].update()]()

    def reset_event(self, indice):
       self._events[indice].reset()

    def remove_event(self, indice):
         self._events.remove(indice)

    def notify(self, event, *params):
        indices = [i for i, x in enumerate(self._events) if x == event]
        for i in indices:
            self._events[i].emit(*params)
            self.updateManagedEvents(i)

    def register_event(self, event):
        self._events.append(event)

    def __init__(self):
        self._events = []
        self.updateEvent = {
            UpdateTypes.RESET : self.reset,
            UpdateTypes.REMOVE : self.remove
        }
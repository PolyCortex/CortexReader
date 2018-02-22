from events import Event, EventTypes, UpdateTypes

class EventManager:
    def updateManagedEvents(self, event):
        self.updateEvent[event.update()]()

    def reset_event(self, indice):
       self._events[indice].reset()

    def remove_event(self, event):
         self._events.remove(indice)
         
    def emit_specific(self, event, *params):
        for callBack in self._events[event]:
            callBack(*params)
        self.updateManagedEvents(event)

    def emit_type(self, eventType, *params):
        for event, callBacks in self._events.items():
            if event._Type == eventType:
                for callBack in callBacks:                
                    callBack(*params)
            
    
    def register_to_specific_event(self, event, callBack):
        if self._events[event] is None:
             self._events[event] = []
        self._events[event].append(callBack)

    def register_to_a_type_of_event(self,eventType, callBack):
        if self._types_of_events[eventType] is None:
             self._types_of_events[eventType] = []
        self._events[event].append(callBack)

    def __init__(self):
        self._specific_events = {}
        self._types_of_events = {}
        self.updateEvent = {
            UpdateTypes.RESET : self.reset_event,
            UpdateTypes.REMOVE : self.remove_event
        }
from .events import EventTypes, UpdateTypes
from Utilities.singleton import Singleton
from threading import Lock

class EventManager(metaclass=Singleton):
    #ATTENTION POURRAIT CAUSER DATA RACE
    def updateManagedEvents(self, event):
        self.updateEvent[event._updateType](event)
    #ATTENTION POURRAIT CAUSER DATA RACE
    def reset_event(self, event):
        self._specific_events[event].reset()
    #ATTENTION POURRAIT CAUSER DATA RACE
    def remove_event(self, event):
        if event in self._specific_events:
            self._specific_events.pop(event)
         
    def emit_specific(self, event, *params):
        self._mutex.acquire()
        for callBack in self._specific_events[event]:
            callBack(*params)
        self._mutex.release()
        self.emit_type(event._type, *params)
        self.updateManagedEvents(event)

    def emit_type(self, eventType, *params):
        self._mutex.acquire()
        for _eventType, callBacks in self._types_of_events.items():
            if _eventType == eventType:
                for callBack in callBacks:                
                    callBack(*params)
        self._mutex.release()
     
    def register_to_specific_event(self, event, callBack):
        self._mutex.acquire()
        if event not in self._specific_events:
            self._specific_events[event] = []
        self._specific_events[event].append(callBack)
        self._mutex.release()

    def register_to_a_type_of_event(self,eventType, callBack):
        self._mutex.acquire()
        if eventType not in self._types_of_events:
             self._types_of_events[eventType] = []
        self._types_of_events[eventType].append(callBack)
        self._mutex.release()

    def __init__(self):
        self._mutex = Lock()
        self._specific_events = {}
        self._types_of_events = {}
        self.updateEvent = {
            UpdateTypes.RESET : self.reset_event,
            UpdateTypes.REMOVE : self.remove_event
        }
import abc
from enum import Enum, unique
@unique 
class UpdateTypes(Enum):
    RESET = 0
    REMOVE = 1
    
@unique
class EventTypes(Enum):
    ARRAY_READY =0

from .eventmanager import EventManager
class Event(abc.ABC):

    def reset(self):
        print('please implement if I ever were to be triggered which I don\'t think should happen for now')
    @abc.abstractmethod
    def notify(self, *params):
        pass
    def __init__(self, eventType=None, updateType=None):        
        self._type = EventTypes(eventType)
        if updateType is not None:
            self._updateType = UpdateTypes(updateType)
        self._eventManager = EventManager()

import abc
from enum import Enum, unique

@unique 
class UpdateTypes(Enum):
    RESET = 0
    REMOVE = 1
@unique
class EventTypes(Enum):
    ARRAY_IS_READY = 0
    TIMER_EVENT = 1 


class Event(abc.ABC):
    @abc.abstractmethod
    def reset(self):
        pass
    @abc.abstractmethod
    def notify(self, *params):
        pass
    def __init__(self, eventType, updateType ):
        self._type = EventTypes(eventType)
        self._updateType = UpdateTypes(updateType)
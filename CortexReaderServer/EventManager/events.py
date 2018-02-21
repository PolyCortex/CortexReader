import abc
from enum import Enum, unique

@unique 
class UpdateTypes(Enum):
    RESET = 0
    REMOVE = 1
@unique
class EventTypes(Enum):
    ARRAY_IS_READY = 0
    TIME_EVENT = 1 
#ETCETERA

class Event(abc.ABC):
    @abc.abstractmethod
    def reset(self):
        pass
    @abc.abstractmethod
    def emit(self, *params):
        pass
    def __init__(self, event_type, updateType ):
        self._type = EventTypes(even_type)
        self._updateType = updateType
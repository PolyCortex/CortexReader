import abc
from enum import Enum, unique
@unique 
class UpdateTypes(Enum):
    RESET = 0
    REMOVE = 1
    
@unique
class EventTypes(Enum):
    PIPELINE_RECORD_PREPROCESS_ARRAY_READY = 0
    PIPELINE_PREPROCESS_GUI_ARRAY_READY = 1
    #GPIO_EVENT = 1


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

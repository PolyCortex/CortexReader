#Data type that describes what a single gpio input element looks like
from BaseDataType import BaseDataType
from EventManager.events import *
from EventManager.eventmanager import *

class GPIOInput(BaseDataType):
    def touch(self):
        pass 
        
    #def notify(self, *params):
        #EventManager().emit_type(self._type, self)

    def __init__(self, value, TTL):
        BaseDataType.__init__(self)
        #Event.__init__(self, EventTypes.GPIO_EVENT)
        self._value = value
        self.time_to_leave = TTL
#Data type that describes what a single gpio input element looks like
from BaseDataType import BaseDataType

class GPIOInput(BaseDataType):
    def touch(self):
        pass 
    def __init__(self, value, TTL):
        BaseDataType.__init__(self)
        self._value = value
        self.time_to_leave = TTL
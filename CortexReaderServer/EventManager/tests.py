from eventManager import *
from events import *

class testEvent(Event):
    def reset(self):
        self.value = 0
    def notify(self, *params):
        self.value = params[0]
    def __init__(self, value, eventType, updateType):
        Event.__init__(eventType, updateType)
        self.value = value
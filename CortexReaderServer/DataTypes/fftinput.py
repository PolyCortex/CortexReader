#Data type that describes what a single fft element looks like
from BaseDataType import BaseDataType

class FFTInput(BaseDataType):
    def __init__(self, value):
        BaseDataType.__init__(self)
        self._value = value
#Contains the main structure of the pipeline that we will have the ability to heritate from
import abc
from threading import Lock
class BasePipelineStage:
    def __init__(self ):
        self._array_shared = []
        self._mutex = Lock()
    @abc.abstractmethod
    def get_array(self):
        pass
    def swap_array(self, array):
        self._mutex.acquire()
        tmp = self._array_shared
        self._array_shared = array
        array = tmp
        self._mutex.release()

class PipelineRecordPreprocess(metaclass=Singleton, BasePipelineStage):
    def get_array(self):
        return self._array_shared
    def __init__(self, sampleFrequency):
        BasePipelineStage.__init__()
        self._sampleFrequency = sampleFrequency
        
        

#PipelineStage for preprocessing gpio inputs
from PipelineStages.BasePipeline import PipelineRecordPreprocess
from PipelineStages.BasePipeline import PipelinePreprocessGUI

from EventManager.events import *
from EventManager.eventmanager import *

class SamplePreProcessor:
    def fft(self):
        #IMPLEMENT FFT
        pass 
    def preprocess_data(self, value):
        self._pipelineStage.swap_array(self._unprocessed_array)
        #CATCH THE OUTPUT OR HANDLE WHATEVER
        self._data_Raw = self._unprocessed_array
        self._fft_data = self.fft()
        self._data_to_emit = self._data_Raw + self._fft_data
        self._unprocessed_array = []
        EventManager().emit_type(EventTypes.PIPELINE_PREPROCESS_GUI_ARRAY_READY)

    def __init__(self):
        self._unprocessed_array = []
        self._fft_data = []
        self._data_Raw = []
        EventManager().register_to_a_type_of_event(EventTypes.PIPELINE_RECORD_PREPROCESS_ARRAY_READY, self.preprocess_data)
        self._pipelineStage = PipelineRecordPreprocess()
        self._guiPipelineStage = PipelinePreprocessGUI()
        #EventManager().register_to_a_type_of_event(EventTypes.GPIO_EVENT, self.record)
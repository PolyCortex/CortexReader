#Will derive the base class and interconnect with the next stage in the pipeline
from PipelineStages.BasePipeline import PipelineRecordPreprocess
from EventManager.events import *
from EventManager.eventmanager import *
class Recorder:
    def record(self, value):
        #START RECORDING HERE ON SELF._GPIOADDRR
        if len(self._recording_array) > self._pipelineStage._sampleFrequency:
            self._pipelineStage.swap_array(self._recording_array)
            EventManager().emit_type(EventTypes.PIPELINE_RECORD_PREPROCESS_ARRAY_READY)
        self._recording_array.append(value)

    def __init__(self, gpio_addr):
        self._gpio_addr = gpio_addr
        self._recording_array = []
        self._pipelineStage = PipelineRecordPreprocess()
        #EventManager().register_to_a_type_of_event(EventTypes.GPIO_EVENT, self.record)
"""
Frame_sync block
Correlation method
"""

from readline import set_history_length
import numpy as np
from gnuradio import gr
import pmt

class Frame_sync(gr.basic_block):
    def __init__(self, SF=9, preamble_len = 6, frameLength = 18):
        gr.basic_block.__init__(self,
            name="LoRa Frame Detector",
            in_sig=[np.complex64,(np.complex64, round(pow(2,SF)*(preamble_len+2.25)))], # first input is the input signal, second is the preamble to be correlated with
            # out_sig=[(np.complex64,pow(2,SF))])
            out_sig=[(np.complex64)])
        self.SF = SF
        self.fullPreambleLength = round(pow(2,SF)*(preamble_len+2.25))
        self.frameLength = round(pow(2,SF)*(frameLength))
        set_history_length(self.fullPreambleLength)

    def forecast(self, noutput_items, ninputs) :
        ninput_items_required = [1]*ninputs #ninput_items_required[i] is the number of items that will be consumed on input port i
        return ninput_items_required

    def general_work(self, input_items, output_items):
        preamble_detected = False
        offset = 0

        #buffer references
        in0 = input_items[0] #input signal
        in1 = input_items[1] #preamble to be correlated with

        Corr = np.correlate(in0[:], in1[0])
        peak = np.max(Corr)
        peakIndex = np.argmax(Corr)
        threshold = 2000
        # print("\n--- Correlator ---")
        # print("Peak: ", peak)
        # print("Peak Index: ", peakIndex)
        # print("output_items[0]: ", len(output_items[0]))

        if peak > threshold :
            # print("peak > threshold")
            self.add_item_tag(0, self.nitems_written(0) + self.fullPreambleLength + peakIndex,  pmt.intern("preambleStart"),  pmt.intern(str(self.frameLength)))
            output_items[0][0:len(in0)] = in0[:len(output_items[0])]
            self.consume(0, len(in0[:len(output_items[0])]))
            # print("consumed: ", len(in0[:len(output_items[0])]))
            return len(in0[:len(output_items[0])])

        else :
            output_items[0][0:len(in0)] = in0[:len(output_items[0])]
            self.consume(0, len(in0[:len(output_items[0])]))
            # print("consumed: ", len(in0[:len(output_items[0])]))
            return len(in0[:len(output_items[0])])

        # if preamble_detected :
        #     print("preamble_detected")
        #     self.consume(0, offset) # consume till offset
        #     pass
        # else :
        #     print("preamble_NOT_detected")
        #     self.consume(0, self.in_len) # consume all input items
        #     return 0

        # # parsing in0 (convert + crop t
        # # to uint32
        # output_items[0][0:(self.CR+4)] = output_matrix.dot(1 << np.arange(output_matrix.shape[-1] - 1, -1, -1))

        # #consume inputs (should be SF)
        # self.consume(0, self.SF)
        # return self.CR+4
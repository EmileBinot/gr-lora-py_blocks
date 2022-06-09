"""
Frame sync block:
Tries to find a correlation peak between the input sequence and a reference sequence (preamble). If found, tag the end of preamble.

INPUTS:
    - in_sig[0]: IQ complex input stream
    - in_sig[1]: IQ complex reference vector (preamble)
OUTPUT:
    - out_sig[0]: IQ complex stream
"""


import numpy as np
from gnuradio import gr
import pmt

class Frame_sync(gr.basic_block):
    def __init__(self, SF=9, preamble_len = 6, frame_length = 18):
        gr.basic_block.__init__(self,
            name="LoRa Frame Detector",
            in_sig=[np.complex64,(np.complex64, round(pow(2,SF)*(preamble_len+2.25)))], # first input is the input signal, second is the preamble to be correlated with
            # out_sig=[(np.complex64,pow(2,SF))])
            out_sig=[(np.complex64)])
        self.SF = SF
        self.full_preamble_length = round(pow(2,SF)*(preamble_len+2.25))
        self.frame_length = round(pow(2,SF)*(frame_length))

    def forecast(self, noutput_items, ninputs) :
        ninput_items_required = [1]*ninputs #ninput_items_required[i] is the number of items that will be consumed on input port i
        return ninput_items_required

    def general_work(self, input_items, output_items):

        # buffer references
        in0 = input_items[0] # input signal
        in1 = input_items[1] # preamble to be correlated with
        out = output_items[0] # output buffer

        corr = np.correlate(in0[:], in1[0]) # correlate input signal with preamble
        peak = np.max(corr)                 # find the correlation peak
        threshold = 2000                    # threshold for peak detection

        # # debug
        # print("\n--- Correlator ---")
        # print("Peak: ", peak)
        # print("Peak Index: ", peakIndex)
        # print("output_items[0]: ", len(output_items[0]))

        if peak > threshold :
            # print("peak > threshold")
            peak_index = np.argmax(corr)         # get index of the peak
            # add tag at the end of the preamble, write frame_length inside so Tagged Stream Cropper block can remove preamble
            self.add_item_tag(0, self.nitems_written(0) + peak_index + self.full_preamble_length,  pmt.intern("preamble_end"),  pmt.intern(str(self.frame_length)))

        out[0:len(in0)] = in0[:len(out)]
        self.consume(0, len(in0[:len(out)]))
        return len(in0[:len(out)])
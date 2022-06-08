"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class Frame_sync(gr.sync_block):
    def __init__(self, SF=9, preamble_len = 6):
        gr.sync_block.__init__(self,
            name="LoRa Frame Detector",
            in_sig=[np.complex64,(np.complex64, round(pow(2,SF)*(preamble_len+2.25)))], # first input is the input signal, second is the preamble to be correlated with
            # out_sig=[(np.complex64,pow(2,SF))])
            out_sig=[(np.complex64)])
        self.SF = SF
        self.in_len = round(pow(2,SF)*(preamble_len+2.25))
        self.set_history(self.in_len)

    def work(self, input_items, output_items):
        #buffer references
        in0 = input_items[0] #input signal
        in1 = input_items[1] #preamble to be correlated with

        Corr = np.correlate(in0[:], in1[0])
        peak = np.max(Corr)
        peakIndex = np.argmax(Corr)
        threshold = 10
        print("\n--- Correlator ---")
        print("Peak: ", peak)
        print("Peak Index: ", peakIndex)
        print("output_items[0]: ", len(output_items[0]))
        print("consumed: ", len(in0))
        if peak > threshold :
            print("peak > threshold")
            # self.add_item_tag(0, peakIndex,  pmt.intern("key"),  pmt.intern("Value"))
            # output_items[0][0:len(in0)] = in0
            # self.consume(0, len(in0))
            # return len(in0)
        else :
            pass

        output_items[0][:] = input_items[0][:len(output_items[0])]
        return len(output_items[0])

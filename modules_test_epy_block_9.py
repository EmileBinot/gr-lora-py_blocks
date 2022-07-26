"""
LoRa Threshold Sync:
This block will add a tag 'threshold_exceeded' on the item indice that will be over the threshold

INPUT:
    - in_sig[0] : IQ complex items
OUTPUT:
    - out_sig[0]: IQ complex items, w/ tag added if > treshold
"""

import numpy as np
from gnuradio import gr
import pmt
import matplotlib.pyplot as plt

class blk(gr.sync_block):
    def __init__(self,preamble_nitems = 24, payload_nitems = 1, threshold = 10000):
        gr.sync_block.__init__(
            self,
            name='LoRa Threshold Sync',
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.preamble_nitems = preamble_nitems
        self.payload_nitems = payload_nitems
        self.threshold = threshold
        self.items_written0_old = 0

        self.state = 0 # 0 if searching for preamble, 1 if found
        self.set_output_multiple(self.preamble_nitems + self.payload_nitems + 1000)

    def work(self, input_items, output_items):

        in0 = input_items[0][:len(output_items[0])]
    
        if self.state == 0 :    # searching for preamble
            threshold_in0 = np.where(in0 > self.threshold)
            if len(threshold_in0[0]) > 0:
                self.state = 1
                tag_index = self.nitems_read(0) + threshold_in0[0][0]
                self.add_item_tag(0,tag_index,  pmt.intern("threshold_exceeded"),  pmt.intern(str(self.payload_nitems + self.preamble_nitems + 1000)))
                self.items_written0_old = self.nitems_written(0)

        if self.state == 1 :    # preamble found
            if self.nitems_written(0) - self.items_written0_old > self.payload_nitems*2:    
                self.state = 0  # if enough items have passed, reset self.state to 0
            pass

        output_items[0][:] = in0
        return len(output_items[0])

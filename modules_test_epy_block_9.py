"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import matplotlib.pyplot as plt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self,preamble_nitems = 24, payload_nitems = 1, threshold = 10000):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='LoRa Threshold Sync',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )

        
        self.preamble_nitems = preamble_nitems
        self.payload_nitems = payload_nitems
        self.threshold = threshold

        self.state = 0 # 0 if searching for preamble, 1 if found
        self.last_tag = 0

    def work(self, input_items, output_items):

        in0 = input_items[0][:len(output_items[0])]
        # plt.specgram(in0, NFFT=64, Fs=32, noverlap=8)
        # plt.show()

        if self.state == 0 : 
            # print('searching for preamble')
            for i in range(len(in0)) :
                if np.abs(in0[i]) > self.threshold and self.state == 0 :
                    # print("Threshold exceeded")
                    self.state = 1
                    tag_index = self.nitems_written(0) + i + self.preamble_nitems
                    self.last_tag = self.nitems_written(0) + i + self.preamble_nitems
                    self.add_item_tag(0,tag_index,  pmt.intern("payload_begin"),  pmt.intern(str(self.payload_nitems)))


        if self.state == 1 :
            if int(self.nitems_written(0)) - self.last_tag > self.payload_nitems:
                # print("Reset")
                self.state = 0
            pass



        output_items[0][:] = input_items[0]
        return len(output_items[0])

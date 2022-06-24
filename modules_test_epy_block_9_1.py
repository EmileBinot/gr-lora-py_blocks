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

class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self,preamble_nitems = 24, payload_nitems = 1, threshold = 10000):  # only default arguments here
        gr.basic_block.__init__(
            self,
            name='LoRa Threshold',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )

        
        self.preamble_nitems = preamble_nitems
        self.payload_nitems = payload_nitems
        self.threshold = threshold
        self.items_read0_old = 0

        self.state = 0 # 0 if searching for preamble, 1 if found
        self.last_tag = 0
        self.set_output_multiple(self.preamble_nitems + self.payload_nitems + 1000)

    def general_work(self, input_items, output_items):

        in0 = input_items[0][:len(output_items[0])]


        if self.state == 0 :
            threshold_in0 = np.where(in0 > self.threshold)
            if len(threshold_in0[0]) > 0:
                print("fast : ", threshold_in0[0][0])
                self.state = 1
                # tag_index = self.nitems_read(0) + threshold_in0[0][0]
                # self.add_item_tag(0,tag_index,  pmt.intern("threshold_exceeded"),  pmt.intern(str(self.payload_nitems + self.preamble_nitems + 1000 )))
                # self.last_tag = tag_index
                self.items_read0_old = self.nitems_read(0) + threshold_in0[0][0]
                # # # debug
                # vect = np.arange(0,len(in0))
                # plt.plot(vect, np.real(in0))
                # plt.axvline(threshold_in0[0][0], 0, 1, color = "red", label = "Corr peak idx")
                # # plt.specgram(in0, NFFT=64, Fs=32, noverlap=8)
                # plt.show()
                self.consume(0,threshold_in0[0][0])
                return 0

            else :
                self.consume(0,len(in0))
                return 0

                

        if self.state == 1 :

            if self.nitems_read(0) - self.items_read0_old > self.payload_nitems*2:
                print("Reset")
                self.state = 0
        
            output_items[0][:] = in0
            self.consume(0,len(in0))
            return len(output_items[0])

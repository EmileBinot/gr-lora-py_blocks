"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self, preamble_nitems = 4224, payload_nitems = 6144):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='LoRa Frame Constructor stream',   # will show up in GRC
            in_sig=[(np.complex64),(np.complex64)],
            out_sig=[(np.complex64)]
        )
        self.payload_nitems = payload_nitems
        self.preamble_nitems = preamble_nitems
        self.frame_counter = 0
        
    def general_work(self, input_items, output_items):
        if len(input_items[0]) >= self.preamble_nitems and len(input_items[1]) >= self.payload_nitems :
            in0 = input_items[0][:self.preamble_nitems]
            in1 = input_items[1][:self.payload_nitems]
            out = np.concatenate((in0,in1))
            output_items[0][:len(out)] = out[:len(output_items[0])]

            self.frame_counter += 1
            print("\n\n[TX] Constr. : Frame #%d sent" % (self.frame_counter))
            return len(output_items[0])
        else :
            return 0
        # out = np.concatenate((input_items[0][0],input_items[1][0]))
        # print(len(out))
        # output_items[0][:] = out
        

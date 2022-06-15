"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, preamble_nitems = 4224, payload_nitems = 6144):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='LoRa Frame Constructor',   # will show up in GRC
            in_sig=[(np.complex64,preamble_nitems),(np.complex64,payload_nitems)],
            out_sig=[(np.complex64,preamble_nitems+payload_nitems)]
        )
        self.payload_nitems = payload_nitems
        self.preamble_nitems = preamble_nitems
        self.frame_counter = 0
        
    def work(self, input_items, output_items):
        # output_items[0][:] = input_items[0]
        # out = np.concatenate((input_items[0],input_items[1]),axis=1)
        # print(len(input_items[0][0]))
        # print(len(input_items[1][0]))
        if len(input_items[0][0]) == self.preamble_nitems and len(input_items[1][0]) == self.payload_nitems :
            output_items[0][:] = np.concatenate((input_items[0],input_items[1]),axis=1)
            self.frame_counter += 1
            print("\n\n[TX] Constr. : Frame #%d sent" % (self.frame_counter))
            return len(output_items[0])
        else :
            return 0
        # out = np.concatenate((input_items[0][0],input_items[1][0]))
        # print(len(out))
        # output_items[0][:] = out
        

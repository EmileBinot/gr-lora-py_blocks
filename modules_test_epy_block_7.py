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

    def __init__(self, preamble_nitems = 2, payload_nitems = 2):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[(np.complex64,4224),(np.complex64,6144)],
            out_sig=[(np.complex64, 6144 + 4224)]
        )
        self.preamble_nitems = preamble_nitems
        self.payload_nitems = payload_nitems


    def work(self, input_items, output_items):
        """example: multiply with constant"""

        
        # print("\n\ninput_items[1].shape: ", input_items[1].shape)
        frame = np.concatenate((input_items[0][:],input_items[1][:]), axis=1)

        print("\n\n -- mux --")
        print("\n\ninput_items[0]: ", input_items[0])
        print("\n\nframe : ", frame)
        output_items[0][:] = frame
        return len(output_items[0])

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

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.frame_counter = 0
        self.state=0

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        threshold_up = 0.5
        threshold_down = 0.005

        for i in range(len(input_items[0])):       
            if np.abs(input_items[0][i]) > threshold_up and self.state == 0:
                print("[RX] Correl. : Frame #%d received" % (self.frame_counter))
                self.frame_counter += 1
                self.state = 1
            
            if np.abs(input_items[0][i]) < threshold_down and self.state == 1:
                self.state = 0



        output_items[0][:] = input_items[0]
        return len(output_items[0])

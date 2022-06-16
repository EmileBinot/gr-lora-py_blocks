"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):
    def __init__(self, preamble_nitems = 4224, payload_nitems = 6144):
        gr.sync_block.__init__(
            self,
            name='LoRa EoB Tagger',
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.payload_nitems = payload_nitems
        self.preamble_nitems = preamble_nitems

    def work(self, input_items, output_items):

        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        for tag in tags:
            key = pmt.to_python(tag.key) # convert from PMT to python string
            value = pmt.to_python(tag.value) # Note that the type(value) can be several things, it depends what PMT type it was

            key = pmt.intern("tx_eob")
            value = pmt.from_bool(True)
            self.add_item_tag(0, # Write to output port 0
                    self.nitems_written(0) + self.payload_nitems+self.preamble_nitems-1, # Index of the tag in absolute terms
                    key, # Key of the tag
                    value # Value of the tag
            )
        output_items[0][:] = input_items[0]

        return len(output_items[0])

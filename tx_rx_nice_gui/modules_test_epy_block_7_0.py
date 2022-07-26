"""
LoRa EoB tagger:
Add tx_eob (End Of Burst) tag to the LoRa frame
References : https://wiki.gnuradio.org/index.php/USRP_Sink

INPUT:
    - in_sig[0] : IQ complex items, length = preamble_nitems+payload_nitems (= FRAME)
OUTPUT:
    - out_sig[0]: IQ complex items, length = preamble_nitems+payload_nitems (= FRAME) with tag added
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):
    def __init__(self, preamble_nitems = 4224, payload_nitems = 8192):
        gr.sync_block.__init__(
            self,
            name='LoRa EoB Tagger',
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.payload_nitems = payload_nitems
        self.preamble_nitems = preamble_nitems
        self.frame_counter = 0

    def work(self, input_items, output_items):

        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        for tag in tags:
            if pmt.to_python(tag.key) == "tx_sob" :
                key = pmt.intern("tx_eob")  # when 'tx_sob' tag detected, add 'tx_eob' tag at the end of frame
                value = pmt.from_bool(True)
                self.add_item_tag(0,
                        self.nitems_written(0) + self.payload_nitems+self.preamble_nitems-1, # Index of the tag in absolute terms
                        key,
                        value
                )
                self.frame_counter += 1
        output_items[0][:] = input_items[0]

        return len(output_items[0])

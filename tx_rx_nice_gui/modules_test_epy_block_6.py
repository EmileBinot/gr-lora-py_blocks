"""
LoRa Frame Constructor:
Concatenate preamble and payload items + add tags for USRP Bursty transmission use 
References : https://wiki.gnuradio.org/index.php/USRP_Sink

KNOWN BUGS :
    - changing preamble_nitems and/or payload_nitems values in the GRC flowgraph will not work ! If you want to change their value, do it here. (https://github.com/gnuradio/gnuradio/issues/4196)

INPUT:
    - in_sig[0] : IQ complex vector, length =  preamble_nitems (= PREAMBLE)
    - in_sig[1] : IQ complex vector length = payload_nitems (= PAYLOAD)
OUTPUT:
    - out_sig[0]: IQ complex vector, length = preamble_nitems+payload_nitems (= FRAME)
"""

import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self, preamble_nitems = 4224, payload_nitems = 8192):  # only default arguments here
        self.payload_nitems = payload_nitems
        self.preamble_nitems = preamble_nitems
        self.frame_counter = 0
        gr.sync_block.__init__(
            self,
            name='LoRa Frame Constructor',   # will show up in GRC
            in_sig=[(np.complex64,self.preamble_nitems),(np.complex64,self.payload_nitems)],
            out_sig=[(np.complex64,self.preamble_nitems+self.payload_nitems)]
        )
        self.message_port_register_out(pmt.intern("msg_out"))
        
        
    def work(self, input_items, output_items):

        # verify vectors length
        if len(input_items[0][0]) == self.preamble_nitems and len(input_items[1][0]) == self.payload_nitems :
            # concatenate preamble with payload symbols
            output_items[0][:] = np.concatenate((input_items[0],input_items[1]),axis=1)
            
            # TAGS
            key = pmt.intern("tx_sob")
            value = pmt.from_bool(True)
            self.add_item_tag(0, # Write to output port 0
                    self.nitems_written(0), # Index of the tag in absolute terms
                    key, # Key of the tag
                    value # Value of the tag
            )

            # tx_time tag is optional : https://discuss-gnuradio.gnu.narkive.com/c2r83OZW/uhd-usrp-sink-stream-tagging

            key = pmt.intern("packet_len")
            value = pmt.from_long(self.preamble_nitems+self.payload_nitems)
            self.add_item_tag(0, # Write to output port 0
                    self.nitems_written(0), # Index of the tag in absolute terms
                    key, # Key of the tag
                    value # Value of the tag
            )

            self.frame_counter += 1
            print("\n\n[TX] Constr. : Frame #%d sent" % (self.frame_counter))
            PMT_msg = pmt.cons(pmt.intern("frame_nbr"), pmt.from_long(self.frame_counter))
            self.message_port_pub(pmt.intern("msg_out"), PMT_msg)

            return len(output_items[0])
        else :
            return 0

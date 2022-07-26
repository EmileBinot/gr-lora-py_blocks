"""
Gray coding block
A gray coding is a mapping between a symbol in any numeric representation to a binary sequence. e
particularity of the obtained binary sequence is that adjacent symbols in the original representation only
differ by one bit in the gray representation.
Reference : https://www.epfl.ch/labs/tcl/wp-content/uploads/2020/02/Reverse_Eng_Report.pdf

INPUT:
    - in_sig[0]: CR int32 input sequence (symbols)
OUTPUT:
    - out_sig[0]: CR int32 input sequence (symbols)
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):

    def __init__(self, SF=1):
        gr.sync_block.__init__(
            self,
            name='LoRa Gray Rx',
            in_sig=[np.int32],
            out_sig=[np.int32]
        )
        self.SF = SF

    def work(self, input_items, output_items):
        in0 = input_items[0][:len(output_items[0])]
        out = output_items[0]

        for i in range(len(out)):
            out[i] = in0[i]
            for j in range(1,self.SF):
                out[i]= out[i] ^ (in0[i] >> j)
        return len(output_items[0])

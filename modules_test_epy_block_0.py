"""
Deinterleaving block
Inverse of interleaving block.
Reference : "Towards an SDR implementation of LoRa..." 2020 A.Marquet, N.Montavont, G.Papadopoulos)

INPUT:
    - in_sig[0]: CR int32 input sequence (symbols)
OUTPUT:
    - out_sig[0]: SF bytes output sequence (4+CR useful bits per byte)
"""

import numpy as np
from gnuradio import gr
import pmt

class Deinterleaver(gr.basic_block):
    def __init__(self, SF=9, CR=2):
        gr.basic_block.__init__(self,
            name="LoRa Deinterleaver",
            in_sig=[np.uint32],
            out_sig=[np.uint8])
        self.SF = SF
        self.CR = CR
        self.set_tag_propagation_policy(gr.TPP_DONT)

    def forecast(self, noutput_items, ninputs) :
        #ninput_items_required[i] is the number of items that will be consumed on input port i
        ninput_items_required = [self.CR+4]*ninputs # we need CR+4 items to produce anything
        return ninput_items_required

    def general_work(self, input_items, output_items):
        
        tags = self.get_tags_in_window(0, 0, len(input_items[0]))
        for tag in tags:
            key = pmt.to_python(tag.key)
            value = pmt.to_python(tag.value)
            self.add_item_tag(0, self.nitems_written(0), tag.key, tag.value)

        if(len(input_items[0]) >= self.CR+4) :  # if we have enough items to process

            in0 = input_items[0][:self.CR+4]    # input buffer reference

            # formatting the input buffer
            input_matrix = np.zeros((self.CR+4, self.SF), dtype=np.uint8)
            for i in range(len(in0)):
                bits_crop = [int(x) for x in bin(in0[i])[2:]]                                   # convert to binary         
                input_matrix[i][:] = ([0]*(self.SF-len(bits_crop)) + bits_crop)[-(self.SF):]    # crop to SF bits

            # deinterleaving
            output_matrix = np.zeros((self.SF, self.CR+4), dtype=np.uint8)
            for i in range(0,(self.SF)) :
                for j in range(0,(self.CR+4)) :
                    idi=self.CR+4-1-j
                    idj=(self.SF-1-i+(self.CR+4)-1-j)%self.SF
                    output_matrix[i][j]=input_matrix[idi][idj]

            # to uint32
            output_items[0][0:(self.SF)] = output_matrix.dot(1 << np.arange(output_matrix.shape[-1] - 1, -1, -1))

            self.consume(0, self.CR+4)  # consume inputs (should be CR+4)
            return self.SF              # return produced outputs (should be SF)

        else :
            return 0
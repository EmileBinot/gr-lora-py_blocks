"""
Interleaving block
Scrambles bits together to fight error bursts.
Reference : "Towards an SDR implementation of LoRa..." 2020 A.Marquet, N.Montavont, G.Papadopoulos)
"""

import numpy as np
from gnuradio import gr

class Interleaver(gr.basic_block):
    def __init__(self, SF=9, CR=4):
        gr.basic_block.__init__(self,
            name="Deiterleaver",
            in_sig=[np.uint32],
            out_sig=[np.uint8])
        self.SF = SF
        self.CR = CR

    def forecast(self, noutput_items, ninputs) :
        ninput_items_required = [self.CR+4]*ninputs #ninput_items_required[i] is the number of items that will be consumed on input port i
        return ninput_items_required

    def general_work(self, input_items, output_items):
        
        if(len(input_items[0]) >= self.CR+4) :

            #buffer references
            in0 = input_items[0][:self.CR+4]

            # parsing in0 (convert + crop to CR+4 lines of SF bits and bundle in matrix)
            input_matrix = np.zeros((self.CR+4, self.SF), dtype=np.uint8)
            for i in range(len(in0)):
                bits_crop = [int(x) for x in bin(in0[i])[2:]]        
                bits_crop_norm = ([0]*(self.SF-len(bits_crop)) + bits_crop)[-(self.SF):]
                input_matrix[i][:] = np.asarray(bits_crop_norm, dtype=np.uint8)

            # deinterleaving
            output_matrix = np.zeros((self.SF, self.CR+4), dtype=np.uint8)
            for i in range(0,(self.SF)) :
                for j in range(0,(self.CR+4)) :
                    idi=self.CR+4-1-j
                    idj=(self.SF-1-i+(self.CR+4)-1-j)%self.SF
                    output_matrix[i][j]=input_matrix[idi][idj]


            # to uint32
            output_items[0][0:(self.SF)] = output_matrix.dot(1 << np.arange(output_matrix.shape[-1] - 1, -1, -1))

            # debug
            print("\n--- GENERAL WORK : DEINTERLEAVER ---")
            print("in0 :")
            print(in0)
            print("len(in0) (should be CR+4): ")
            print(len(in0))
            print("input_matrix (CR+4 x SF):")
            print(input_matrix)
            print("output_matrix (SF x CR+4 ):")
            print(output_matrix)
            print("output_items[0] = ")
            print(output_items[0][0:(self.SF)])
            print("return len(output_items[0]) (should be CR+4): ")
            print(len(output_items[0]))

            self.consume(0, self.CR+4)
            # self.produce(0, self.SF-1)
            return self.SF

        else :
            return 0




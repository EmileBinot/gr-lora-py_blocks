"""
Hamming encoding block
Forward Error Correction encoding block
Reference : "Towards an SDR implementation of LoRa..." 2020 A.Marquet, N.Montavont, G.Papadopoulos)
"""

import numpy as np
from gnuradio import gr


class Hamming_enc(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self, CR = 4):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='LoRa Hamming Tx',   # will show up in GRC
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.CR = CR

    def work(self, input_items, output_items):
        
        in0 = input_items[0]
        out = output_items[0]
    
        # Hamming encoding (iterate over matrix lines and encode each)
        output_matrix = np.zeros((len(in0), 4+self.CR), dtype=np.uint8)
        input_matrix = np.zeros((len(in0), 4), dtype=np.uint8)
        for i in range(len(in0)):

            # parsing in0 (convert + crop to lines of 4 bits and bundle in matrix)
            bits_crop = [int(x) for x in bin(in0[i])[2:]] 
            print(bits_crop)      
            bits_crop_norm = ([0]*(4-len(bits_crop)) + bits_crop)[-(4):]
            input_matrix[i][:] = np.asarray(bits_crop_norm, dtype=np.uint8)

            if self.CR == 1:
                p0 = input_matrix[i][0] ^ input_matrix[i][1] ^ input_matrix[i][2] ^ input_matrix[i][3]
                output_matrix[i] = np.asarray([input_matrix[i][0], input_matrix[i][1], input_matrix[i][2], input_matrix[i][3], p0], dtype=np.uint8)

            if self.CR == 2:
                p0 = input_matrix[i][0] ^ input_matrix[i][1] ^ input_matrix[i][2]
                p1 = input_matrix[i][1] ^ input_matrix[i][2] ^ input_matrix[i][3]
                output_matrix[i] = np.asarray([input_matrix[i][0], input_matrix[i][1], input_matrix[i][2], input_matrix[i][3], p1, p0], dtype=np.uint8)

            if self.CR == 3:
                Q = np.array([[0,1,1,1], [1,1,0,1], [1,1,1,0], [1,0,1,1]], np.uint8)
                Id = np.identity(4, dtype=np.uint8)
                G = np.concatenate((Id, Q),axis=1)
                output_matrix[i] = (np.dot(input_matrix[i],G)%2)[0:4+self.CR]

            if self.CR == 4:
                Q = np.array([[0,1,1,1], [1,1,0,1], [1,1,1,0], [1,0,1,1]], np.uint8)
                Id = np.identity(4, dtype=np.uint8)
                G = np.concatenate((Id, Q),axis=1)
                output_matrix[i] = (np.dot(input_matrix[i],G)%2)

        # convert output matrix to uint8
        out[:] = output_matrix.dot(1 << np.arange(output_matrix.shape[-1] - 1, -1, -1))

        #debug
        print("\n--- GENERAL WORK : HAMMING_ENC ---")
        print("in0 :")
        print(in0)
        print("input_matrix :")
        print(input_matrix)
        print("output_matrix :")
        print(output_matrix)
        print("out :")
        print(out)
        print("--- HAMMING_ENC END---")

        return len(output_items[0])

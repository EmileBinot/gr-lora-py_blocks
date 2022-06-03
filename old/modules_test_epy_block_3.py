"""
Hamming Decoding block
Forward Error Correction encoding block
Reference : "Towards an SDR implementation of LoRa..." 2020 A.Marquet, N.Montavont, G.Papadopoulos)
"""

import numpy as np
from gnuradio import gr


class Hamming_dec(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self, CR = 4):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Hamming_dec',   # will show up in GRC
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.CR = CR

    def decode(self, input_vect, CR_loc) : 

        output=input_vect

        if CR_loc == 1:
            syndrome = input_vect[0] ^ input_vect[1] ^ input_vect[2] ^ input_vect[3] ^ input_vect[4]
            output = input_vect

        if CR_loc == 2:
            syndrome = np.zeros((2,1), dtype=np.uint8)
            syndrome[0] = input_vect[0] ^ input_vect[1] ^ input_vect[2] ^ input_vect[5]
            syndrome[1] = input_vect[1] ^ input_vect[2] ^ input_vect[3] ^ input_vect[4]
            output = input_vect

        if CR_loc == 3:
            n = 4+CR_loc
            k = 4
            Q = np.array([[0,1,1], [1,1,0], [1,1,1], [1,0,1]], np.uint8)
            Id = np.identity(n-k, dtype=np.uint8)
            H = np.concatenate((Q.transpose(), Id),axis=1)
            syndrome = np.dot(input_vect[:], H.transpose())%2

            tmp = np.zeros((1,n-k+4), dtype=np.uint8)
            tmp2 = np.identity(n-k+4, dtype=np.uint8)
            E = np.concatenate((tmp, tmp2),axis=0)
            S = np.dot(E,H.transpose())%2

            # if(syndrome[0] == 1 or syndrome[1] == 1):
            #     print("Error detected, correcting...")

            for j in range(S.shape[1]):
                if np.array_equal(S[j],syndrome):
                    output = input_vect ^ E[j][:]


        if CR_loc == 4:
            n = 4+CR_loc
            k = 4
            Q = np.array([[0,1,1,1], [1,1,0,1], [1,1,1,0], [1,0,1,1]], np.uint8)
            Id = np.identity(n-k, dtype=np.uint8)
            H = np.concatenate((Q.transpose(), Id),axis=1)
            syndrome = np.dot(input_vect[:], H.transpose())%2
            if np.array_equal(syndrome,np.array([0,0,0,0])):
                output = input_vect
                # print("no error detected")

            else :
                parity = input_vect[0] ^ input_vect[1] ^ input_vect[2] ^ input_vect[3] ^ input_vect[4] ^ input_vect[5] ^ input_vect[6] ^ input_vect[7]

                if parity :
                    # print("1 error detected, sending to hamming(7,3)")
                    output = self.decode(input_vect[:][0:7], 3)
                # else :
                    # print("2 errors detected")
                
        
        return output[:][0:4]

    def work(self, input_items, output_items):

        in0 = input_items[0]
        out = output_items[0]
    
        # Hamming encoding (iterate over matrix lines and encode each)
        output_matrix = np.zeros((len(in0), 4), dtype=np.uint8)
        input_matrix = np.zeros((len(in0), 4+self.CR), dtype=np.uint8)

        for i in range(len(in0)):

            # parsing in0 (convert + crop to lines of 4 bits and bundle in matrix)
            bits_crop = [int(x) for x in bin(in0[i])[2:]]        
            bits_crop_norm = ([0]*(self.CR+4-len(bits_crop)) + bits_crop)[-(self.CR+4):]
            input_matrix[i][:] = np.asarray(bits_crop_norm, dtype=np.uint8)

            output_matrix[i][:] = self.decode(input_matrix[i][:],self.CR)


        # convert output matrix to uint8
        out[:] = output_matrix.dot(1 << np.arange(output_matrix.shape[-1] - 1, -1, -1))

        # debug
        # print("\n--- GENERAL WORK : HAMMING_DEC ---")
        # print("in0 :")
        # print(in0)
        # print("input_matrix :")
        # print(input_matrix)
        # print("output_matrix :")
        # print(output_matrix)
        # print("out :")
        # print(out)


        return len(output_items[0])

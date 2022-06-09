"""
Preamble Generation Block:
Reference : "Towards an SDR implementation of LoRa..." 2020 A.Marquet, N.Montavont, G.Papadopoulos)

INPUT:
    - None
OUTPUT:
    - out_sig[0]: IQ complex vector, length = M * os_factor * (preamble_len + 2.25)
"""

import numpy as np
from gnuradio import gr
import math

def modulate_vect(SF, id, os_factor) :
    M  = pow(2,SF)
    chirp = np.zeros((len(id),M*os_factor), dtype=np.complex64)

    for i in range(len(id)) :
        n_fold = M * os_factor - id[i] * os_factor
        for n in range(0,M*os_factor):
            if n < n_fold:
                chirp[i][n] = np.exp(2j*math.pi *(n*n/(2*M)/pow(os_factor,2)+(id[i]/M-0.5)*n/os_factor))
            else:
                chirp[i][n] = np.exp(2j*math.pi *(n*n/(2*M)/pow(os_factor,2)+(id[i]/M-1.5)*n/os_factor))
    return chirp

class PreambleGenerator(gr.sync_block):

    def __init__(self, SF = 9, preamble_len = 6):
        gr.sync_block.__init__(
            self,
            name='LoRa Preamble Generator',
            in_sig=None,
            out_sig=[(np.complex64,round(pow(2,SF)*(preamble_len+2.25)))]   # !!! will cause problem if os_factor > 1 !!! 
        )
        self.SF = SF
        self.preamble_len = preamble_len

    def work(self, input_items, output_items):

        preamble_up = np.reshape(modulate_vect(self.SF, [0]*self.preamble_len, 1), -1)      # generate preamble_len upchirps
        preamble_down = np.reshape(np.conjugate(modulate_vect(self.SF, [0]*3, 1)), -1)      # generate 3 downchirps
        preamble = np.concatenate((preamble_up, preamble_down[0:int(2.25*pow(2,self.SF))])) # concatenate preamble_up and preamble_down[0:2.25*M]
        output_items[0][0] = np.reshape(preamble,-1)                                        # reshape preamble to a vector

        return len(output_items[0])
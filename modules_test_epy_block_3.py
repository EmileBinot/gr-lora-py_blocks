"""
Modulation Block:
"""

import numpy as np
from gnuradio import gr
import math

def modulate(SF, id, os_factor) :
    M  = pow(2,SF)
    chirp = np.zeros((len(id),M*os_factor), dtype=np.complex64)

    for i in range(len(id)) :
        n_fold = M * os_factor - id[i] * os_factor
        for n in range(0,M*os_factor):
            if n < n_fold:
                chirp[i][n] = np.exp(2j*math.pi *(n*n/(2*M)/pow(os_factor,2)+(id[i]/M-0.5)*n/os_factor))
            else:
                chirp[i][n] = np.exp(2j*math.pi *(n*n/(2*M)/pow(os_factor,2)+(id[i]/M-1.5)*n/os_factor))
    
    # chirp = np.reshape(chirp,-1)

    return chirp

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, SF = 9, preamble_len = 6):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='LoRa Preamble',   # will show up in GRC
            in_sig=None,
            # out_sig=[(np.complex64,pow(2,SF)*preamble_len+round(pow(2,SF)*2.25))]
            out_sig=[(np.complex64,round(pow(2,SF)*(preamble_len+2.25)))]
        )
        self.SF = SF
        self.preamble_len = preamble_len

    def work(self, input_items, output_items):

        # for i in range (len(symbols)) :
        #     output_items[0][i] = modulate(self.SF, [symbols[i]], 1)
        
        # preamble = np.zeros((self.preamble_len*pow(2,self.SF)), dtype=np.complex64)
        preamble_up = np.reshape(modulate(self.SF, [0]*self.preamble_len, 1), -1)
        preamble_down = np.reshape(np.conjugate(modulate(self.SF, [0]*3, 1)), -1)[0:int(2.25*pow(2,self.SF))]
        #  [:round(0.75*pow(2,self.SF))]
        # print(preamble_up.shape)
        # print(preamble_down.shape)
        preamble = np.concatenate((preamble_up, preamble_down))
        output_items[0][0] = np.reshape(preamble,-1)


        return len(output_items[0])
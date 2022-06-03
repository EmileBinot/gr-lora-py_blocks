"""
Modulation Block:
"""

import numpy as np
from gnuradio import gr
import math

def modulate(SF, id, os_factor) :
    M  = pow(2,SF)
    n_fold = M * os_factor - id * os_factor
    chirp = np.zeros(M*os_factor, dtype=np.complex64)
    for n in range(0,M*os_factor):
        if n < n_fold:
            chirp[n] = np.exp(2j*math.pi *(n*n/(2*M)/pow(os_factor,2)+(id/M-0.5)*n/os_factor))
        else:
            chirp[n] = np.exp(2j*math.pi *(n*n/(2*M)/pow(os_factor,2)+(id/M-1.5)*n/os_factor))
    return chirp

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self, SF = 9):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='LoRa Modulation',   # will show up in GRC
            in_sig=[np.uint32],
            out_sig=[(np.complex64,512)]
        )
        self.SF = SF

    def work(self, input_items, output_items):
        
        symbols = input_items[0]

        for i in range (len(symbols)) :
            output_items[0][i] = modulate(self.SF, symbols[i], 1)
        
        # # debug
        # print("\n--- GENERAL WORK : MODULATION ---")
        # print("symbols :")
        # print(symbols)


        return len(output_items[0])

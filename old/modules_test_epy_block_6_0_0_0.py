"""
Modulation Block:
"""

import numpy as np
from gnuradio import gr
import math

def modulate(SF, symbol, sign) :
    M  = pow(2,SF)
    ka = np.arange(0,M)
    fact1 = np.exp(1j*sign*math.pi*pow(ka,2)/M)
    fact1 = np.reshape(fact1,(1,-1))
    symbK = np.multiply(fact1,np.exp(2j*math.pi*(symbol/M)*ka))

    return symbK

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

        for k in range (len(symbols)) :
            output_items[0][:] = modulate(self.SF, symbols[k], 1)

        return len(output_items[0])

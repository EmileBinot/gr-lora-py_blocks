"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import math

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, SF = 9):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Modulation',   # will show up in GRC
            in_sig=[np.uint32],
            out_sig=[(np.complex64,512)]
        )
        self.SF = SF

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        
        symbols = input_items[0]
        M  = pow(2,self.SF)
        ka = np.arange(0,M)

        fact1 = np.exp(1j*1*math.pi*pow(ka,2)/M)
        fact1 = np.reshape(fact1,(1,-1))
        
        r=0
        txSig=np.zeros((len(symbols), M), dtype=np.complex64)

        for k in range (len(symbols)) :
            symbK = np.multiply(fact1,np.exp(2j*math.pi*(symbols[0]/M)*ka))
            output_items[0][:] = symbK

        return len(output_items[0])

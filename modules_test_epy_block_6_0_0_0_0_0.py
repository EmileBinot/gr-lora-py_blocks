"""
Modulation Block:
Reference : "Towards an SDR implementation of LoRa..." 2020 A.Marquet, N.Montavont, G.Papadopoulos)

INPUT:
    - in_sig[0]: int32 input stream
OUTPUT:
    - out_sig[0]: IQ complex vectors output stream
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

class Modulation(gr.sync_block):

    def __init__(self, SF = 9):
        gr.sync_block.__init__(
            self,
            name='LoRa Modulation',
            in_sig=[np.uint32],
            out_sig=[(np.complex64,pow(2,SF))]
        )
        self.SF = SF

    def work(self, input_items, output_items):

        symbols = input_items[0]
        for i in range (len(symbols)) :
            output_items[0][i] = modulate(self.SF, symbols[i], 1)   # modulate every symbol

        # debug
        print("\n--- GENERAL WORK : MODULATION ---")
        print("symbols :")
        print(symbols)

        return len(output_items[0])
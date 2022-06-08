"""
Demodulation Block:
"""

import numpy as np
from gnuradio import gr
import math

# def modulate(SF, symbol, sign) :
    # M  = pow(2,SF)
    # ka = np.arange(0,M)
    # fact1 = np.exp(1j*sign*math.pi*pow(ka,2)/M)
    # fact1 = np.reshape(fact1,(1,-1))
    # symbK = np.multiply(fact1,np.exp(2j*math.pi*(symbol/M)*ka))
    # return symbK
    
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

    def __init__(self, SF = 9, B = 250000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='LoRa Demodulation',   # will show up in GRC
            in_sig=[(np.complex64,pow(2,SF))],
            # out_sig=[(np.complex64,512)]
            out_sig=[np.uint32]
        )
        self.SF = SF
        self.B = B

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        base_upchirp = modulate(self.SF, 0, 1)
        base_downchirp = np.conjugate(base_upchirp)
        M = pow(2,self.SF)
        symbols_hat =  np.zeros(len(input_items[0]), dtype=np.uint32)
        for i in range(len(input_items[0])):
            demod_signal = np.multiply(input_items[0][i], base_downchirp)
            demod_signal_fft = np.fft.fft(demod_signal)
            idx = np.argmax(np.abs(demod_signal_fft))
            freq_vect = np.arange(0,M-1)*(self.B/M) # !!!! WILL INTRODUCE PROBLEMS WHEN OS_FACTOR IS NOT 1 !!!!
            output_items[0][i] = round(freq_vect[idx]*M/self.B)
            symbols_hat[i] = round(freq_vect[idx]*M/self.B)
        
        # debug
        print("\n--- GENERAL WORK : DEMODULATION ---")
        print("symbols_hat :")
        print(symbols_hat)

        return len(output_items[0])

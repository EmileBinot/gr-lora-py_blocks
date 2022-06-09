"""
Demodulation Block:
Reference : "Towards an SDR implementation of LoRa..." 2020 A.Marquet, N.Montavont, G.Papadopoulos)

INPUT:
    - in_sig[0]: IQ complex vectors input sequence
OUTPUT:
    - out_sig[0]: 
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

class Demodulation(gr.sync_block):

    def __init__(self, SF = 9, B = 250000):
        gr.sync_block.__init__(
            self,
            name='LoRa Demodulation',
            in_sig=[(np.complex64,pow(2,SF))],
            out_sig=[np.uint32]
        )
        self.SF = SF
        self.B = B

    def work(self, input_items, output_items):

        M = pow(2,self.SF)
        base_upchirp = modulate(self.SF, 0, 1)
        base_downchirp = np.conjugate(base_upchirp)

        symbols_hat =  np.zeros(len(input_items[0]), dtype=np.uint32)
        for i in range(len(input_items[0])):
            demod_signal = np.multiply(input_items[0][i], base_downchirp)   # multiply every symbol with the downchirp
            demod_signal_fft = np.fft.fft(demod_signal)                     # perform FFT on demodulated signal    
            idx = np.argmax(np.abs(demod_signal_fft))                       # find the frequency index of the maximum value
            freq_vect = np.arange(0,M-1)*(self.B/M)                         # !!!! WILL INTRODUCE PROBLEMS WHEN OS_FACTOR IS NOT 1 !!!!
            symbols_hat[i] = round(freq_vect[idx]*M/self.B)                 # convert the frequency index to symbol index
            output_items[0][i] = symbols_hat[i]
            
        
        # debug
        print("\n--- GENERAL WORK : DEMODULATION ---")
        print("symbols_hat :")
        print(symbols_hat)

        return len(output_items[0])

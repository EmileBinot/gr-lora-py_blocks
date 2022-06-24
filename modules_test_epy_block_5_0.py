"""
Demodulation Block:
Reference : "Towards an SDR implementation of LoRa..." 2020 A.Marquet, N.Montavont, G.Papadopoulos)

INPUT:
    - in_sig[0]: IQ complex vectors input sequence
OUTPUT:
    - out_sig[0]: 
"""

from re import M
import numpy as np
from gnuradio import gr
import math
import matplotlib.pyplot as plt
# def modulate(SF, id, os_factor) :
#     M  = pow(2,SF)
#     n_fold = M * os_factor - id * os_factor
#     chirp = np.zeros(M*os_factor, dtype=np.complex64)
#     for n in range(0,M*os_factor):
#         if n < n_fold:
#             chirp[n] = np.exp(2j*math.pi *(n*n/(2*M)/pow(os_factor,2)+(id/M-0.5)*n/os_factor))
#         else:
#             chirp[n] = np.exp(2j*math.pi *(n*n/(2*M)/pow(os_factor,2)+(id/M-1.5)*n/os_factor))
#     return chirp

def modulate(SF, id, os_factor, sign) :
    M  = pow(2,SF)*os_factor
    ka = np.arange(0,M)
    fact1 = np.exp(1j*sign*math.pi*(pow(ka,2))/M)
    chirp = fact1*np.exp(2j*math.pi*(id/M)*ka)
    return chirp

class Demodulation(gr.basic_block):

    def __init__(self, SF = 9, B = 250000, os_factor = 1):
        gr.basic_block.__init__(
            self,
            name='LoRa Demodulation',
            in_sig=[(np.complex64)],
            out_sig=[np.uint32]
        )
        self.SF = SF
        self.B = B
        self.os_factor = os_factor
        self.M = 2**SF

    def forecast(self, noutput_items, ninputs) :
        #ninput_items_required[i] is the number of items that will be consumed on input port i
        ninput_items_required = [self.M*self.os_factor]*ninputs   # we need SF items to produce anything
        return ninput_items_required

    def general_work(self, input_items, output_items):

        # print(len(input_items[0]),len(output_items[0]))

        base_downchirp = modulate(self.SF, 0, self.os_factor, -1)
        freq_vect = np.arange(0,self.M*self.os_factor)                                    # !!!! WILL INTRODUCE PROBLEMS WHEN OS_FACTOR IS NOT 1 !!!!
        max_array = np.zeros(len(input_items[0]), dtype=np.float32)
        
        in0 = input_items[0][:self.M]

        demod_signal = np.multiply(in0, base_downchirp)   # multiply every symbol with the downchirp
        demod_signal_fft = np.fft.fft(demod_signal)                     # perform FFT on demodulated signal    
        idx = np.argmax(np.abs(demod_signal_fft))                       # find the frequency index of the maximum value
        output_items[0][0] = round(round(freq_vect[idx]))               # convert the frequency index to symbol index
        # debug
        # max_array[i] = np.max(np.abs(demod_signal_fft[idx]))
        
        self.consume(0, self.M)
        return 1
        


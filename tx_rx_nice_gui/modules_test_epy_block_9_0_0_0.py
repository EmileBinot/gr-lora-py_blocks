"""
LoRa Correlation Sync:
This block will add a tag 'preamble_begin' if correlation value > threshold

INPUT:
    - in_sig[0] : IQ complex items
OUTPUT:
    - out_sig[0]: IQ complex items, w/ tag added if corr_max > treshold
"""


import numpy as np
from gnuradio import gr
import pmt
import matplotlib.pyplot as plt
import math

def modulate_vect(SF, id, os_factor, sign) :
    M  = pow(2,SF)
    ka = np.arange(0,M)
    fact1 = np.exp(1j*sign*math.pi*(pow(ka,2))/M)
    chirp = np.zeros((len(id),M*os_factor), dtype=np.complex64)
    for i in range(len(id)) :
        chirp[i] = fact1*np.exp(2j*math.pi*(id[i]/M)*ka)
    return chirp

class blk(gr.sync_block):
    def __init__(self,preamble_len = 6, payload_nitems = 1, threshold = 10000, SF = 1):
        gr.sync_block.__init__(
            self,
            name='LoRa Correlation Sync Preamble',
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        
        self.preamble_len = preamble_len
        self.preamble_nitems = round(pow(2,SF)*(preamble_len+2.25))
        self.payload_nitems = payload_nitems
        self.threshold = threshold
        self.SF = SF

        self.state = 0 # 0 if searching for preamble, 1 if found
        self.items_written0_old = 0
        self.set_output_multiple(self.preamble_nitems + self.payload_nitems + 1000)

    def work(self, input_items, output_items):

        in0 = input_items[0]

        # Preamble creation
        preamble_up = np.reshape(modulate_vect(self.SF, [0]*self.preamble_len, 1, 1), -1)       # generate preamble_len upchirps
        preamble_down = np.reshape(np.conjugate(modulate_vect(self.SF, [0]*3, 1, 1)), -1)       # generate 3 downchirps
        preamble = np.concatenate((preamble_up, preamble_down[0:int(2.25*pow(2,self.SF))]))     # concatenate preamble_up and preamble_down[0:2.25*M]
    
        corr = np.abs(np.correlate(in0, preamble))**2
        corr_max = np.max(corr)
        corr_max_idx = np.argmax(corr)

        if corr_max > self.threshold :
            self.state = 1
            tag_index = self.nitems_written(0) + corr_max_idx
            self.add_item_tag(0,tag_index,  pmt.intern("preamble_begin"),  pmt.intern(str(self.preamble_nitems)))
            self.items_written0_old = self.nitems_written(0)

            # # debug

            # vect = np.arange(0,len(in0))
            # plt.plot(vect, np.abs(in0))
            # plt.axvline(corr_max_idx, 0, 1, color = "red", label = "Corr peak idx")
            # fig, axs = plt.subplots(3)
            # axs[0].specgram(in0, NFFT=64, Fs=32, noverlap=8)
            # axs[0].plot(np.arange(0, len(in0)), in0)
            # axs[1].plot(np.arange(0, len(corr)), corr)
            # axs[2].specgram(in0, NFFT=64, Fs=32, noverlap=8)
            # plt.show()   


        output_items[0][:] = in0[:len(output_items[0])]
        return len(output_items[0])

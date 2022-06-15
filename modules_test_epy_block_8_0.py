import numpy as np
from gnuradio import gr
import math
import pmt

def modulate_vect(SF, id, os_factor, sign) :
    M  = pow(2,SF)
    ka = np.arange(0,M)
    fact1 = np.exp(1j*sign*math.pi*(pow(ka,2))/M)
    chirp = np.zeros((len(id),M*os_factor), dtype=np.complex64)
    for i in range(len(id)) :
        chirp[i] = fact1*np.exp(2j*math.pi*(id[i]/M)*ka)
    return chirp

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    def __init__(self, SF=9, preamble_len = 6, frame_nitems = 18):  # only default arguments here
        """Preamble Correlator debug"""
        gr.sync_block.__init__(
            self,
            name='Preamble Correlator debug',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.SF = SF
        self.preamble_len = 6
        self.frame_len = 18
        self.preamble_nitems = int(pow(2,SF)*(preamble_len+2.25))
        self.frame_nitems = frame_nitems
        self.frame_counter = 0
        self.set_tag_propagation_policy(gr.TPP_DONT)
            
    def work(self, input_items, output_items):

        preamble_up = np.reshape(modulate_vect(self.SF, [0]*self.preamble_len, 1, 1), -1)      # generate preamble_len upchirps
        preamble_down = np.reshape(np.conjugate(modulate_vect(self.SF, [0]*3, 1, 1)), -1)      # generate 3 downchirps
        preamble = np.concatenate((preamble_up, preamble_down[0:int(2.25*pow(2,self.SF))])) # concatenate preamble_up and preamble_down[0:2.25*M]

        corr = np.correlate(input_items[0][0:self.preamble_nitems+1], preamble) # correlate input signal with preamble
        peak = np.max(np.abs(corr))             # find the correlation peak
        threshold = 2000                        # threshold for peak detection
        peak_index = np.argmax(corr)            # get index of the peak

        if peak > threshold :
            # tag_index = self.nitems_written(0) + self.preamble_nitems
            tag_index = self.nitems_written(0) 

            # add tag at the end of the preamble, write frame_length inside so Tagged Stream Cropper block can remove preamble
            # self.add_item_tag(0,tag_index,  pmt.intern("payload_begin"),  pmt.intern(str(self.frame_nitems)))
            self.add_item_tag(0,tag_index,  pmt.intern("preamble_begin"),  pmt.intern(str(self.preamble_nitems)))
            self.frame_counter += 1
            # print("[RX] Correlator : preamble detected, frame number :", self.frame_counter)
            # # # debug
            # print("\n--- Correlator ---")
            # print("peak > threshold")
            # print("peak index :",self.nitems_written(0))
            # print("tag index :",tag_index)

        output_items[0][:] = input_items[0]
        return len(output_items[0])
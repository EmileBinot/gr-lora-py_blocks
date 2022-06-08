"""
LoRa sync block
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

class Sync(gr.basic_block):
    def __init__(self, SF=9, B=250000, preamble_len= 6):
        gr.basic_block.__init__(self,
            name="LoRa Sync",
            in_sig=[np.complex64],
            out_sig=[np.complex64])
        self.SF = SF
        self.currentState = 'WAIT'
        self.B = B
        self.preamble_len = preamble_len
        self.receivedBlocksCounter = 1

    def forecast(self, noutput_items, ninputs) :
        #ninput_items_required[i] is the number of items that will be consumed on input port i
        # we need 2^SF items to produce anything
        ninput_items_required = [pow(2,self.SF)]*ninputs 
        return ninput_items_required

    def general_work(self, input_items, output_items):
        M = pow(2,self.SF)
        threshold = M/2
        syncword = 0

        if(len(input_items[0]) >= pow(2,self.SF)) :

            base_upchirp = modulate(self.SF, 0, 1)
            base_downchirp = np.conjugate(base_upchirp)
            demod_signal = np.multiply(input_items[0][:M], base_downchirp)
            demod_signal_fft = np.fft.fft(demod_signal)
            peak = int(np.max(np.abs(demod_signal_fft)))
            idx = np.argmax(np.abs(demod_signal_fft))
            freq_vect = np.arange(0,M-1)*(self.B/M) # !!!! WILL INTRODUCE PROBLEMS WHEN OS_FACTOR IS NOT 1 !!!!
            symbols_hat = round(freq_vect[idx]*M/self.B)
            
            if(self.currentState == 'WAIT') :
                if peak > threshold :
                    self.currentState = 'UPCHIRPS'
                else :
                    self.consume(0, M)

            if self.currentState == 'UPCHIRPS' :
                if peak < threshold :
                    self.currentState = 'WAIT'
                f_up = idx
                if idx == 0 :
                    self.receivedBlocksCounter += 1
                    if self.receivedBlocksCounter >= self.preamble_len-2 :
                        self.currentState = 'SYNCWORD'
                self.consume(0, M)

            if self.currentState == 'SYNCWORD' :
                if peak < threshold :
                    self.currentState = 'WAIT'
                if idx == syncword :
                    self.receivedBlocksCounter += 1
                if self.receivedBlocksCounter >= self.preamble_len :
                    self.currentState = 'DOWNCHIRPS'
                self.consume(0, M)

            if self.currentState == 'DOWNCHIRPS' :
                demod_signal = np.multiply(input_items[0][:M], base_upchirp)
                demod_signal_fft = np.fft.fft(demod_signal)
                peak = int(np.max(np.abs(demod_signal_fft)))
                idx = np.argmax(np.abs(demod_signal_fft))
                freq_vect = np.arange(0,M-1)*(self.B/M) # !!!! WILL INTRODUCE PROBLEMS WHEN OS_FACTOR IS NOT 1 !!!!
                f_down = idx
                self.receivedBlocksCounter += 1

                if self.receivedBlocksCounter > self.preamble_len+2 :
                    self.consume(0, M*0.25)
                    self.currentState = 'SYNC'
                else : 
                    self.consume(0, M)
            if self.currentState == 'SYNC' :
                CFOint = ((f_down + f_up)/2)*self.B
                STOint = (1-(f_down + f_up)/2)*M
                output_items[0][0:M] = input_items[0][0:M] # pass thru
                self.consume(0, M)

            print("\n--- Frame Sync ---")
            print(self.currentState)
            print("receivedBlockCounter: ", self.receivedBlocksCounter)
            print("idx: ", idx)
            print("peak: ", peak)


            
            return 0
        else :
            return 0




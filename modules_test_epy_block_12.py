"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import math
import matplotlib.pyplot as plt
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
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='Channel estimator',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.SF = 9
        self.preamble_len = 6
        preamble_up = np.reshape(modulate_vect(self.SF, [0]*self.preamble_len, 1, 1), -1)           # generate preamble_len upchirps
        preamble_down = np.reshape(np.conjugate(modulate_vect(self.SF, [0]*3, 1, 1)), -1)           # generate 3 downchirps
        self.preamble = np.concatenate((preamble_up, preamble_down[0:int(2.25*pow(2,self.SF))]))    # concatenate preamble_up and preamble_down[0:2.25*M]
        
        self.set_output_multiple(len(self.preamble))
        self.message_port_register_out(pmt.intern("h_est"))


    def work(self, input_items, output_items):

        in0 = input_items[0][:len(self.preamble)]

        h_est = in0.T*self.preamble# https://www.youtube.com/watch?v=XCe0xanaPFo
        h_est_LS = in0 / self.preamble

        h_est_mean = np.mean(h_est)
        h_est_LS_mean = np.mean(h_est_LS)

        # print("[RX] Channel : h^est =",h_est_mean)
        

        # Computing MSE :
        y = in0
        y_est_LS = self.preamble * h_est_LS_mean
        mse_LS = np.abs((np.square(y - y_est_LS)).mean(axis=None))

        # y_est = self.preamble * h_est_mean
        # mse = np.abs((np.square(y - y_est)).mean(axis=None))

        print("[RX] Channel : h^estLS =",h_est_LS_mean)
        # print("[RX] Channel : MSE_LS = ",mse_LS)

        # print("[RX] Channel : MSE = ",mse)

        P_pair = pmt.cons(pmt.string_to_symbol("h_est"), pmt.from_complex(complex(round(h_est_LS_mean.real,1),round(h_est_LS_mean.imag,1))))
        # self.message_port_pub(pmt.intern("h_est"), P_pair)
        self.message_port_pub(pmt.intern("h_est"), P_pair)


        # fig, axs = plt.subplots(4)
        # axs[0].specgram(self.preamble, NFFT=64, Fs=32, noverlap=8)
        # axs[0].set_title('X')
        # axs[1].specgram(y, NFFT=64, Fs=32, noverlap=8)
        # axs[1].set_title('Y = H*X+N')
        # axs[2].specgram(y_est_LS, NFFT=64, Fs=32, noverlap=8)
        # axs[2].set_title('Y_est = H_est*X+N')
        # # axs[4].plot(np.arange(0,len(h)),np.real(h),np.arange(0,len(h)), np.imag(h))
        # # axs[4].set_ylim([-1,1])
        # plt.show()

        
        output_items[0][:len(in0)] = in0
        return len(in0)


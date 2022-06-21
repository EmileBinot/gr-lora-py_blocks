"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self,preamble_len = 6, payload_nitems = 6144, SF = 9):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.complex64],
            out_sig=[np.complex64]
        )
        self.preamble_len = preamble_len
        self.preamble_nitems = int((preamble_len+2.25)*(2**SF))
        self.payload_nitems = payload_nitems
        self.frame_nitems = self.preamble_nitems + self.payload_nitems
        self.SF = SF

        self.set_history(self.preamble_nitems)
        self.declare_sample_delay(self.preamble_nitems)
        self.set_output_multiple(self.preamble_nitems)

        self.state = 0 # 0 if searching for preamble, 1 if found
        self.last_tag = 0

    def work(self, input_items, output_items):

        in0 = input_items[0][:len(output_items[0])]

        threshold = 0.15
        threshold_pwr = 0.5
        in0_pwr = (np.linalg.norm(in0)**2)/len(in0)
        # print(in0_pwr)
        if self.state == 0 : 
            print('searching for preamble')
            for i in range(len(in0)) :
                if np.abs(in0[i]) > threshold and self.state == 0 :
                    print("Threshold exceeded")
                    self.state = 1
                    tag_index = self.nitems_written(0) + i + self.preamble_nitems
                    self.last_tag = self.nitems_written(0) + i + self.preamble_nitems
                    self.add_item_tag(0,tag_index,  pmt.intern("payload_begin"),  pmt.intern(str(self.frame_nitems)))

                    # fig, axs = plt.subplots(3)
                    # fig.suptitle('Vertically stacked subplots')
                    # axs[0].specgram(in0, NFFT=64, Fs=32, noverlap=8)
                    # plt.show()

        if self.state == 1 :
            if int(self.nitems_written(0)) - self.last_tag > self.payload_nitems:
                print("Reset")
                self.state = 0
            pass

        output_items[0][:] = input_items[0]
        return len(output_items[0])

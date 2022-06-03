#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.9.5.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import modules_test_epy_block_1_0_0 as epy_block_1_0_0  # embedded python block
import modules_test_epy_block_1_1 as epy_block_1_1  # embedded python block




class modules_test(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.epy_block_1_1 = epy_block_1_1.Hamming_enc(CR=2)
        self.epy_block_1_0_0 = epy_block_1_0_0.Whitening()
        self.blocks_vector_source_x_0_0_0_0 = blocks.vector_source_b((0x01, 0x02), False, 1, [])
        self.blocks_file_sink_0_1 = blocks.file_sink(gr.sizeof_char*1, 'dumpOUT', False)
        self.blocks_file_sink_0_1.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, 'dumpIN', False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_0_0_0_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_vector_source_x_0_0_0_0, 0), (self.epy_block_1_0_0, 0))
        self.connect((self.epy_block_1_0_0, 0), (self.epy_block_1_1, 0))
        self.connect((self.epy_block_1_1, 0), (self.blocks_file_sink_0_1, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=modules_test, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()

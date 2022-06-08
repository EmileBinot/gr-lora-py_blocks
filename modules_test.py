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
import modules_test_epy_block_0 as epy_block_0  # embedded python block
import modules_test_epy_block_0_1_0_0 as epy_block_0_1_0_0  # embedded python block
import modules_test_epy_block_1 as epy_block_1  # embedded python block
import modules_test_epy_block_1_0_0 as epy_block_1_0_0  # embedded python block
import modules_test_epy_block_1_1 as epy_block_1_1  # embedded python block
import modules_test_epy_block_2 as epy_block_2  # embedded python block
import modules_test_epy_block_3 as epy_block_3  # embedded python block
import modules_test_epy_block_5 as epy_block_5  # embedded python block
import modules_test_epy_block_6 as epy_block_6  # embedded python block
import modules_test_epy_block_6_0 as epy_block_6_0  # embedded python block
import modules_test_epy_block_6_0_0_0_0_0 as epy_block_6_0_0_0_0_0  # embedded python block




class modules_test(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.preamble_len = preamble_len = 6
        self.SF = SF = 9
        self.CR = CR = 2

        ##################################################
        # Blocks
        ##################################################
        self.epy_block_6_0_0_0_0_0 = epy_block_6_0_0_0_0_0.blk(SF=SF)
        self.epy_block_6_0 = epy_block_6_0.my_basic_adder_block(tag_name="preambleStart")
        self.epy_block_6 = epy_block_6.Frame_sync(SF=9, preamble_len=preamble_len, frameLength=18)
        self.epy_block_5 = epy_block_5.blk(SF=SF, B=250000)
        self.epy_block_3 = epy_block_3.blk(SF=9, preamble_len=preamble_len)
        self.epy_block_2 = epy_block_2.LoRa_Dewhitening()
        self.epy_block_1_1 = epy_block_1_1.Hamming_enc(CR=CR)
        self.epy_block_1_0_0 = epy_block_1_0_0.Whitening()
        self.epy_block_1 = epy_block_1.Hamming_Rx(CR=CR)
        self.epy_block_0_1_0_0 = epy_block_0_1_0_0.Interleaver(SF=SF, CR=CR)
        self.epy_block_0 = epy_block_0.Deinterleaver(SF=SF, CR=CR)
        self.blocks_vector_to_stream_0_0_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, pow(2,SF))
        self.blocks_vector_to_stream_0_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, round(pow(2,SF)*(preamble_len+2.25)))
        self.blocks_vector_source_x_0_0_0_0 = blocks.vector_source_b((0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x0e, 0x0d, 0x0c), False, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_c((0, 0, 0, 0, 0, 0, 0, 0), True, 1, [])
        self.blocks_tagged_stream_align_1 = blocks.tagged_stream_align(gr.sizeof_gr_complex*1, "preambleStart")
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, pow(2,SF))
        self.blocks_stream_mux_1 = blocks.stream_mux(gr.sizeof_gr_complex*1, (8, round(pow(2,SF)*(preamble_len+2.25)), 18*512))
        self.blocks_file_sink_2_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'payloadOUT', False)
        self.blocks_file_sink_2_0.set_unbuffered(False)
        self.blocks_file_sink_0_3 = blocks.file_sink(gr.sizeof_char*1, 'dumpIN', False)
        self.blocks_file_sink_0_3.set_unbuffered(False)
        self.blocks_file_sink_0_1 = blocks.file_sink(gr.sizeof_char*1, 'dumpOUT', False)
        self.blocks_file_sink_0_1.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_stream_mux_1, 0), (self.epy_block_6, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.epy_block_5, 0))
        self.connect((self.blocks_tagged_stream_align_1, 0), (self.epy_block_6_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_mux_1, 0))
        self.connect((self.blocks_vector_source_x_0_0_0_0, 0), (self.blocks_file_sink_0_3, 0))
        self.connect((self.blocks_vector_source_x_0_0_0_0, 0), (self.epy_block_1_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0_0, 0), (self.blocks_stream_mux_1, 1))
        self.connect((self.blocks_vector_to_stream_0_0_1, 0), (self.blocks_stream_mux_1, 2))
        self.connect((self.epy_block_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_0_1_0_0, 0), (self.epy_block_6_0_0_0_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.epy_block_2, 0))
        self.connect((self.epy_block_1_0_0, 0), (self.epy_block_1_1, 0))
        self.connect((self.epy_block_1_1, 0), (self.epy_block_0_1_0_0, 0))
        self.connect((self.epy_block_2, 0), (self.blocks_file_sink_0_1, 0))
        self.connect((self.epy_block_3, 0), (self.blocks_vector_to_stream_0_0_0, 0))
        self.connect((self.epy_block_3, 0), (self.epy_block_6, 1))
        self.connect((self.epy_block_5, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_6, 0), (self.blocks_tagged_stream_align_1, 0))
        self.connect((self.epy_block_6_0, 0), (self.blocks_file_sink_2_0, 0))
        self.connect((self.epy_block_6_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.epy_block_6_0_0_0_0_0, 0), (self.blocks_vector_to_stream_0_0_1, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_preamble_len(self):
        return self.preamble_len

    def set_preamble_len(self, preamble_len):
        self.preamble_len = preamble_len
        self.epy_block_3.preamble_len = self.preamble_len

    def get_SF(self):
        return self.SF

    def set_SF(self, SF):
        self.SF = SF
        self.epy_block_0.SF = self.SF
        self.epy_block_0_1_0_0.SF = self.SF
        self.epy_block_5.SF = self.SF
        self.epy_block_6_0_0_0_0_0.SF = self.SF

    def get_CR(self):
        return self.CR

    def set_CR(self, CR):
        self.CR = CR
        self.epy_block_0.CR = self.CR
        self.epy_block_0_1_0_0.CR = self.CR
        self.epy_block_1.CR = self.CR
        self.epy_block_1_1.CR = self.CR




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

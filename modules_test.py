#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.2.0

from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import pdu
import modules_test_epy_block_0 as epy_block_0  # embedded python block
import modules_test_epy_block_0_1_0_0 as epy_block_0_1_0_0  # embedded python block
import modules_test_epy_block_1 as epy_block_1  # embedded python block
import modules_test_epy_block_1_0_0 as epy_block_1_0_0  # embedded python block
import modules_test_epy_block_1_1 as epy_block_1_1  # embedded python block
import modules_test_epy_block_2 as epy_block_2  # embedded python block
import modules_test_epy_block_5 as epy_block_5  # embedded python block
import modules_test_epy_block_6_0_0_0_0_0 as epy_block_6_0_0_0_0_0  # embedded python block




class modules_test(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.bandwidth = bandwidth = int(125e3)
        self.samp_rate = samp_rate = bandwidth
        self.preamble_len = preamble_len = 6
        self.frame_len = frame_len = 18
        self.center_freq = center_freq = int(868e6)
        self.SF = SF = 9
        self.CR = CR = 2

        ##################################################
        # Blocks
        ##################################################
        self.pdu_random_pdu_0 = pdu.random_pdu(SF*10, SF*10, 0x0F, SF)
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, 64)
        self.epy_block_6_0_0_0_0_0 = epy_block_6_0_0_0_0_0.Modulation(SF=SF)
        self.epy_block_5 = epy_block_5.Demodulation(SF=SF, B=250000)
        self.epy_block_2 = epy_block_2.LoraDewhitening()
        self.epy_block_1_1 = epy_block_1_1.HammingTx(CR=CR)
        self.epy_block_1_0_0 = epy_block_1_0_0.Whitening()
        self.epy_block_1 = epy_block_1.HammingRx(CR=CR)
        self.epy_block_0_1_0_0 = epy_block_0_1_0_0.Interleaver(SF=SF, CR=CR)
        self.epy_block_0 = epy_block_0.Deinterleaver(SF=SF, CR=CR)
        self.blocks_vector_to_stream_0_0_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, pow(2,SF))
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, pow(2,SF))
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("#t"), 1000)
        self.blocks_file_sink_0_3 = blocks.file_sink(gr.sizeof_char*1, 'dumpIN', False)
        self.blocks_file_sink_0_3.set_unbuffered(False)
        self.blocks_file_sink_0_1 = blocks.file_sink(gr.sizeof_char*1, 'dumpOUT', False)
        self.blocks_file_sink_0_1.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.pdu_random_pdu_0, 'generate'))
        self.msg_connect((self.pdu_random_pdu_0, 'pdus'), (self.pdu_pdu_to_stream_x_0, 'pdus'))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.epy_block_5, 0))
        self.connect((self.blocks_vector_to_stream_0_0_1, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.epy_block_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_0_1_0_0, 0), (self.epy_block_6_0_0_0_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.epy_block_2, 0))
        self.connect((self.epy_block_1_0_0, 0), (self.epy_block_1_1, 0))
        self.connect((self.epy_block_1_1, 0), (self.epy_block_0_1_0_0, 0))
        self.connect((self.epy_block_2, 0), (self.blocks_file_sink_0_1, 0))
        self.connect((self.epy_block_2, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.epy_block_5, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_6_0_0_0_0_0, 0), (self.blocks_vector_to_stream_0_0_1, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.blocks_file_sink_0_3, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.epy_block_1_0_0, 0))


    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_samp_rate(self.bandwidth)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_preamble_len(self):
        return self.preamble_len

    def set_preamble_len(self, preamble_len):
        self.preamble_len = preamble_len

    def get_frame_len(self):
        return self.frame_len

    def set_frame_len(self, frame_len):
        self.frame_len = frame_len

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq

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

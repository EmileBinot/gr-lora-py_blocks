#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.2.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import pdu
from gnuradio import uhd
import time
import modules_test_epy_block_0_1_0_0 as epy_block_0_1_0_0  # embedded python block
import modules_test_epy_block_1_0_0 as epy_block_1_0_0  # embedded python block
import modules_test_epy_block_1_1 as epy_block_1_1  # embedded python block
import modules_test_epy_block_3 as epy_block_3  # embedded python block
import modules_test_epy_block_6 as epy_block_6  # embedded python block
import modules_test_epy_block_6_0_0_0_0_0 as epy_block_6_0_0_0_0_0  # embedded python block
import modules_test_epy_block_7 as epy_block_7  # embedded python block



from gnuradio import qtgui

class modules_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "modules_test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.payload_len = payload_len = 18
        self.SF = SF = 9
        self.CR = CR = 2
        self.preamble_len = preamble_len = 6
        self.payload_nsymb = payload_nsymb = int((payload_len/SF)*(CR+4))
        self.bandwidth = bandwidth = int(125e3)
        self.samp_rate = samp_rate = bandwidth
        self.preamble_nitems = preamble_nitems = round(pow(2,SF)*(preamble_len+2.25))
        self.payload_nitems = payload_nitems = int(payload_nsymb*pow(2,SF))
        self.center_freq = center_freq = int(868e6)

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("addr=192.168.10.3", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_clock_source('gpsdo', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(bandwidth, 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            preamble_nitems+payload_nitems, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.pdu_random_pdu_0 = pdu.random_pdu(payload_len, payload_len, 0x0F, SF)
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, 64)
        self.epy_block_7 = epy_block_7.blk(preamble_nitems=preamble_nitems, payload_nitems=payload_nitems)
        self.epy_block_6_0_0_0_0_0 = epy_block_6_0_0_0_0_0.Modulation(SF=SF)
        self.epy_block_6 = epy_block_6.blk(preamble_nitems=4224, payload_nitems=6144)
        self.epy_block_3 = epy_block_3.PreambleGenerator(SF=SF, preamble_len=preamble_len)
        self.epy_block_1_1 = epy_block_1_1.HammingTx(CR=CR)
        self.epy_block_1_0_0 = epy_block_1_0_0.Whitening(reset_key="tx_sob")
        self.epy_block_0_1_0_0 = epy_block_0_1_0_0.Interleaver(SF=SF, CR=CR)
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, pow(2,SF))
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, payload_nitems+preamble_nitems)
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, payload_nitems)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("#t"), 100)
        self.blocks_file_sink_0_3_0_0_0 = blocks.file_sink(gr.sizeof_char*1, 'dumpIN', False)
        self.blocks_file_sink_0_3_0_0_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.pdu_random_pdu_0, 'generate'))
        self.msg_connect((self.pdu_random_pdu_0, 'pdus'), (self.pdu_pdu_to_stream_x_0, 'pdus'))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.epy_block_6, 1))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.epy_block_7, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.epy_block_0_1_0_0, 0), (self.epy_block_6_0_0_0_0_0, 0))
        self.connect((self.epy_block_1_0_0, 0), (self.epy_block_1_1, 0))
        self.connect((self.epy_block_1_1, 0), (self.epy_block_0_1_0_0, 0))
        self.connect((self.epy_block_3, 0), (self.epy_block_6, 0))
        self.connect((self.epy_block_6, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.epy_block_6_0_0_0_0_0, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.epy_block_7, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.epy_block_7, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.blocks_file_sink_0_3_0_0_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.epy_block_1_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "modules_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_payload_len(self):
        return self.payload_len

    def set_payload_len(self, payload_len):
        self.payload_len = payload_len
        self.set_payload_nsymb(int((self.payload_len/self.SF)*(self.CR+4)))

    def get_SF(self):
        return self.SF

    def set_SF(self, SF):
        self.SF = SF
        self.set_payload_nitems(int(self.payload_nsymb*pow(2,self.SF)))
        self.set_payload_nsymb(int((self.payload_len/self.SF)*(self.CR+4)))
        self.set_preamble_nitems(round(pow(2,self.SF)*(self.preamble_len+2.25)))
        self.epy_block_0_1_0_0.SF = self.SF
        self.epy_block_3.SF = self.SF
        self.epy_block_6_0_0_0_0_0.SF = self.SF

    def get_CR(self):
        return self.CR

    def set_CR(self, CR):
        self.CR = CR
        self.set_payload_nsymb(int((self.payload_len/self.SF)*(self.CR+4)))
        self.epy_block_0_1_0_0.CR = self.CR
        self.epy_block_1_1.CR = self.CR

    def get_preamble_len(self):
        return self.preamble_len

    def set_preamble_len(self, preamble_len):
        self.preamble_len = preamble_len
        self.set_preamble_nitems(round(pow(2,self.SF)*(self.preamble_len+2.25)))
        self.epy_block_3.preamble_len = self.preamble_len

    def get_payload_nsymb(self):
        return self.payload_nsymb

    def set_payload_nsymb(self, payload_nsymb):
        self.payload_nsymb = payload_nsymb
        self.set_payload_nitems(int(self.payload_nsymb*pow(2,self.SF)))

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_samp_rate(self.bandwidth)
        self.uhd_usrp_sink_0.set_bandwidth(self.bandwidth, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_preamble_nitems(self):
        return self.preamble_nitems

    def set_preamble_nitems(self, preamble_nitems):
        self.preamble_nitems = preamble_nitems
        self.epy_block_7.preamble_nitems = self.preamble_nitems

    def get_payload_nitems(self):
        return self.payload_nitems

    def set_payload_nitems(self, payload_nitems):
        self.payload_nitems = payload_nitems
        self.epy_block_7.payload_nitems = self.payload_nitems

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)




def main(top_block_cls=modules_test, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()

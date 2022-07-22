#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: LoRa Tx/Rx
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
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import channels
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import pdu
import pmt
from gnuradio import uhd
import time
import modules_test_epy_block_0 as epy_block_0  # embedded python block
import modules_test_epy_block_0_1_0_0 as epy_block_0_1_0_0  # embedded python block
import modules_test_epy_block_1 as epy_block_1  # embedded python block
import modules_test_epy_block_12 as epy_block_12  # embedded python block
import modules_test_epy_block_1_0_0 as epy_block_1_0_0  # embedded python block
import modules_test_epy_block_1_1 as epy_block_1_1  # embedded python block
import modules_test_epy_block_2 as epy_block_2  # embedded python block
import modules_test_epy_block_3 as epy_block_3  # embedded python block
import modules_test_epy_block_5 as epy_block_5  # embedded python block
import modules_test_epy_block_6 as epy_block_6  # embedded python block
import modules_test_epy_block_6_0 as epy_block_6_0  # embedded python block
import modules_test_epy_block_6_0_0 as epy_block_6_0_0  # embedded python block
import modules_test_epy_block_6_0_0_0_0_0 as epy_block_6_0_0_0_0_0  # embedded python block
import modules_test_epy_block_6_0_1 as epy_block_6_0_1  # embedded python block
import modules_test_epy_block_7_0 as epy_block_7_0  # embedded python block
import modules_test_epy_block_8 as epy_block_8  # embedded python block
import modules_test_epy_block_8_0 as epy_block_8_0  # embedded python block
import modules_test_epy_block_9 as epy_block_9  # embedded python block
import modules_test_epy_block_9_0 as epy_block_9_0  # embedded python block
import modules_test_epy_block_9_0_0_0 as epy_block_9_0_0_0  # embedded python block



from gnuradio import qtgui

class modules_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "LoRa Tx/Rx", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("LoRa Tx/Rx")
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
        self.CR = CR = 4
        self.success_rate = success_rate = 0
        self.preamble_len = preamble_len = 6
        self.payload_nsymb = payload_nsymb = int((payload_len/SF)*(CR+4))
        self.h_est = h_est = 0
        self.frame_nbr_rx = frame_nbr_rx = 0
        self.frame_nbr = frame_nbr = 0
        self.bandwidth = bandwidth = int(125e3)
        self.samp_rate = samp_rate = bandwidth
        self.prod_01_1 = prod_01_1 = h_est
        self.prod_01_0 = prod_01_0 = frame_nbr_rx
        self.prod_01 = prod_01 = frame_nbr
        self.prod = prod = success_rate
        self.preamble_nitems = preamble_nitems = round(pow(2,SF)*(preamble_len+2.25))
        self.payload_nitems = payload_nitems = int(payload_nsymb*pow(2,SF))
        self.os_factor = os_factor = 1
        self.h_simul = h_simul = 1
        self.const_multiply = const_multiply = 1
        self.chooser = chooser = 0
        self.center_freq = center_freq = int(868e6)

        ##################################################
        # Blocks
        ##################################################
        self._h_simul_tool_bar = Qt.QToolBar(self)
        self._h_simul_tool_bar.addWidget(Qt.QLabel("One tap simulation channel h" + ": "))
        self._h_simul_line_edit = Qt.QLineEdit(str(self.h_simul))
        self._h_simul_tool_bar.addWidget(self._h_simul_line_edit)
        self._h_simul_line_edit.returnPressed.connect(
            lambda: self.set_h_simul(eval(str(self._h_simul_line_edit.text()))))
        self.top_layout.addWidget(self._h_simul_tool_bar)
        # Create the options list
        self._chooser_options = [0, 1]
        # Create the labels list
        self._chooser_labels = ['Simulation', 'USRP']
        # Create the combo box
        # Create the radio buttons
        self._chooser_group_box = Qt.QGroupBox("Choose Channel" + ": ")
        self._chooser_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._chooser_button_group = variable_chooser_button_group()
        self._chooser_group_box.setLayout(self._chooser_box)
        for i, _label in enumerate(self._chooser_labels):
            radio_button = Qt.QRadioButton(_label)
            self._chooser_box.addWidget(radio_button)
            self._chooser_button_group.addButton(radio_button, i)
        self._chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._chooser_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._chooser_options.index(i)))
        self._chooser_callback(self.chooser)
        self._chooser_button_group.buttonClicked[int].connect(
            lambda i: self.set_chooser(self._chooser_options[i]))
        self.top_grid_layout.addWidget(self._chooser_group_box, 0, 3, 1, 3)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.variable_qtgui_msg_push_button_0 = _variable_qtgui_msg_push_button_0_toggle_button = qtgui.MsgPushButton('[Tx] : Send frame', 'pressed',1,"default","default")
        self.variable_qtgui_msg_push_button_0 = _variable_qtgui_msg_push_button_0_toggle_button

        self.top_grid_layout.addWidget(_variable_qtgui_msg_push_button_0_toggle_button, 0, 0, 1, 3)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.uhd_usrp_source_1 = uhd.usrp_source(
            ",".join(("addr=192.168.10.2", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_1.set_clock_source('mimo', 0)
        self.uhd_usrp_source_1.set_time_source('mimo', 0)
        self.uhd_usrp_source_1.set_samp_rate(samp_rate)
        # No synchronization enforced.

        self.uhd_usrp_source_1.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_1.set_antenna("TX/RX", 0)
        self.uhd_usrp_source_1.set_gain(0, 0)
        self.uhd_usrp_source_1.set_auto_dc_offset(True, 0)
        self.uhd_usrp_source_1.set_auto_iq_balance(True, 0)
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
        self.uhd_usrp_sink_0.set_normalized_gain(1, 0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            preamble_nitems+payload_nitems, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1.5, 1.5)

        self.qtgui_time_sink_x_0.set_y_label('Tx Frame', "")

        self.qtgui_time_sink_x_0.enable_tags(False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['In-Phase', 'Quadrature', 'Signal 3', 'Signal 4', 'Signal 5',
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
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 1, 0, 2, 6)
        for r in range(1, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._prod_01_1_tool_bar = Qt.QToolBar(self)

        if None:
            self._prod_01_1_formatter = None
        else:
            self._prod_01_1_formatter = lambda x: repr(x)

        self._prod_01_1_tool_bar.addWidget(Qt.QLabel("[Rx] : Channel estimation :"))
        self._prod_01_1_label = Qt.QLabel(str(self._prod_01_1_formatter(self.prod_01_1)))
        self._prod_01_1_tool_bar.addWidget(self._prod_01_1_label)
        self.top_grid_layout.addWidget(self._prod_01_1_tool_bar, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._prod_01_0_tool_bar = Qt.QToolBar(self)

        if None:
            self._prod_01_0_formatter = None
        else:
            self._prod_01_0_formatter = lambda x: str(x)

        self._prod_01_0_tool_bar.addWidget(Qt.QLabel("[Rx] : Number of frames received :"))
        self._prod_01_0_label = Qt.QLabel(str(self._prod_01_0_formatter(self.prod_01_0)))
        self._prod_01_0_tool_bar.addWidget(self._prod_01_0_label)
        self.top_grid_layout.addWidget(self._prod_01_0_tool_bar, 3, 2, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._prod_01_tool_bar = Qt.QToolBar(self)

        if None:
            self._prod_01_formatter = None
        else:
            self._prod_01_formatter = lambda x: str(x)

        self._prod_01_tool_bar.addWidget(Qt.QLabel("[Tx] : Number of frames sent :"))
        self._prod_01_label = Qt.QLabel(str(self._prod_01_formatter(self.prod_01)))
        self._prod_01_tool_bar.addWidget(self._prod_01_label)
        self.top_grid_layout.addWidget(self._prod_01_tool_bar, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._prod_tool_bar = Qt.QToolBar(self)

        if None:
            self._prod_formatter = None
        else:
            self._prod_formatter = lambda x: str(x)

        self._prod_tool_bar.addWidget(Qt.QLabel("[Rx] : Symbols without error on current frame (/18) :"))
        self._prod_label = Qt.QLabel(str(self._prod_formatter(self.prod)))
        self._prod_tool_bar.addWidget(self._prod_label)
        self.top_grid_layout.addWidget(self._prod_tool_bar, 4, 2, 1, 2)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pdu_random_pdu_0 = pdu.random_pdu(payload_len, payload_len, 0x0F, SF)
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, 64)
        self.epy_block_9_0_0_0 = epy_block_9_0_0_0.blk(preamble_len=preamble_len, payload_nitems=payload_nitems, threshold=int(5e4), SF=9)
        self.epy_block_9_0 = epy_block_9_0.blk(preamble_len=preamble_len, payload_nitems=payload_nitems, threshold=int(50e3), SF=9)
        self.epy_block_9 = epy_block_9.blk(preamble_nitems=preamble_nitems*os_factor, payload_nitems=payload_nitems*os_factor, threshold=0.1)
        self.epy_block_8_0 = epy_block_8_0.blk(SF=9)
        self.epy_block_8 = epy_block_8.blk(SF=9)
        self.epy_block_7_0 = epy_block_7_0.blk(preamble_nitems=preamble_nitems, payload_nitems=payload_nitems)
        self.epy_block_6_0_1 = epy_block_6_0_1.my_basic_adder_block(tag_name="preamble_begin")
        self.epy_block_6_0_0_0_0_0 = epy_block_6_0_0_0_0_0.Modulation(SF=SF)
        self.epy_block_6_0_0 = epy_block_6_0_0.my_basic_adder_block(tag_name="threshold_exceeded")
        self.epy_block_6_0 = epy_block_6_0.my_basic_adder_block(tag_name="payload_begin")
        self.epy_block_6 = epy_block_6.blk(preamble_nitems=4224, payload_nitems=8192)
        self.epy_block_5 = epy_block_5.Demodulation(SF=SF, B=250000, os_factor=os_factor)
        self.epy_block_3 = epy_block_3.PreambleGenerator(SF=SF, preamble_len=preamble_len)
        self.epy_block_2 = epy_block_2.LoraDewhitening(reset_key="payload_begin")
        self.epy_block_1_1 = epy_block_1_1.HammingTx(CR=CR)
        self.epy_block_1_0_0 = epy_block_1_0_0.Whitening(reset_key="tx_sob")
        self.epy_block_12 = epy_block_12.blk()
        self.epy_block_1 = epy_block_1.HammingRx(CR=CR, payload_len=payload_len)
        self.epy_block_0_1_0_0 = epy_block_0_1_0_0.Interleaver(SF=SF, CR=CR)
        self.epy_block_0 = epy_block_0.Deinterleaver(SF=SF, CR=CR)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=0,
            frequency_offset=0,
            epsilon=1.0,
            taps=[h_simul],
            noise_seed=0,
            block_tags=True)
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, pow(2,SF))
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, payload_nitems+preamble_nitems)
        self.blocks_vector_source_x_1_0 = blocks.vector_source_c([0]*100000, True, 1, [])
        self.blocks_tagged_stream_align_1_1 = blocks.tagged_stream_align(gr.sizeof_gr_complex*1, "preamble_begin")
        self.blocks_tagged_stream_align_1_0 = blocks.tagged_stream_align(gr.sizeof_gr_complex*1, "threshold_exceeded")
        self.blocks_tagged_stream_align_1 = blocks.tagged_stream_align(gr.sizeof_gr_complex*1, "payload_begin")
        self.blocks_tagged_stream_align_0 = blocks.tagged_stream_align(gr.sizeof_gr_complex*1, 'packet_len')
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, payload_nitems)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, pow(2,SF)*os_factor)
        self.blocks_stream_mux_0_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, (100000, preamble_nitems + payload_nitems))
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_gr_complex*1,0,chooser)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,chooser,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_null_sink_1_0 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_msgpair_to_var_0_0_0_0 = blocks.msg_pair_to_var(self.set_h_est)
        self.blocks_msgpair_to_var_0_0_0 = blocks.msg_pair_to_var(self.set_frame_nbr_rx)
        self.blocks_msgpair_to_var_0_0 = blocks.msg_pair_to_var(self.set_frame_nbr)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_success_rate)
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.blocks_file_sink_0_1_0 = blocks.file_sink(gr.sizeof_gr_complex*1, 'lora_rx_payload', False)
        self.blocks_file_sink_0_1_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_1, 'msg_out'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.epy_block_12, 'h_est'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.epy_block_12, 'h_est'), (self.blocks_msgpair_to_var_0_0_0_0, 'inpair'))
        self.msg_connect((self.epy_block_6, 'msg_out'), (self.blocks_msgpair_to_var_0_0, 'inpair'))
        self.msg_connect((self.epy_block_9_0, 'msg_out'), (self.blocks_msgpair_to_var_0_0_0, 'inpair'))
        self.msg_connect((self.pdu_random_pdu_0, 'pdus'), (self.pdu_pdu_to_stream_x_0, 'pdus'))
        self.msg_connect((self.variable_qtgui_msg_push_button_0, 'pressed'), (self.pdu_random_pdu_0, 'generate'))
        self.connect((self.blocks_selector_0, 0), (self.epy_block_9, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_stream_mux_0_0, 1))
        self.connect((self.blocks_selector_0_0, 1), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_stream_mux_0_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.epy_block_5, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.epy_block_6, 1))
        self.connect((self.blocks_tagged_stream_align_0, 0), (self.epy_block_7_0, 0))
        self.connect((self.blocks_tagged_stream_align_1, 0), (self.epy_block_6_0, 0))
        self.connect((self.blocks_tagged_stream_align_1_0, 0), (self.epy_block_6_0_0, 0))
        self.connect((self.blocks_tagged_stream_align_1_1, 0), (self.epy_block_6_0_1, 0))
        self.connect((self.blocks_vector_source_x_1_0, 0), (self.blocks_stream_mux_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_tagged_stream_align_0, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.epy_block_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_0_1_0_0, 0), (self.epy_block_8, 0))
        self.connect((self.epy_block_1, 0), (self.epy_block_2, 0))
        self.connect((self.epy_block_12, 0), (self.blocks_null_sink_1_0, 0))
        self.connect((self.epy_block_1_0_0, 0), (self.epy_block_1_1, 0))
        self.connect((self.epy_block_1_1, 0), (self.epy_block_0_1_0_0, 0))
        self.connect((self.epy_block_2, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.epy_block_3, 0), (self.epy_block_6, 0))
        self.connect((self.epy_block_5, 0), (self.epy_block_8_0, 0))
        self.connect((self.epy_block_6, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.epy_block_6_0, 0), (self.blocks_file_sink_0_1_0, 0))
        self.connect((self.epy_block_6_0, 0), (self.blocks_null_sink_1, 0))
        self.connect((self.epy_block_6_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.epy_block_6_0_0, 0), (self.epy_block_9_0, 0))
        self.connect((self.epy_block_6_0_0, 0), (self.epy_block_9_0_0_0, 0))
        self.connect((self.epy_block_6_0_0_0_0_0, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.epy_block_6_0_1, 0), (self.epy_block_12, 0))
        self.connect((self.epy_block_7_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.epy_block_7_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.epy_block_8, 0), (self.epy_block_6_0_0_0_0_0, 0))
        self.connect((self.epy_block_8_0, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_9, 0), (self.blocks_tagged_stream_align_1_0, 0))
        self.connect((self.epy_block_9_0, 0), (self.blocks_tagged_stream_align_1, 0))
        self.connect((self.epy_block_9_0_0_0, 0), (self.blocks_tagged_stream_align_1_1, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.epy_block_1_0_0, 0))
        self.connect((self.uhd_usrp_source_1, 0), (self.blocks_selector_0, 1))


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
        self.epy_block_1.payload_len = self.payload_len

    def get_SF(self):
        return self.SF

    def set_SF(self, SF):
        self.SF = SF
        self.set_payload_nitems(int(self.payload_nsymb*pow(2,self.SF)))
        self.set_payload_nsymb(int((self.payload_len/self.SF)*(self.CR+4)))
        self.set_preamble_nitems(round(pow(2,self.SF)*(self.preamble_len+2.25)))
        self.epy_block_0.SF = self.SF
        self.epy_block_0_1_0_0.SF = self.SF
        self.epy_block_3.SF = self.SF
        self.epy_block_5.SF = self.SF
        self.epy_block_6_0_0_0_0_0.SF = self.SF

    def get_CR(self):
        return self.CR

    def set_CR(self, CR):
        self.CR = CR
        self.set_payload_nsymb(int((self.payload_len/self.SF)*(self.CR+4)))
        self.epy_block_0.CR = self.CR
        self.epy_block_0_1_0_0.CR = self.CR
        self.epy_block_1.CR = self.CR
        self.epy_block_1_1.CR = self.CR

    def get_success_rate(self):
        return self.success_rate

    def set_success_rate(self, success_rate):
        self.success_rate = success_rate
        self.set_prod(self.success_rate)

    def get_preamble_len(self):
        return self.preamble_len

    def set_preamble_len(self, preamble_len):
        self.preamble_len = preamble_len
        self.set_preamble_nitems(round(pow(2,self.SF)*(self.preamble_len+2.25)))
        self.epy_block_3.preamble_len = self.preamble_len
        self.epy_block_9_0.preamble_len = self.preamble_len
        self.epy_block_9_0_0_0.preamble_len = self.preamble_len

    def get_payload_nsymb(self):
        return self.payload_nsymb

    def set_payload_nsymb(self, payload_nsymb):
        self.payload_nsymb = payload_nsymb
        self.set_payload_nitems(int(self.payload_nsymb*pow(2,self.SF)))

    def get_h_est(self):
        return self.h_est

    def set_h_est(self, h_est):
        self.h_est = h_est
        self.set_prod_01_1(self.h_est)

    def get_frame_nbr_rx(self):
        return self.frame_nbr_rx

    def set_frame_nbr_rx(self, frame_nbr_rx):
        self.frame_nbr_rx = frame_nbr_rx
        self.set_prod_01_0(self.frame_nbr_rx)

    def get_frame_nbr(self):
        return self.frame_nbr

    def set_frame_nbr(self, frame_nbr):
        self.frame_nbr = frame_nbr
        self.set_prod_01(self.frame_nbr)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.set_samp_rate(self.bandwidth)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_1.set_samp_rate(self.samp_rate)

    def get_prod_01_1(self):
        return self.prod_01_1

    def set_prod_01_1(self, prod_01_1):
        self.prod_01_1 = prod_01_1
        Qt.QMetaObject.invokeMethod(self._prod_01_1_label, "setText", Qt.Q_ARG("QString", str(self._prod_01_1_formatter(self.prod_01_1))))

    def get_prod_01_0(self):
        return self.prod_01_0

    def set_prod_01_0(self, prod_01_0):
        self.prod_01_0 = prod_01_0
        Qt.QMetaObject.invokeMethod(self._prod_01_0_label, "setText", Qt.Q_ARG("QString", str(self._prod_01_0_formatter(self.prod_01_0))))

    def get_prod_01(self):
        return self.prod_01

    def set_prod_01(self, prod_01):
        self.prod_01 = prod_01
        Qt.QMetaObject.invokeMethod(self._prod_01_label, "setText", Qt.Q_ARG("QString", str(self._prod_01_formatter(self.prod_01))))

    def get_prod(self):
        return self.prod

    def set_prod(self, prod):
        self.prod = prod
        Qt.QMetaObject.invokeMethod(self._prod_label, "setText", Qt.Q_ARG("QString", str(self._prod_formatter(self.prod))))

    def get_preamble_nitems(self):
        return self.preamble_nitems

    def set_preamble_nitems(self, preamble_nitems):
        self.preamble_nitems = preamble_nitems
        self.epy_block_7_0.preamble_nitems = self.preamble_nitems
        self.epy_block_9.preamble_nitems = self.preamble_nitems*self.os_factor

    def get_payload_nitems(self):
        return self.payload_nitems

    def set_payload_nitems(self, payload_nitems):
        self.payload_nitems = payload_nitems
        self.epy_block_7_0.payload_nitems = self.payload_nitems
        self.epy_block_9.payload_nitems = self.payload_nitems*self.os_factor
        self.epy_block_9_0.payload_nitems = self.payload_nitems
        self.epy_block_9_0_0_0.payload_nitems = self.payload_nitems

    def get_os_factor(self):
        return self.os_factor

    def set_os_factor(self, os_factor):
        self.os_factor = os_factor
        self.epy_block_5.os_factor = self.os_factor
        self.epy_block_9.payload_nitems = self.payload_nitems*self.os_factor
        self.epy_block_9.preamble_nitems = self.preamble_nitems*self.os_factor

    def get_h_simul(self):
        return self.h_simul

    def set_h_simul(self, h_simul):
        self.h_simul = h_simul
        Qt.QMetaObject.invokeMethod(self._h_simul_line_edit, "setText", Qt.Q_ARG("QString", repr(self.h_simul)))
        self.channels_channel_model_0.set_taps([self.h_simul])

    def get_const_multiply(self):
        return self.const_multiply

    def set_const_multiply(self, const_multiply):
        self.const_multiply = const_multiply

    def get_chooser(self):
        return self.chooser

    def set_chooser(self, chooser):
        self.chooser = chooser
        self._chooser_callback(self.chooser)
        self.blocks_selector_0.set_input_index(self.chooser)
        self.blocks_selector_0_0.set_output_index(self.chooser)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)
        self.uhd_usrp_source_1.set_center_freq(self.center_freq, 0)




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

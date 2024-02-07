#!/usr/bin/env python
#
# Copyright 2012,2015 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
#

from gnuradio import gr, filter
from gnuradio import blocks
from gnuradio.fft import window
from tcp_sou import tcp_source
import sys

try:
    from gnuradio import qtgui
    from PyQt5 import QtWidgets, Qt
    import sip
except ImportError:
    sys.stderr.write("Error: Program requires PyQt5 and gr-qtgui.\n")
    sys.exit(1)

try:
    from gnuradio import analog
except ImportError:
    sys.stderr.write("Error: Program requires gr-analog.\n")
    sys.exit(1)

try:
    from gnuradio import channels
except ImportError:
    sys.stderr.write("Error: Program requires gr-channels.\n")
    sys.exit(1)


class dialog_box(QtWidgets.QWidget):
    def __init__(self, display, control):
        QtWidgets.QWidget.__init__(self, None)
        self.setWindowTitle('PyQt Test GUI')

        self.boxlayout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.LeftToRight, self)
        self.boxlayout.addWidget(display, 1)
        self.boxlayout.addWidget(control)

        self.resize(800, 500)


class control_box(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowTitle('Control Panel')

        self.setToolTip('Control the signals')
        QtWidgets.QToolTip.setFont(Qt.QFont('OldEnglish', 10))

        self.layout = QtWidgets.QFormLayout(self)



class my_top_block(gr.top_block):
    def __init__(self, filename):
        gr.top_block.__init__(self)

        fftsize = 2048

        self.qapp = QtWidgets.QApplication(sys.argv)
        ss = open(gr.prefix() + '/share/gnuradio/themes/dark.qss')
        sstext = ss.read()
        ss.close()
        self.qapp.setStyleSheet(sstext)

        src = tcp_source(gr.sizeof_gr_complex, "127.0.0.1", 6000, False)
        thr = blocks.throttle(gr.sizeof_gr_complex, 100 * fftsize)
        self.snk1 = qtgui.sink_c(fftsize, window.WIN_BLACKMAN_hARRIS,
                                 0, 8000,
                                 "Complex Signal Example",
                                 True, True, True, False, None)

        self.connect(src, thr, self.snk1)

        self.ctrl_win = control_box()

        # Get the reference pointer to the SpectrumDisplayForm QWidget
        pyQt = self.snk1.qwidget()

        # Wrap the pointer as a PyQt SIP object
        # This can now be manipulated as a PyQt5.QtWidgets.QWidget
        pyWin = sip.wrapinstance(pyQt, QtWidgets.QWidget)

        self.main_box = dialog_box(pyWin, self.ctrl_win)

        self.main_box.show()


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python your_script.py filename")
        sys.exit(1)
    filename = sys.argv[1]
    tb = my_top_block(filename)
    tb.start()
    tb.qapp.exec_()
    tb.stop()

if __name__ == "__main__":
    tb = my_top_block()
    tb.start()
    tb.qapp.exec_()
    tb.stop()   


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QObject, pyqtSlot
import sys
import gui
import numpy as np
import pyqtgraph as pg
import time
import threading
import multiprocessing as mp


class App(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    # This function is performed everytime the application is launched. It initializes the GUI and all of its parameters
    def __init__(self, parent=None):
        # Initialize
        super(App, self).__init__(parent)
        self.setupUi(self)

        # Initialize variable
        self.savepath = ""
        self.has_savepath = False
        self.xdata = [[], [], [], []]
        self.ydata = [[], [], [], []]
        self.fxdata = [[], [], [], []]
        self.fydata = [[], [], [], []]
        self.threads = []
        self.threadpool = QtCore.QThreadPool()

        # Associate callbacks
        self.btn_startstop.clicked.connect(self.startstop)
        self.btn_browse.clicked.connect(self.browse)

        # Initialize graphs
        self.timers = []
        self.plotlist = [self.tsgraph_el1, self.tsgraph_el2, self.tsgraph_el3, self.tsgraph_el4,
                         self.fsgraph_el1, self.fsgraph_el2, self.fsgraph_el3, self.fsgraph_el4]
        plottitles = ['Time Series - Electrode 1', 'Time Series - Electrode 2', 'Time Series - Electrode 3',
                      'Time Series - Electrode 4', 'Frequency Spectrum - Electrode 1',
                      'Frequency Spectrum - Electrode 2', 'Frequency Spectrum - Electrode 3',
                      'Frequency Spectrum - Electrode 4']
        plotlinecolors = ['r','g','c','y','r','g','c','y']
        self.curve = []
        for itr in range(len(self.plotlist)):
            g = self.plotlist[itr]
            g.plotItem.setTitle(plottitles[itr])
            if itr < 4:
                g.plotItem.setLabel('left','Amplitude','?')
                g.plotItem.setLabel('bottom','Time','s')
                g.plotItem.getViewBox().setXRange(0, 10)
            else:
                g.plotItem.setLabel('left','Amplitude','?')
                g.plotItem.setLabel('bottom','Frequency','Hz')
                g.plotItem.getViewBox().setXRange(0, 60)
            g.plotItem.getViewBox().setMouseEnabled(False)
            g.plotItem.getViewBox().setMenuEnabled(False)
            self.curve.append(g.plotItem.plot())
            self.curve[itr].setPen(plotlinecolors[itr])


    def startstop(self):
        if self.btn_startstop.text() == "START":
            self.btn_startstop.setText("STOP")
            # Start acquisition
            self.threads = []
            if self.group_el1.isChecked():
                self.threads.append(AcquisitionThread(0))
                self.threads[-1].signals.data.connect(self.update_data)
                # self.threads.append(PlottingThread(self.update_plot, 0))
            if self.group_el2.isChecked():
                self.threads.append(AcquisitionThread(1))
                self.threads[-1].signals.data.connect(self.update_data)
                # self.threads.append(PlottingThread(self.update_plot, 1))
            if self.group_el3.isChecked():
                self.threads.append(AcquisitionThread(2))
                self.threads[-1].signals.data.connect(self.update_data)
                # self.threads.append(PlottingThread(self.update_plot, 2))
            if self.group_el4.isChecked():
                self.threads.append(AcquisitionThread(3))
                self.threads[-1].signals.data.connect(self.update_data)
                # self.threads.append(PlottingThread(self.update_plot, 3))
            for t in self.threads:
                self.threadpool.start(t)
                t.start_button()

        elif self.btn_startstop.text() == "STOP":
            self.btn_startstop.setText("START")
            # Stop acquisition
            for t in self.threads:
                t.stop_button()

    # Callback function of the "Browse" button, which is used to ask the user where to save data after acquisition.
    def browse(self):
        self.savepath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.has_savepath = True
        self.ed_saveloc.setText(self.savepath)

    # Emit functions (launched when emitting from the QThread objects
    def update_data(self, data):
        plot_id = data[0]
        self.xdata[plot_id] = data[1]
        self.ydata[plot_id] = data[2]
        self.fxdata[plot_id] = data[3]
        self.fydata[plot_id] = data[4]
        self.update_plot(plot_id)

    def update_plot(self, plot_id):
        # TODO : Adjust range from parameters in GUI
        if self.data_valid(plot_id):
            self.curve[plot_id].setData(self.xdata[plot_id], self.ydata[plot_id])
            self.curve[plot_id+4].setData(self.fxdata[plot_id], self.fydata[plot_id])

    # Validation functions
    def data_valid(self, plot_id):
        if len(self.xdata[plot_id]) != len(self.ydata[plot_id]):
            return False
        if len(self.fxdata[plot_id]) != len(self.fydata[plot_id]):
            return False
        # TODO : Add other validation? (data type, etc.)
        return True


# class PlottingSignals(QObject):
#     data = pyqtSignal(object)  # [[xdata],[ydata],[fxdata],[fydata]]
#     plot_id = pyqtSignal(int)
#
#
# class PlottingThread(QtCore.QRunnable):
#     def __init__(self, fn, plot_id, *args, **kwargs):
#         super(PlottingThread, self).__init__()
#         # QThread.__init__(self)
#         self.fn = fn
#         self.plot_id = plot_id
#         self.args = args
#         self.kwargs = kwargs
#         self.started = False
#         self.signals = PlottingSignals()
#
#     # def __del__(self):
#     #     self.wait()
#
#     @pyqtSlot()
#     def run(self):
#         while self.started:
#             self.fn(self.plot_id)
#             #time.sleep(0.2)
#
#     def start_button(self):
#         self.started = True
#
#     def stop_button(self):
#         self.started = False


class AcquisitionSignals(QObject):
    data = pyqtSignal(object)  # [plot_id, [xdata],[ydata],[fxdata],[fydata]]


class AcquisitionThread(QtCore.QRunnable):
    def __init__(self, plot_id, *args, **kwargs):
        super(AcquisitionThread, self).__init__()
        self.setAutoDelete(True)
        # QThread.__init__(self)
        self.plot_id = plot_id
        self.args = args
        self.kwargs = kwargs
        self.started = False
        self.signals = AcquisitionSignals()


    @pyqtSlot()
    def run(self):
        while self.started:
            # TODO : Acquisition from server + Add data properly (push according to buffer size)
            xdata = range(60)
            ydata = np.random.random(len(xdata))
            fxdata = range(60)
            fydata = np.random.random(len(fxdata))
            self.signals.data.emit([self.plot_id, xdata, ydata, fxdata, fydata])
            time.sleep(0.1)

    def start_button(self):
        self.started = True

    def stop_button(self):
        self.started = False


def main():
    app = QtWidgets.QApplication(sys.argv)
    wndw = App()
    wndw.show()
    app.exec()


if __name__ == '__main__':
    main()

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
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

        # initialise your qthread objects, i only did one
        
        self.runPlot_=runPlot()
        self.runPlot.signal.connect(self.plot) # ton signal emit dna

        # Initialize variable
        self.savepath = ""
        self.has_savepath = False
        self.xdata = [[], [], [], []]
        self.ydata = [[], [], [], []]
        self.fxdata = [[], [], [], []]
        self.fydata = [[], [], [], []]
        self.threads = []

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

        # Display window

    def startstop(self):
        if self.btn_startstop.text() == "START":
            self.btn_startstop.setText("STOP")
            # Start acquisition
            # if self.group_el1.isChecked():
            #     self.threads.append(self.PlotThread(self, 'pl_el1', 0))
            #     self.threads.append(self.AcquireThread(self, 'ac_el1', 0))
            # if self.group_el2.isChecked():
            #     self.threads.append(self.PlotThread(self, 'pl_el2', 1))
            #     self.threads.append(self.AcquireThread(self, 'ac_el2', 1))
            # if self.group_el3.isChecked():
            #     self.threads.append(self.PlotThread(self, 'pl_el3', 2))
            #     self.threads.append(self.AcquireThread(self, 'ac_el3', 2))
            # if self.group_el4.isChecked():
            #     self.threads.append(self.PlotThread(self, 'pl_el4', 3))
            #     self.threads.append(self.AcquireThread(self, 'ac_el4', 3))
            # self.threads[0].start()
            # self.threads[1].start()
            self.threads = []
            if self.group_el1.isChecked():
                self.threads.append(threading.Thread(target=self.runAcquisition, args=(0,)))
                self.threads.append(threading.Thread(target=self.runPlot, args=(0,)))
            if self.group_el2.isChecked():
                self.threads.append(threading.Thread(target=self.runAcquisition, args=(1,)))
                self.threads.append(threading.Thread(target=self.runPlot, args=(1,)))
            if self.group_el3.isChecked():
                self.threads.append(threading.Thread(target=self.runAcquisition, args=(2,)))
                self.threads.append(threading.Thread(target=self.runPlot, args=(2,)))
            if self.group_el4.isChecked():
                self.threads.append(threading.Thread(target=self.runAcquisition, args=(3,)))
                self.threads.append(threading.Thread(target=self.runPlot, args=(3,)))
            for t in self.threads:
                t.start()

        elif self.btn_startstop.text() == "STOP":
            self.btn_startstop.setText("START")
            # Stop acquisition
            for t in self.threads:
                pass

    # Callback function of the "Browse" button, which is used to ask the user where to save data after acquisition.
    def browse(self):
        self.savepath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.has_savepath = True
        self.ed_saveloc.setText(self.savepath)
        
    def plot(self,plotId):
        

    """
    # _TEST FUNCTION_
    def test_testplot(self):
            self.timers = QtCore.QTimer()
            self.timers.timeout.connect(self.test_updatedata)
            self.timers.start(50)

    # _TEST FUNCTION_
    def test_updatedata(self):
        for i in range(len(self.curve)):
            x = range(60)
            y = np.random.random(len(x))
            self.updateplot(i, x, y)
    
    # Function which updates plot with the data contained in xdata (x-axis) and ydata (y-axis)
    def updateplot(self, pltnumber, xdata, ydata):
        # Function to update the plot pltnumber in the gui using with xdata and ydata, both arrays
        # pltnumber = 0 to 7 (0 = first left, 7 = last right in the layout)
        assert len(xdata) == len(ydata), "xdata (%r) and ydata (%r) aren't the same length" % (len(xdata), len(ydata))

        # Get range parameters
        # TODO

        # Plot data
        self.curve[pltnumber].setData(xdata, ydata)
    """

class runPlot(QThread):
    signal=pyqtSignal(objet)
    # emit signal once you want to plot something, that should pass arguments to a function that will just do plot when triggered
        
    def __init__(self):
        QThread.__init__(self)
        self.startButton=False
        
    def __del__(self):
        self.wait()
    def startButton(self):
        self.startButton=True
    
    def stopButton(self):
        self.stopButton=False
    
    def passArgs(self,plotid):
        #in here pass arguments

    def run(self): #### when you wanna start this thread do nameOfThread.start()
        ## faire des update ici, et emettre tes signaux icu
        while self.stopButton:
            QtWidgets.QApplication.processEvents()
            if (len(self.xdata[plotid]) != 0) & (len(self.fxdata[plotid]) != 0) & (len(self.xdata[plotid]) == len(self.ydata[plotid])) & (len(self.fxdata[plotid]) == len(self.fydata[plotid])):
                self.curve[plotid].setData(self.xdata[plotid], self.ydata[plotid])
                self.curve[plotid+4].setData(self.fxdata[plotid], self.fydata[plotid])





###### same as abovvvvve
      def runAcquisition(self, plotid, testflag=True):
        while self.btn_startstop.text() == "STOP":
            QtWidgets.QApplication.processEvents()
            if testflag:
                self.xdata[plotid] = range(60)
                self.ydata[plotid] = np.random.random(len(self.xdata[plotid]))
                self.fxdata[plotid] = range(60)
                self.fydata[plotid] = np.random.random(len(self.xdata[plotid]))

    # CUSTOM CLASSES #############
class PlotThread(QThread):
    signal=pyqtSignal(object)
    def __init__(self, ghandle, name, plotid):
            QThread.__init__(self)
            self.id = plotid
            self.name = name
            self.errorCount = 0
            self.ghandle = ghandle
    def __del__(self):
        self.wait()

    def run(self):
            while True:
                try:
                    if (len(self.ghandle.xdata[self.id]) != 0) & (len(self.ghandle.fxdata[self.id]) != 0):
                        # TODO: get range parameters and adjust graphs according to those
                        self.ghandle.curve[self.id].setData(self.ghandle.xdata[self.id], self.ghandle.ydata[self.id])
                        self.ghandle.curve[self.id+4].setData(self.ghandle.fxdata[self.id], self.ghandle.fydata[self.id])
                finally:
                    self.errorCount += 1
                    if self.errorCount > 10:
                        pass

class AcquireThread(QThread):
    signal=pyqtSignal(object)        
   
    def __init__(self, ghandle, name, plotid, testflag=True):
        QThread.__init__(self)
        self.id = plotid
        self.name = name
        self.errorCount = 0
        self.ghandle = ghandle
        self.testflag = testflag
            # TODO: Initialize communication with server
            
    def __del__(self):
        self.wait()
    def run(self):
        while True:
            try:
                if self.testflag:
                    self.ghandle.xdata[self.id] = range(60)
                    self.ghandle.ydata[self.id] = np.random.random(len(self.ghandle.xdata[self.id]))
                    self.ghandle.fxdata[self.id] = range(60)
                    self.ghandle.fydata[self.id] = np.random.random(len(self.ghandle.xdata[self.id]))
                 else:
                    pass
                        # TODO: get data from server and place in arrays
                time.sleep(0.001)  # TODO: Change 0.001 to the acquisition frequency?
            finally:
                self.errorCount += 1
                if self.errorCount > 10:
                    pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    wndw = App()
    wndw.show()
    app.exec()


if __name__ == '__main__':
    main()

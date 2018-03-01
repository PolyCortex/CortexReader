from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import gui
import numpy as np
import pyqtgraph as pg
import time
import threading


class App(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        # Initialize
        super(App, self).__init__(parent)
        self.setupUi(self)

        # Initialize variable
        self.savepath = ""
        self.has_savepath = False

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
            self.test_testplot()
        elif self.btn_startstop.text() == "STOP":
            self.btn_startstop.setText("START")
            # Stop acquisition
            self.timers.stop()

    def browse(self):
        self.savepath = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.has_save1path = True
        self.ed_saveloc.setText(self.savepath)
        self.ed_saveloc.
1
    def test_testplot(self):
            self.timers = QtCore.QTimer()
            self.timers.timeout.connect(self.test_updatedata)
            self.timers.start(50)

    def test_updatedata(self):
        for i in range(len(self.curve)):
            x = range(60)
            y = np.random.random(len(x))
            self.updateplot(i, x, y)

    def updateplot(self, pltnumber, xdata, ydata):
        # Function to update the plot pltnumber in the gui using with xdata and ydata, both arrays
        # pltnumber = 0 to 7 (0 = first left, 7 = last right in the layout)
        assert len(xdata) == len(ydata), "xdata (%r) and ydata (%r) aren't the same length" % (len(xdata), len(ydata))

        # Get range parameters
        # TODO

        # Plot data
        self.curve[pltnumber].setData(xdata, ydata)

def main():
    app = QtWidgets.QApplication(sys.argv)
    wndw = App()
    wndw.show()
    app.exec()


if __name__ == '__main__':
    main()

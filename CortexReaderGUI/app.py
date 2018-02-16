from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import gui


class App(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)
        self.setupUi(self)

        # Associate callbacks
        self.btn_startstop.clicked.connect(self.startstop)

    def startstop(self):
        if self.btn_startstop.text() == "START":
            self.btn_startstop.setText("STOP")
            # Start acquisition
        elif self.btn_startstop.text() == "STOP":
            self.btn_startstop.setText("START")
            # Stop acquisition


def main():
    app = QtWidgets.QApplication(sys.argv)
    wndw = App()
    wndw.show()
    app.exec()


if __name__ == '__main__':
    main()

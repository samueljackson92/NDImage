import sys
from PyQt4 import QtGui
from gui.main_window import NDImageWindow


def main():
    app = QtGui.QApplication(sys.argv)
    window = NDImageWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

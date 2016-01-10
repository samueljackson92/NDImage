from PyQt4 import QtGui, QtCore
from . import get_ui_file
from mpl_canvas import StaticMplCanvas
from table_view import TableView
form_class = get_ui_file("main.ui")


class NDImageWindow(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        # menu bar
        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        static_canvas = StaticMplCanvas(self, width=2, height=2, dpi=100)
        self.mainHBoxLayout.addWidget(static_canvas)

        data = {'col1':['1','2','3'],
                'col2':['4','5','6'],
                'col3':['7','8','9']}

        static_table_view = TableView(data, 5, 3)
        self.rightVBoxLayout.addWidget(static_table_view)

    def fileQuit(self):
        self.close()

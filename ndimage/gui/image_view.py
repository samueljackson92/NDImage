from PyQt import QtGui

class TableView(QtGui.QFrame):
    def __init__(self, parent=None):
        QtGui.QTableWidget.__init__(self, parent)

        self._image = QtGui.QLabel(parent)
        self._image.setGeometry(10, 10, 400, 100)
        self._image.setPixmap(QtGui.QPixmap(os.getcwd() + "/logo.png"))
        
        self._layout = QtGui.
        self._layout.addWidget(static_canvas)
        self.setLayout()

    def load_image():

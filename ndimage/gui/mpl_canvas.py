from __future__ import unicode_literals
from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class PandasMplWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.figure = PandasMplCanvas(width=2, height=2, dpi=100)
        self.toolbar = NavigationToolbar(self.get_canvas(), self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(True)
        self.toolbar.setSizePolicy(sizePolicy)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.figure)
        vbox.addWidget(self.toolbar)
        self.setLayout(vbox)

    def get_canvas(self):
        return self.figure.figure.canvas

    def plot(self, data):
        self.figure.plot_data_frame(data)


class PandasMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plot_data_frame(self, dataFrame):
        x = dataFrame[[0]]
        y = dataFrame[[1]]
        self.axes.scatter(x, y, picker=True)
        self.draw()

from __future__ import unicode_literals
from PyQt4 import QtGui
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class PandasMplWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.pmc = PandasMplCanvas(width=2, height=2, dpi=100)
        self.toolbar = NavigationToolbar(self.pmc.figure.canvas, self)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(True)
        self.toolbar.setSizePolicy(sizePolicy)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.pmc)
        vbox.addWidget(self.toolbar)
        self.setLayout(vbox)

    def get_figure_canvas(self):
        return self.pmc

    def plot(self, data):
        self.pmc.plot_data_frame(data)


class PandasMplCanvas(FigureCanvas):
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
        self.points = self.axes.scatter(x, y, picker=True)
        self.reset_face_color()
        self.draw()

    def set_class_label(self, labels):
        categories = np.unique(labels)
        colors = np.linspace(0, 1, len(categories))
        colordict = dict(zip(categories, colors))
        colour_weights = labels.apply(lambda x: colordict[x])
        color_map = plt.get_cmap("Spectral")
        class_colors = color_map(colour_weights)
        # copy existing alpha values
        class_colors[:, -1] = self.face_color[:, -1]
        self.face_color = class_colors
        self.points.set_facecolors(self.face_color)
        self.draw()

    def reset_face_color(self):
        npts = len(self.points.get_offsets())
        self.face_color = self.points.get_facecolors()
        self.face_color = np.tile(self.face_color, npts).reshape(npts, -1)

    def reset_color(self):
        self.face_color = self.points.get_facecolors()
        self.face_color[:, -1] = 1
        self.points.set_facecolors(self.face_color)
        self.draw()

    def highlight_points(self, idx, alpha=0.2):
        self.face_color[:, -1] = alpha
        self.face_color[idx, -1] = 1
        self.points.set_facecolors(self.face_color)

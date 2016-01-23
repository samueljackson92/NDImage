
from PyQt4 import QtGui
from . import get_ui_file

import numpy as np

from gui.table_view import PandasTableView
from gui.table_model import DataFrameTableModel
from gui.mpl_canvas import PandasMplWidget
from controllers.menu_controller import (
    FileMenuListener, ProjectionMenuListener)
from controllers.mpl_canvas_controller import MplCanvasListener

form_class = get_ui_file("main.ui")


class NDImageWindow(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.fileController = FileMenuListener(self)
        self.projectionController = ProjectionMenuListener(self)

        self.datasetTable = DataFrameTableModel()
        self.projectionTable = DataFrameTableModel()

        self.datasetTableView = PandasTableView(self)
        self.projectionTableView = PandasTableView(self)

        self.datasetTableView.setModel(self.datasetTable)
        self.datasetTableView.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        self.projectionTableView.setModel(self.projectionTable)
        self.projectionTableView.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)

        self.figure = PandasMplWidget()
        self.mplCanvasController = MplCanvasListener(self.figure.get_figure_canvas(), self)

        self.mainHBoxLayout.addWidget(self.figure)
        self.topVBoxLayout.addWidget(self.datasetTableView)
        self.bottomVBoxLayout.addWidget(self.projectionTableView)

    def get_dataset(self):
        return self.datasetTable.get_data()

    def get_projection(self):
        return self.projectionTable.get_data()

    def select_rows(self, index):
        self.projectionTableView.clearSelection()
        self.datasetTableView.clearSelection()

        # if the index is a single number convert it to an iterable
        if isinstance(index, int):
            index = [index]

        # iterate and set all rows to selected
        for i in index:
            self.datasetTableView.selectRow(i)
            self.projectionTableView.selectRow(i)

    def get_selected_rows(self):
        return self.datasetTableView.selectedIndexes()

    def deselect_all_rows(self):
        self.datasetTableView.clearSelection()
        self.projectionTableView.clearSelection()

    def get_selected_data(self):
        idx = [item.row() for item in self.get_selected_rows()]
        idx = np.unique(idx)
        df = self.get_dataset()
        return df.iloc[idx].describe()

    def update_projection(self, projection):
        self.projectionTable.set_data(projection)
        self.figure.plot(projection)

    def update_dataset(self, dataset):
        self.datasetTable.set_data(dataset)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def fileQuit(self):
        self.close()

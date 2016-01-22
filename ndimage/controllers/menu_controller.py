
from PyQt4 import QtGui
import os.path

import pandas as pd
from sklearn.decomposition import PCA
from fileprocessing.data_loader import DataLoader
from mpl_canvas_controller import MplCanvasLassoSelector

from algorithms.algorithm_factory import AlgorithmFactory
from gui.dialogs import StatsDialog, AlgorithmDialog
from gui.table_model import DataFrameTableModel


class FileMenuListener(object):

    def __init__(self, parent):
        self._parent = parent
        self._dataLoader = DataLoader()
        parent.actionLoad_Dataset.triggered.connect(self.action_load_dataset)
        parent.actionLoad_Projection.triggered.connect(self.action_load_projection)

    def action_load_dataset(self, event):
        dataset = self._load_data_file()
        self._parent.update_dataset(dataset)

    def action_load_projection(self, event):
        projection = self._load_data_file()
        self._parent.update_projection(projection)

    def _load_data_file(self):
        file_name = self._show_open_file_dialog()
        data_frame = self._dataLoader.load_csv(file_name)
        return data_frame

    def _show_open_file_dialog(self):
        home_dir = os.path.expanduser("~")
        filename = QtGui.QFileDialog.getOpenFileName(self._parent, 'Open file', home_dir)
        return str(filename)


class ProjectionMenuListener(object):

    def __init__(self, parent):
        self._parent = parent
        self._parent.actionCreate_Projection.triggered.connect(self.action_create_projection)
        self._parent.actionSelect_Points.triggered.connect(self.action_select_points)
        self._parent.actionDeselect_All.triggered.connect(self.action_deselect_points)
        self._parent.actionSelection_Statistics.triggered.connect(self.action_selection_statistics)

    def action_select_points(self, event):
        fig_canvas = self._parent.figure.get_figure_canvas()
        self.selector = MplCanvasLassoSelector(fig_canvas, self._parent)

    def action_deselect_points(self, event):
        self._parent.figure.get_figure_canvas().reset_color()
        self._parent.deselect_all_rows()

    def action_selection_statistics(self, event):
        data = self._parent.get_selected_data()
        model = DataFrameTableModel(data=data, parent=self._parent)
        dialog = StatsDialog(model, self._parent)
        dialog.show()

    def action_create_projection(self, event):
        name, parameters, ok = AlgorithmDialog.getAlgorithmParameters(self._parent)
        if ok:
            dataset = self._parent.get_dataset()
            algorithm = AlgorithmFactory.create(name, parameters)
            projection = algorithm.fit_transform(dataset)
            projection = pd.DataFrame(projection)
            self._parent.update_projection(projection)

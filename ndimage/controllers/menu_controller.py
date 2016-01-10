
from PyQt4 import QtGui
import os.path

import pandas as pd
from sklearn.decomposition import PCA
from fileprocessing.data_loader import DataLoader
from gui.table_view import DataFrameTableView


class MenuController(object):

    def __init__(self, fileMenu, parent):
        self.parent = parent
        self._dataLoader = DataLoader()

        loadDatasetAction = QtGui.QAction('Load Dataset', parent)
        loadDatasetAction.setStatusTip('Load Dataset')
        loadDatasetAction.triggered.connect(self.load_dataset)
        fileMenu.addAction(loadDatasetAction)

        loadProjectionAction = QtGui.QAction('Load Projection', parent)
        loadProjectionAction.setStatusTip('Load Projection')
        loadProjectionAction.triggered.connect(self.load_projection)
        fileMenu.addAction(loadProjectionAction)

    def load_dataset(self, event):
        data_frame = self._load_data_file()
        self.parent._dataset = data_frame
        table_view = DataFrameTableView(data_frame)
        self._set_table_view(table_view, self.parent.topVBoxLayout)

    def load_projection(self, event):
        data_frame = self._load_data_file()
        self.parent._projection = data_frame
        table_view = DataFrameTableView(data_frame)
        self._set_table_view(table_view, self.parent.bottomVBoxLayout)

        self.parent.figure.plot_data_frame(data_frame)
        self.parent.mainHBoxLayout.addWidget(self.parent.figure)

    def _load_data_file(self):
        file_name = self._show_open_file_dialog()
        data_frame = self._dataLoader.load_csv(file_name)
        return data_frame

    def _set_table_view(self, table_view, layout):
        self.parent.clear_layout(layout)
        layout.addWidget(table_view)

    def _show_open_file_dialog(self):
        home_dir = os.path.expanduser("~")
        filename = QtGui.QFileDialog.getOpenFileName(self.parent, 'Open file', home_dir)
        return str(filename)


class CreateProjectionMenuController(object):

    def __init__(self, createProjectionMenu, parent):
        self.parent = parent

        pcaProjectionAction = QtGui.QAction('PCA', parent)
        pcaProjectionAction.setStatusTip('PCA')
        pcaProjectionAction.triggered.connect(self.run_pca)
        createProjectionMenu.addAction(pcaProjectionAction)

    def run_pca(self, event):
        X = self.parent._dataset
        pca = PCA(n_components=2)
        X_r = pca.fit(X).transform(X)
        projection = pd.DataFrame(X_r)

        self.parent.figure.plot_data_frame(projection)
        table_view = DataFrameTableView(projection)
        self._set_table_view(table_view, self.parent.bottomVBoxLayout)
        self._projection = projection

    def _set_table_view(self, table_view, layout):
        self.parent.clear_layout(layout)
        layout.addWidget(table_view)

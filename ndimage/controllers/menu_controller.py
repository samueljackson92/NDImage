
from PyQt4 import QtGui
import os.path

import pandas as pd
from sklearn.decomposition import PCA
from fileprocessing.data_loader import DataLoader


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


class CreateProjectionMenuListener(object):

    def __init__(self, parent):
        self._parent = parent
        parent.actionPCA.triggered.connect(self.action_run_pca)

    def action_run_pca(self, event):
        dataset = self._parent.get_dataset()
        projection = self.run_pca(dataset)
        self._parent.update_projection(projection)

    def run_pca(self, X):
        pca = PCA(n_components=2)
        X_r = pca.fit(X).transform(X)
        return pd.DataFrame(X_r)

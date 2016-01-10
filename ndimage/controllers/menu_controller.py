
from PyQt4 import QtGui
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
        table_view = DataFrameTableView(data_frame)
        self._set_table_view(table_view, self.parent.topVBoxLayout)

    def load_projection(self, event):
        data_frame = self._load_data_file()
        table_view = DataFrameTableView(data_frame)
        self._set_table_view(table_view, self.parent.bottomVBoxLayout)

    def _load_data_file(self):
        file_name = self._show_open_file_dialog()
        data_frame = self._dataLoader.load_csv(file_name)
        return data_frame

    def _set_table_view(self, table_view, layout):
        self.parent.clear_layout(layout)
        layout.addWidget(table_view)

    def _show_open_file_dialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self.parent, 'Open file', '/home')
        return str(filename)

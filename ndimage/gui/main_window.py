
from PyQt4 import QtGui
from . import get_ui_file

from gui.table_model import DataFrameTableModel
from gui.mpl_canvas import PandasMplCanvas
from controllers.menu_controller import FileMenuListener, CreateProjectionMenuListener

form_class = get_ui_file("main.ui")


class NDImageWindow(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.fileController = FileMenuListener(self)
        self.createProjectionMenuController = CreateProjectionMenuListener(self)

        self.figure = PandasMplCanvas(width=2, height=2, dpi=100)
        self.datasetTable = DataFrameTableModel()
        self.projectionTable = DataFrameTableModel()

        datasetTableView = QtGui.QTableView()
        projectionTableView = QtGui.QTableView()
        datasetTableView.setModel(self.datasetTable)
        projectionTableView.setModel(self.projectionTable)

        self.mainHBoxLayout.addWidget(self.figure)
        self.topVBoxLayout.addWidget(datasetTableView)
        self.bottomVBoxLayout.addWidget(projectionTableView)

    def get_dataset(self):
        return self.datasetTable.get_data()

    def update_projection(self, projection):
        self.projectionTable.set_data(projection)
        self.figure.plot_data_frame(projection)

    def update_dataset(self, dataset):
        self.datasetTable.set_data(dataset)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def fileQuit(self):
        self.close()

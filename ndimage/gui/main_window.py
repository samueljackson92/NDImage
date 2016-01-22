
from PyQt4 import QtGui
from . import get_ui_file

from gui.table_model import DataFrameTableModel
from gui.mpl_canvas import PandasMplWidget
from controllers.menu_controller import FileMenuListener, CreateProjectionMenuListener
from controllers.mpl_canvas_controller import MplCanvasListener

form_class = get_ui_file("main.ui")


class NDImageWindow(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.fileController = FileMenuListener(self)
        self.createProjectionMenuController = CreateProjectionMenuListener(self)

        self.datasetTable = DataFrameTableModel()
        self.projectionTable = DataFrameTableModel()

        self.datasetTableView = QtGui.QTableView()
        self.projectionTableView = QtGui.QTableView()
        self.datasetTableView.setModel(self.datasetTable)
        self.projectionTableView.setModel(self.projectionTable)

        self.figure = PandasMplWidget()
        self.mplCanvasController = MplCanvasListener(self.figure.get_canvas(), self)

        self.mainHBoxLayout.addWidget(self.figure)
        self.topVBoxLayout.addWidget(self.datasetTableView)
        self.bottomVBoxLayout.addWidget(self.projectionTableView)

    def get_dataset(self):
        return self.datasetTable.get_data()

    def get_projection(self):
        return self.projectionTable.get_data()

    def select_rows(self, index):
        self.datasetTableView.selectRow(index)
        self.projectionTableView.selectRow(index)

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

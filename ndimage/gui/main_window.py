
from PyQt4 import QtGui
from . import get_ui_file
from gui.mpl_canvas import PandasMplCanvas
from controllers.menu_controller import MenuController, CreateProjectionMenuController
form_class = get_ui_file("main.ui")


class NDImageWindow(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):

        fileMenu = self.menuFile
        createProjectionMenu = self.menuCreate_Projection
        self.fileController = MenuController(fileMenu, self)
        self.createProjectionMenuController = CreateProjectionMenuController(createProjectionMenu, self)

        self.figure = PandasMplCanvas(width=2, height=2, dpi=100)
        self.mainHBoxLayout.addWidget(self.figure)
        self.bottomVBoxLayout.addWidget(QtGui.QTableWidget(0, 0))
        self.topVBoxLayout.addWidget(QtGui.QTableWidget(0, 0))

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def fileQuit(self):
        self.close()

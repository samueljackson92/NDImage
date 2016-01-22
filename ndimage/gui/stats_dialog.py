
from PyQt4 import QtGui
from . import get_ui_file

dialog_class = get_ui_file("stats.ui")


class StatsDialog(QtGui.QDialog, dialog_class):
    def __init__(self, model, parent=None):
        self._parent = parent
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.init_ui(model)

    def init_ui(self, model):
        self.statisticsTable.setModel(model)
        self.statisticsTable.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

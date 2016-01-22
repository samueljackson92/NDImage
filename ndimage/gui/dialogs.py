
from PyQt4 import QtGui
from . import get_ui_file

stats_class = get_ui_file("stats.ui")
algorithm_class = get_ui_file("algorithm.ui")


class StatsDialog(QtGui.QDialog, stats_class):
    def __init__(self, model, parent=None):
        self._parent = parent
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.init_ui(model)

    def init_ui(self, model):
        self.statisticsTable.setModel(model)
        self.statisticsTable.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)


class AlgorithmDialog(QtGui.QDialog, algorithm_class):
    def __init__(self, parent=None):
        self._parent = parent
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        pass

    def get_algorithm_name(self):
        return str(self.algorithmName.currentText())

    @staticmethod
    def getAlgorithmParameters(parent=None):
        dialog = AlgorithmDialog(parent)
        result = dialog.exec_()
        name = dialog.get_algorithm_name()
        parameters = {}
        return (name, parameters, result == QtGui.QDialog.Accepted)

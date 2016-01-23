
from PyQt4 import QtGui, QtCore
from . import get_ui_file
from algorithms.algorithm_factory import AlgorithmFactory

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
        self.statisticsTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)


class AlgorithmDialog(QtGui.QDialog, algorithm_class):
    def __init__(self, parent=None):
        self._parent = parent
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.connect(self.algorithmName, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self._update_parameters)
        self._setup_parameter_table()
        self._update_parameters(self.get_algorithm_name())

    def _setup_parameter_table(self):
        self.parameterTable.setColumnCount(2)
        self.parameterTable.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.parameterTable.setHorizontalHeaderLabels(['Name', 'Value'])

    def _update_parameters(self, alg_name):
        default_parameters = AlgorithmFactory.get_algorithm_parameters(str(alg_name))

        self.parameterTable.setRowCount(len(default_parameters))

        for i, (name, value) in enumerate(default_parameters):
            self.parameterTable.setItem(i, 0, QtGui.QTableWidgetItem(name))
            self.parameterTable.setItem(i, 1, QtGui.QTableWidgetItem(str(value)))

    def get_algorithm_name(self):
        return str(self.algorithmName.currentText())

    def parse_columns(self):
        columns_text = str(self.columnsEditor.text())
        if columns_text == "":
            return None

        parts = columns_text.split(',')

        def convert_type(x):
            try:
                return int(x)
            except ValueError:
                return str(x)

        idx = map(convert_type, parts)
        return idx

    def get_parameters(self):
        names = [str(self.parameterTable.item(row, 0).text())
                 for row in xrange(self.parameterTable.rowCount())]

        values = [str(self.parameterTable.item(row, 1).text())
                  for row in xrange(self.parameterTable.rowCount())]

        values = map(self.convert_parameter_type, values)
        return dict(zip(names, values))

    def convert_parameter_type(self, value):
        if value == 'None':
            return None

        for type_ in [int, float, str]:
            try:
                return type_(value)
            except ValueError:
                continue

    @staticmethod
    def getAlgorithmParameters(parent=None):
        dialog = AlgorithmDialog(parent)
        result = dialog.exec_()
        name = dialog.get_algorithm_name()
        columns = dialog.parse_columns()
        parameters = dialog.get_parameters()
        return (name, parameters, columns, result == QtGui.QDialog.Accepted)

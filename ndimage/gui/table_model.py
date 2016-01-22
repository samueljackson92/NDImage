from PyQt4 import QtCore


class DataFrameTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data=None, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self.set_data(data)

    def rowCount(self, parent):
        return self._data.shape[0] if self._data is not None else 0

    def columnCount(self, parent):
        return self._data.shape[1] if self._data is not None else 0

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        value = self._data.iloc[index.row()][index.column()]
        return QtCore.QVariant(str(value))

    def get_data(self):
        return self._data

    def set_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

from PyQt4 import QtGui


class DataFrameTableView(QtGui.QTableWidget):
    def __init__(self, data, parent=None):
        QtGui.QTableWidget.__init__(self, data.shape[0],
                                    data.shape[1], parent=parent)
        self._data = data
        self.set_data(data)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def get_data(self):
        return self._data

    def set_data(self, data):
        for i, (key, row) in enumerate(data.iterrows()):
            row = row.astype(str)
            for j, item in enumerate(row):
                self.set_item(i, j, item)

        self.setHorizontalHeaderLabels(data.columns.astype(str))
        self.setVerticalHeaderLabels(data.index.astype(str))

    def set_item(self, i, j, elem):
        widget = QtGui.QTableWidgetItem(elem)
        self.setItem(i, j, widget)

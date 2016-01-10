from PyQt4 import QtGui


class TableView(QtGui.QTableWidget):
    def __init__(self, data, *args):
        QtGui.QTableWidget.__init__(self, *args)
        self.data = data
        self.set_data()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def set_data(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QtGui.QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

from PyQt4 import QtGui, QtCore


class PandasTableView(QtGui.QTableView):
    def __init__(self, parent=None):
        super(PandasTableView, self).__init__()
        self._parent = parent

        self.header = self.horizontalHeader()
        self.header.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.header.customContextMenuRequested.connect(self.context_menu_event)
        self.header.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

        self.header.setMovable(True)
        self.header.setDragEnabled(True)
        self.header.setDragDropMode(QtGui.QAbstractItemView.InternalMove)

    def context_menu_event(self, pos):
        self._current_index = int(self.header.logicalIndexAt(pos))
        parentPosition = self.mapToGlobal(pos)

        menu = QtGui.QMenu()
        action_set_index = QtGui.QAction("&Set as index", self.horizontalHeader(),
                                statusTip="Set this column as the index",
                                triggered=self.set_dataset_index)

        action_delete_column = QtGui.QAction("&Delete Column", self.horizontalHeader(),
                                statusTip="Remove the column from the dataset",
                                triggered=self.remove_column)

        action_class_label = QtGui.QAction("&Use as class label", self.horizontalHeader(),
                                statusTip="Use this column as a class label",
                                triggered=self.set_class_label)

        menu.addAction(action_set_index)
        menu.addAction(action_delete_column)
        menu.addAction(action_class_label)
        menu.exec_(parentPosition)

    def set_dataset_index(self, event):
        df = self._parent.get_dataset()
        df.reset_index(level=0, inplace=True)
        df.set_index(df.columns[self._current_index+1], inplace=True)
        self._parent.update_dataset(df)
        self.resize_view()

    def remove_column(self, event):
        df = self._parent.get_dataset()
        df.drop(df.columns[self._current_index],
                inplace=True, axis=1, errors='ignore')
        self._parent.update_dataset(df)
        self.resize_view()

    def set_class_label(self, event):
        df = self._parent.get_dataset()
        labels = df[df.columns[self._current_index]]
        self._parent.figure.get_figure_canvas().set_class_label(labels)

    def resize_view(self):
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

import scipy.spatial as spatial


class MplCanvasListener(object):
    def __init__(self, canvas, parent):
        self._parent = parent
        canvas.mpl_connect('button_press_event', self.select_rows)
        self._parent.projectionTable.modelReset.connect(self.reset_tree)
        self.reset_tree()

    def reset_tree(self):
        df = self._parent.get_projection()
        if df is not None:
            self.tree = spatial.cKDTree(df[[0, 1]])

    def find_nearest(self, x, y):
        dist, idx = self.tree.query((x, y), k=1, p=1)
        return idx

    def select_rows(self, event):
        df = self._parent.get_projection()
        if df is not None:
            idx = self.find_nearest(event.xdata, event.ydata)
            self._parent.select_rows(idx)

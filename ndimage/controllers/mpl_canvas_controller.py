import numpy as np
import scipy.spatial as spatial
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path


class MplCanvasListener(object):
    def __init__(self, canvas, parent):
        self._parent = parent
        self._canvas = canvas
        self._canvas.mpl_connect('button_press_event', self.select_rows)
        self._lasso = LassoSelector(self._parent.figure.figure.axes, onselect=self.onselect)
        self._parent.projectionTable.modelReset.connect(self.reset_tree)
        self.reset_tree()

    def onselect(self, verts):
        path = Path(verts)
        df = self._parent.get_projection()
        if df is not None:
            idx = np.nonzero([path.contains_point(xy) for xy in df.as_matrix()])[0]
            print idx
            self._parent.select_rows(idx)
            self._canvas.draw_idle()

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

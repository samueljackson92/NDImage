import numpy as np
import scipy.spatial as spatial
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path


class MplCanvasLassoSelector(object):

    def __init__(self, canvas, parent):
        self._parent = parent
        self._canvas = canvas
        self._lasso = LassoSelector(self._parent.figure.get_axes(),
                                    onselect=self.onselect)
        # Figure MUST be redrawn at this point
        self._parent.figure.figure.draw()

    def onselect(self, verts):
        df = self._parent.get_projection()
        if df is not None:
            xys = df.as_matrix()
            path = Path(verts)
            idx = np.nonzero([path.contains_point(xy) for xy in xys])[0]
            self._parent.select_rows(idx)
            self._lasso.disconnect_events()
            self._parent.figure.figure.draw_idle()


class MplCanvasListener(object):
    def __init__(self, canvas, parent):
        self._parent = parent
        self._canvas = canvas
        self._canvas.mpl_connect('button_press_event', self.select_rows)
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

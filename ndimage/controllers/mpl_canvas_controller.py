import numpy as np
import scipy.spatial as spatial
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path


class MplCanvasLassoSelector(object):

    def __init__(self, fig_canvas, parent):
        self._parent = parent
        self._canvas = fig_canvas
        self._lasso = LassoSelector(self._canvas.axes,
                                    onselect=self.onselect)
        # Figure MUST be redrawn at this point
        self._canvas.draw()

    def onselect(self, verts):
        df = self._parent.get_projection()
        if df is not None:
            xys = df.as_matrix()
            path = Path(verts)
            idx = np.nonzero([path.contains_point(xy) for xy in xys])[0]
            self._parent.select_rows(idx)
            self._canvas.highlight_points(idx)
            self._lasso.disconnect_events()
            self._canvas.draw_idle()


class MplCanvasListener(object):
    def __init__(self, fig_canvas, parent):
        self._parent = parent
        self._canvas = fig_canvas
        self._canvas.figure.canvas.mpl_connect('button_press_event', self.select_rows)
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
            self._canvas.highlight_points(idx)
            self._canvas.draw_idle()

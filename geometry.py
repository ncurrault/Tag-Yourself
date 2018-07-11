from __future__ import unicode_literals
import matplotlib.pyplot as plt

class DimensionMismatchException(Exception):
    pass

class Point(object):
    def __init__(self, label, data=None, dim=0):
        self.label = label
        self.dim = dim
        if data is None:
            self.data = [ 0 ] * dim
        else:
            if len(data) == dim:
                self.data = data
            else:
                raise DimensionMismatchException()

    def __str__(self):
        return "{}({})".format(self.label, ", ".join([ str(e) for e in self.data ]) )

    def set_dim(self, new_dim):
        if self.dim == new_dim:
            return
        elif self.dim > new_dim:
            self.data = self.data[:new_dim]
        else:
            while len(self.data) < new_dim:
                self.data.append(0)

        self.dim = new_dim
        assert len(self.data) == self.dim

    def set_data_arr(self, arr):
        if len(arr) == self.dim:
            self.data = arr
        else:
            raise DimensionMismatchException()

    def set_data(self, i, val):
        self.data[i] = val
    def get_data(self, i):
        return self.data[i]

class Plot(object):
    X_BOUNDS = [ -1.2, 1.2 ]
    Y_BOUNDS = X_BOUNDS # square

    def __init__(self, _title):
        self.title = _title

        self.dim = 0
        self.axes = []
        self.points = []

        self.image_dirty = True # image must be generated
    def __str__(self):
        ret = self.title
        ret += "\n"
        ret += "=" * len(self.title)
        ret += "\n"

        ret += ", ".join(self.axes)

        ret += "\n"
        ret += "=" * len(self.title)
        ret += "\n"
        for p in self.points:
            ret += str(p)
            ret += "\n"

        return ret

    def add_axis(self, axis_name):
        self.dim += 1
        for p in self.points:
            p.set_dim(self.dim)
        self.axes.append(axis_name)
        self.image_dirty = True # image is no longer accurate

        assert len(self.axes) == self.dim

    def get_axes(self):
        return self.axes[:] # Pythonic copy

    def add_point(self, p):
        if self.dim == p.dim:
            self.points.append(p)
            self.image_dirty = True # image is no longer accurate
        else:
            raise DimensionMismatchException()

    def generate_image(self):
        if not self.image_dirty:
            return # no new work necessary

        if self.dim != 2:
            return "Only two-dimensional graphs are supported"
            # TODO support 1 and 3 dimensions

        plt.clf() # clears matplotlib canvas
        fig = plt.figure()

        # formatting
        plt.rc('xtick',labelsize = 13)
        plt.rc('ytick',labelsize = 13)
        plt.rc('axes', linewidth = 2)

        # set bounds and draw axes
        axes = plt.gca()
        axes.set_xlim(Plot.X_BOUNDS)
        axes.set_ylim(Plot.Y_BOUNDS)
        plt.plot(Plot.X_BOUNDS, [0, 0], 'k', linewidth=1) # x-axis
        plt.plot([0, 0], Plot.Y_BOUNDS, 'k', linewidth=1) # y-axis

        # text
        plt.title(self.title, fontsize=24)
        plt.xlabel(self.get_axes()[0], fontsize = 18)
        plt.ylabel(self.get_axes()[1], fontsize = 18)

        # points
        xvals = [ pt.get_data(0) for pt in self.points ]
        yvals = [ pt.get_data(1) for pt in self.points ]
        labels = [ pt.label for pt in self.points ]
        plt.scatter(xvals, yvals)

        LABEL_OFFSET_X = 0.02
        LABEL_OFFSET_Y = LABEL_OFFSET_X
        for i in range(len(self.points)):
            plt.annotate(labels[i], (xvals[i] + LABEL_OFFSET_X, yvals[i] + LABEL_OFFSET_Y) )

        fig.savefig("ignore/images/{}.png".format(self.title))
        plt.close(fig)
        self.image_dirty = False

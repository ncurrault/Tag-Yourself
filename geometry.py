import matplotlib.pyplot as plt


class DimensionMismatchException(Exception):
    pass

class Point(object):
    def __init__(self, _label, _dim=0):
        self.label = _label
        self.dim = _dim
        self.data = [ 0 ] * _dim

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
    def __init__(self, _title):
        self.title = _title

        self.dim = 0
        self.axes = []
        self.points = []

    def add_axis(self, axis_name):
        self.dim += 1
        for p in self.points:
            p.set_dim(self.dim)
        self.axes.append(axis_name)

        assert len(self.axes) == self.dim

    def get_axes(self):
        return self.axes[:] # Pythonic copy

    def add_point(self, p):
        if self.dim == p.dim:
            self.points.append(p)
        else:
            raise DimensionMismatchException()

    def generate_image(self):
        pass
        # TODO: the hard part

# /lookatthisgraph _name_
# Display a graph
# *Example message*:
# ```
# /lookatthisgraph Healing
# ```
#
# /tag _name_ _coordinates_ [ _point label_ ]
# Add a point to a graph. Use caller's Telegram name initials if no provided label.
# All axes in all graphs are on the scale \[-1, 1]
#
# *Example message*:
# ```
# /tag Healing (-1, -1) bad
# /tag Healing (1, 1) good
# ```

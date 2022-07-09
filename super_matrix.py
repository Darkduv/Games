"""Defines special matrix and lists to use in games"""
from random import randint


class SuperMatrix(list):
    """Matrix inheriting from list"""

    def __init__(self, number=0, n_lig=12, n_col=12, fill=True):
        list.__init__([])
        if fill:
            for _ in range(n_lig):
                self.append([number] * n_col)

    def copy(self):
        other = SuperMatrix(fill=False)
        for i in range(len(self)):
            other.append(self[i].copy())
        return other

    def __str__(self):
        string = ""
        for i in self:
            string += str(i)
            string += "\n"
        return string


class SuperList(list):
    """Regular list with a twist:

    can append a value if we try to set a non-existant index"""

    def __setitem__(self, index, value):
        try:
            assert isinstance(index, int)
            list.__setitem__(self, index, value)
        except IndexError:
            self.append(value)


class ListWeight(list):

    """List of each position available with its weight :
    the list is in the form of [[position, weight],...]"""

    def _position_weight_min_max(self, keep_first):
        """Returns randomly a position with the highest (or lowest) weight.

        Returns [] if list of positions empty.
        keep_first(a, b) returns True if we want to keep the first value """
        if not self:  # list empty
            return []
        extreme = self[0][1]
        l_extreme = [0]
        for [pos, weight] in self:
            if keep_first(weight, extreme):
                extreme = weight
                l_extreme = [[pos, weight]]
            elif weight == l_extreme:
                l_extreme.append([pos, weight])
        length = len(l_extreme)
        pos_weight = l_extreme[randint(0, length-1)]
        return pos_weight

    def position_weight_max(self):
        """Returns randomly a position with the highest weight.

        Returns [] if list of positions empty."""
        def keep_first(weight, maxi):
            return weight > maxi
        return self._position_weight_min_max(keep_first)

    def position_weight_min(self):
        """Returns randomly a position with the highest weight.

        Returns [] if list of positions empty."""
        def keep_first(weight, maxi):
            return weight < maxi
        return self._position_weight_min_max(keep_first)

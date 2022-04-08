from random import randint


class SuperMatrix(list):
    def __init__(self, number=0, n_lig=12, n_col=12, fill=True):
        list.__init__([])
        if fill:
            for i in range(n_lig):
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

    def __setitem__(self, key, value):
        try:
            assert isinstance(key, int)
            list.__setitem__(self, key, value)
        except IndexError:
            self.append(value)


class ListWeight(list):

    """List of each position available with its weight : the list is in the form of [[position, weight],...]"""

    def position_weight_max(self):
        if self:  # list not empty
            maxi = self[0][1]
            l_max = [0]
            for i in range(len(self)):
                if self[i][1] > maxi:
                    maxi = self[i][1]
                    l_max = [i]
                elif self[i][1] == maxi:
                    l_max.append(i)
            l = len(l_max)
            i_max = l_max[randint(0, l-1)]
            return self[i_max]
        else:
            return []

    def position_weight_min(self):
        if self:  # list not empty
            mini = self[0][1]
            l_min = [0]
            for i in range(len(self)):
                if self[i][1] < mini:
                    mini = self[i][1]
                    l_min = [i]
                elif self[i][1] == mini:
                    l_min.append(i)
            l = len(l_min)
            i_min = l_min[randint(0, l-1)]
            return self[i_min]
        else:
            return []

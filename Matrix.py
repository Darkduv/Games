__author__ = 'maximin'


class Matrix(list):
    """    def __new__(cls, nb_lig, nb_col=None, nb = 0 ):
        if isinstance(nb_lig, list):
            if not nb_lig:
                return Matrix.__init__(list.__)"""

    def __init__(self, nb_lig=0, nb_col=0, nb=0, list_=None):
        # print("cou_cou", list_)
        list.__init__([])
        if list_ is None:
            # print("it doesn't work")
            if nb_lig is [] or nb_lig == 0:
                self.append([])
            elif type(nb_col) != int or nb_col < 0:
                raise TypeError("nb_col must be positive !!!")
            elif type(nb_lig) == int:
                if nb_lig < 0:
                    raise TypeError("nb_lig must be positive")
                for i in range(nb_lig):
                    self.append([nb] * nb_col)
        else:
            # print(type(list_))
            # print(list_)
            if isinstance(list_, list):
                # print("it work's")
                if isinstance(list_[0], list):
                    for i in list_:
                        self.append(i.copy())
                else:
                    self.append(list_.copy())
            else:
                raise TypeError("list_ must be a list")
        self.raise_error_if_not_true_matrix()

    def __str__(self):
        if not self:
            return "[]\n"
        string = "["
        for i in self:
            string += (str(i) + "\n")
        return string[:-1] + "]\n"

    def __repr__(self):
        string = self.__str__()
        return "< {} >".format(string[:-1])

    def __add__(self, other):
        self.raise_error_if_not_true_matrix()
        if not isinstance(other, Matrix):
            raise TypeError("Other's not a Matrix")
        other.raise_error_if_not_true_matrix()
        l = []
        for i in zip(self, other):
            l_bis = []
            for j in zip(i[0], i[1]):
                l_bis.append(j[0] + j[1])
            l.append(l_bis)
        return l

    def __mul__(self, other):
        self.raise_error_if_not_true_matrix()
        if type(other) in [int, float]:
            p = Matrix(len(self), len(self[0]))
            if other == 0:
                return p
            for i in range(len(self)):
                for j in range(len(self[0])):
                    p[i][j] = self[i][j] * other
            return p
        elif isinstance(other, Matrix):
            other.raise_error_if_not_true_matrix()
            if len(other) != len(self[0]):
                raise TypeError("can't multiply Matrix n-p and q-r if p != r")
            else:
                n = len(self)
                p = len(other)
                r = len(other[0])
                mul = Matrix(n, r)
                for i in range(n):
                    for j in range(r):
                        s = 0
                        for k in range(p):
                            s += self[i][k] * self[k][j]
                        mul[i][j] = s
                return mul
        else:
            raise TypeError("other type must be 'int', 'float', or 'Matrix'")

    def __sub__(self, other):
        self.raise_error_if_not_true_matrix()
        if not isinstance(other, Matrix):
            raise TypeError("Not a Matrix")
        other.raise_error_if_not_true_matrix()
        return self + other * -1

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if not type(other) in [int, float]:
            raise TypeError("can'n multiply Matrix by an object not int and not float")
        return self * (1 / other)

    def true_matrix(self):
        try:
            # print(self)
            l = len(self[0])
        except IndexError:
            # print("zut")
            return False
        except TypeError:
            # print("mince")
            return False
        for i in self:
            # print("good bye")
            if l != len(i):
                return False
        return True

    def raise_error_if_not_true_matrix(self):
        if not self.true_matrix():
            raise TypeError("Not a Real Matrix ........\n")

    def transposition(self):
        trace = Matrix()
        for i in range(len(self)):
            l = [j[i] for j in self]
            trace.append(l)
        return trace

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Not a matrix")
        else:
            for i in zip(self, other):
                for j in i:
                    if j != i:
                        return False
            return True


class SquareMatrix(Matrix):
    def __init__(self, nb_lig, nb=0):
        Matrix.__init__(self, nb_lig, nb_lig, nb)

    def true_matrix(self):
        try:
            l = len(self)
        except TypeError:
            return False
        for i in self:
            if l != len(i):
                return False
        return True

    def raise_error_if_not_true_matrix(self):
        if not self.true_matrix():
            raise TypeError("Not a real Square Matrix........")

    def __pow__(self, power):
        self.raise_error_if_not_true_matrix()
        if not type(power) == int or power < 0:
            raise TypeError("Power must be a positive int")
        prod = IdentityMatrix(len(self), 1)
        for i in range(power):
            prod *= self
        return prod


class IdentityMatrix(SquareMatrix):
    def __init__(self, nb_lig, nb=1):
        SquareMatrix.__init__(self, nb_lig)
        for i in range(nb_lig):
            self[i][i] = nb

    def __mul__(self, other):
        if type(other) in [int, float]:
            return IdentityMatrix(len(self), other)
        elif isinstance(other, Matrix):
            other.raise_error_if_not_true_matrix()
            if len(self[0]) != len(other):
                raise TypeError("Dimensions")
            else:
                c = self[0][0]
                if c == 1:
                    return other
                else:
                    return self[0][0] * other

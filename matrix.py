"""Custom matrix test.

Doesn't use numpy arrays (why ?) but inherits from list (quite badly)
Keeping this module only for archives and curiosity purposes.
Violates (among other things) the liskov rule.
"""

from __future__ import annotations
from numbers import Number

__author__ = 'maximin'


class NotMatrixError(Exception):
    """Custom error using an object like a matrix if it's not"""


class NotSquareMatrixError(Exception):
    """Custom error when a matrix is not square."""


class MismatchDimensionError(ValueError):
    """Custom error for dimensions mismatch between matrix """


class Matrix(list):
    """Custom matrix class inheriting from list."""

    def __init__(self, nb_row: int = 1, nb_col: int = 1,
                 fill_val=0, list_: list = None):
        super().__init__()
        if list_ is None:
            if nb_row == 1:
                self.append([])
            elif not isinstance(nb_col, int) or nb_col <= 0:
                raise ValueError("nb_col must an int and be positive!!!")
            elif not isinstance(nb_row, int) or nb_row <= 0:
                raise ValueError("nb_row must an int and be positive")
            for i in range(nb_row):
                self.append([fill_val] * nb_col)
        else:
            if not isinstance(list_, list):
                raise TypeError("list_ must be a list")
            if isinstance(list_[0], list):
                for i in list_:
                    self.append(i.copy())
            else:
                self.append(list_.copy())

        self.raise_error_if_not_true_matrix()

    @property
    def nb_rows(self) -> int:
        return len(self)

    @property
    def nb_cols(self) -> int:
        return len(self[0])

    def __str__(self):
        string = "\n".join(str(i) for i in self)
        return f"[{string[:-1]}]"

    def __repr__(self):
        string = self.__str__()
        return f"< {string} >"

    def __add__(self, other) -> Matrix:
        if not isinstance(other, Matrix):
            raise TypeError("Other's not a Matrix")
        ll = []
        for i1, i2 in zip(self, other):
            l_bis = []
            for j1, j2 in zip(i1, i2):
                l_bis.append(j1 + j2)
            ll.append(l_bis)
        return Matrix(list_=ll)

    def __mul__(self, other: Number | Matrix) -> Matrix:
        if isinstance(other, Number):
            prod = Matrix(self.nb_rows, self.nb_cols)
            if other == 0:
                return prod
            for i in range(len(self)):
                for j in range(len(self[0])):
                    prod[i][j] = self[i][j] * other
            return prod
        elif not isinstance(other, Matrix):
            raise TypeError("other type must be 'int', 'float', or 'Matrix'")
        if len(other) != len(self[0]):
            raise MismatchDimensionError(
                "can't multiply Matrix of sizes n-p and q-r if p != r")
        n = self.nb_rows
        p = other.nb_rows
        r = other.nb_cols
        mul = Matrix(n, r)
        for i in range(n):
            for j in range(r):
                s = sum(self[i][k] * self[k][j] for k in range(p))
                mul[i][j] = s
        return mul

    def __sub__(self, other: Matrix):
        if not isinstance(other, Matrix):
            raise NotMatrixError("`other` is not a matrix")
        return self + other * -1

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if not type(other) in [int, float]:
            raise ValueError("can't divide Matrix by an object"
                             " not int and not float")
        return self * (1 / other)

    def true_matrix(self):
        try:
            length = len(self[0])
        except IndexError:  # empty matrix
            return False
        for row in self:
            if length != len(row):
                return False
        return True

    def raise_error_if_not_true_matrix(self):
        if not self.true_matrix():
            raise NotMatrixError(
                "A matrix should have all rows of the same size")

    def transposition(self):
        trace = Matrix()
        for i in range(len(self)):
            ll = [j[i] for j in self]
            trace.append(ll)
        return trace

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            raise NotMatrixError("`other` is not a matrix")
        for i1, i2 in zip(self, other):
            if i1 != i2:
                return False
        return True


class SquareMatrix(Matrix):
    """Child of Matrix, make a square matrix (change init and check)"""
    def __init__(self, nb_row, fill_val=0):
        super().__init__(nb_row, nb_row, fill_val)

    def true_matrix(self):
        length = len(self)
        for i in self:
            if length != len(i):
                return False
        return True

    def raise_error_if_not_true_matrix(self):
        if not self.true_matrix():
            raise NotSquareMatrixError()

    def __pow__(self, power):
        if not isinstance(power, int) or power < 0:
            raise ValueError("Power must be a positive int")
        prod = IdentityMatrix(len(self))
        for _ in range(power):
            prod *= self
        return prod


class IdentityMatrix(SquareMatrix):
    """IdentityMatrix. Gives a quicker multiplication"""
    def __init__(self, nb_row):
        super().__init__(nb_row)
        for i in range(nb_row):
            self[i][i] = 1

    def __mul__(self, other):
        if type(other) in [int, float]:
            return super().__mul__(other)
        if not isinstance(other, Matrix):
            raise NotMatrixError()
        if len(self[0]) != len(other):
            raise MismatchDimensionError()
        return other.copy()

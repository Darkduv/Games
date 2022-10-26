"""
###########################################
#                                         #
#             Game of 2048                #
#                                         #
#                                         #
#                                         #
#                                         #
#  Version of 10/07/2022 - License : GPL  #
###########################################
"""

from __future__ import annotations
from enum import Enum
from random import randint
import tkinter
from typing import Tuple

import numpy as np

from game_tools import gui


class InvalidError(Exception):
    """Custom error raised if something invalid is done"""


class Move(Enum):
    """List of the possible directions for a move"""
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"

    @classmethod
    def map_values(cls) -> dict[str, Move]:
        """Returns a dict of the form {value: move}"""
        return {move.value: move for move in cls}

    @classmethod
    def val_to_move(cls, val: str) -> Move:
        return cls.map_values()[val]


class Grid:
    """Class with the numeric grid"""

    def __init__(self):
        self.matrix = np.zeros((4, 4), dtype=int)
        self.power = np.array([[0] * 4] * 4)
        self.zeros = np.argwhere(self.matrix == np.zeros((4, 4), dtype=int))
        self.nb_zeros = np.size(self.zeros, 0)
        self.add_number()
        self.add_number()

    def refresh(self) -> None:
        """Refreshes the following attributes : .zeros and .nb_zeros
        """
        self.zeros = np.argwhere(self.matrix == np.zeros((4, 4), dtype=int))
        self.nb_zeros = np.size(self.zeros, 0)

    @staticmethod
    def number_random(prop: int = 10) -> int:
        """Returns randomly 2 or 4 with a probability of one 4 for `prop` 2
        """
        is_four = randint(0, prop) == 0
        return 4 if is_four else 2

    def add_number(self) -> None:
        """
        add 2 or 4, at random, to the numeric grid
        """
        self.refresh()
        if self.nb_zeros == 0:
            raise InvalidError("Can't add a number : grid already filled")
        n = randint(0, self.nb_zeros - 1)
        [i, j] = self.zeros[n]
        nb = self.number_random()
        self.matrix[i][j] = nb
        self.power[i][j] = nb // 2  # if 4: power=2, ok. if 2: power = 1, ok.

    def turn_grid(self, direction: Move):
        """Turn the grid according to direction.

        With this method, only one move ( right to left ) needs to be coded
        """
        if direction == Move.RIGHT:
            self.matrix = np.rot90(self.matrix, 2)
            self.power = np.rot90(self.power, 2)

        elif direction == Move.UP:
            self.matrix = self.matrix.T
            self.power = self.power.T

        elif direction == Move.DOWN:
            self.matrix = np.rot90(self.matrix, 2)
            self.matrix = self.matrix.T
            self.power = np.rot90(self.power, 2)
            self.power = self.power.T

    def shifts_left(self):
        """Before move in itself : transform [2,3,0,4] in [2,3,4,0]

        (easier to manipulate for the move)"""
        for i in range(4):
            m = []
            power = []
            for j in range(4):
                if self.matrix[i, j] != 0:
                    m.append(self.matrix[i, j])
                    power.append(self.power[i, j])
            m += [0] * (4 - len(m))
            power += [0] * (4 - len(power))
            self.matrix[i] = np.array(m)
            self.power[i] = np.array(power)

    def move_to_the_left(self):
        """The move in itself"""
        for i in range(4):
            for j in range(3):
                if self.matrix[i, j] == self.matrix[i, j + 1]:
                    self.matrix[i, j] *= 2
                    if self.matrix[i, j] != 0:
                        self.power[i, j] += 1
                    for k in range(j + 1, 3):
                        self.matrix[i, k] = self.matrix[i, k + 1]
                        self.power[i, k] = self.power[i, k + 1]
                    self.matrix[i, 3] = 0
                    self.power[i, 3] = 0

    def equal(self, bis):
        """
        :param bis: a matrix
        :return: if matrix_bis = self.matrix
        """
        for i in range(4):
            for j in range(4):
                if self.matrix[i, j] != bis[i, j]:
                    return False
        return True

    def make_move(self, move: Move) -> None:
        """makes the move. it must be verified"""
        self.turn_grid(move)
        self.shifts_left()
        self.move_to_the_left()
        self.turn_grid(move)

    def find_moves(self) -> list[Move]:
        """Checks if moves are possible.

        Returns the list of possible moves.
        the list can be empty => the player has lost.
        """
        new_tab = Grid()
        new_tab.matrix = np.copy(self.matrix)
        moves = list(Move)
        moves_copy = moves.copy()

        for i in range(3, -1, -1):
            new_tab.matrix = np.copy(self.matrix)
            new_tab.make_move(moves_copy[i])

            if self.equal(new_tab.matrix):
                moves.pop(i)

        return moves

    def game_round(self, move: Move) -> bool:
        """One round. Returns True if lost game, else False"""
        possible_moves = self.find_moves()
        if not possible_moves:  # empty
            return True
        if move not in possible_moves:
            return False
        self.make_move(move)
        self.refresh()
        self.add_number()
        return False


class Panel(tkinter.Frame):
    """Game panel (game with graphic part)"""

    def __init__(self):
        super().__init__()
        self.matrix = Grid()
        self.n_row, self.n_col = 4, 4  # initial grid = 4 x 4

        # Canvas :
        self.can = tkinter.Canvas(self, bg="white", borderwidth=0,
                                  highlightthickness=1,
                                  highlightbackground="black")
        # self.can.bind("<Configure>", self.re_scale)
        self.can.pack()

        self.init_game()

    def init_game(self):
        """beginning of the Game"""
        # Link of the event <key of the keyboard>to his manager :
        self.matrix = Grid()
        self.can.focus_set()
        self.can.bind("<Key>", self.move)
        self.can.pack()

    # def re_scale(self, event):
    # """ for rescaling the grid """
    # width, height = event.width, event.height
    # self.draw_grid(width, height)

    def lost(self) -> None:
        square_size = self.square_side
        message = self.can.create_text(2 * square_size, 2 * square_size,
                                       text="", font="Helvetica 30 bold",
                                       fill='Black')
        for _ in range(5):
            self.can.itemconfig(message, text="You've lost!")
            self.can.update()
            self.can.after(500)
            self.can.itemconfig(message, text="")
            self.can.update()
            self.can.after(150)

    @property
    def square_side(self) -> int:
        #  maximum possible width and height for the squares :
        l_max = self.winfo_width() // self.n_col
        h_max = self.winfo_height() // self.n_row
        # the side of the square will be the smallest of these dimensions :
        return min(l_max, h_max)

    @property
    def shape(self) -> Tuple[int, int]:
        return self.square_side * self.n_col, self.square_side * self.n_row

    def draw_grid(self):
        """Layout of the grid, according to des options & dimensions"""
        # -> Configuration of the new canvas dimensions :
        width, height = self.shape
        self.can.configure(width=width, height=height)
        # Layout of the grid :
        self.can.delete(tkinter.ALL)  # Effacement older paints
        square_size = self.square_side
        s = square_size
        # horizontal lines and vertical ones because n_row = n_col
        for _ in range(self.n_row - 1):
            self.can.create_line(0, s, width, s, fill="black")
            self.can.create_line(s, 0, s, height, fill="black")
            s += square_size
        c = square_size
        for i in range(4):
            for j in range(4):
                power = self.matrix.power[i][j]
                self.can.create_rectangle(
                    j * c, i * c, (j+1) * c, (i + 1) * c, outline="grey",
                    width=1, fill=self.color(power))

                # self.can.create_rectangle(
                #     j * c, i * c, (j+1) * c, (i + 1) * c, outline="grey",
                #     width=0, fill=f"#{hex(255 - 15 * color)[2:]}fff")

        # Layout of all the numbers :
        for r in range(self.n_row):
            for c in range(self.n_col):
                x = int((c + 1 / 2) * square_size)
                y = int((r + 1 / 2) * square_size)
                # self.can.create_rectangle()
                self.can.create_text(x, y, text=str(self.matrix.matrix[r][c]),
                                     font="Helvetica 30 normal", fill="black")

    @staticmethod
    def color(power: int) -> str:
        """Returns a string '#RRGGBB' of color"""
        rr = hex(255 - 15 * power)[2:]
        gg = hex(255 - power * (36 - 2 * power))[2:]
        bb = hex(250 - power)[2:]
        col = f"#{rr}{gg}{bb}"
        return col

    def move(self, event):
        """Handles the event <Key> """
        if event.keysym in Move.map_values():
            lost = self.matrix.game_round(Move.val_to_move(event.keysym))
            self.draw_grid()
            if lost:
                self.lost()


class Game2048(tkinter.Tk):
    """Main body of the game"""

    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.title("Jeu de 2048")

        menu_config = [
            ("File", [('Restart', self.reset), ('Quit', self.destroy)]),
            ('Help', [('Principe du jeu', self.principle),
                      ('About...', self.about)])
        ]
        self.m_bar = gui.RecursiveMenuBar(self)
        self.m_bar.config_menu(menu_config)
        # self.m_bar.pack(side=tkinter.TOP, expand=tkinter.NO, fill=tkinter.X)

        self.game = Panel()
        self.game.pack(expand=tkinter.YES, fill=tkinter.BOTH, padx=8, pady=8)

        # self.pack()

    def reset(self):
        """with the menu, reset the game"""
        self.game.init_game()
        self.game.draw_grid()

    def principle(self):
        """window-message containing la description rapid du principe du jeu"""
        msg = tkinter.Toplevel(self)
        tkinter.Message(
            msg, bg="navy", fg="ivory", width=400,
            font="Helvetica 10 bold",
            text="This game in moving the numbers in the four directions "
                 "(left, right, up and down) and the adjacent (in the "
                 "axis of the direction are added if they are the same. "
                 "The initial grid contain two numbers 2 or 4 placed "
                 "by chance in the grid. At each move one 2 or one "
                 "appears in the grid. The purpose is to reach 2048 or "
                 "more. For giving the direction of the wanted move, "
                 "type the corresponding arrow on the keyboard. You lost "
                 "if you couldn't any lore do a move.") \
            .pack(padx=10, pady=10)

    def about(self):
        """window-message indicating author and type of the licence"""
        msg = tkinter.Toplevel(self)
        tkinter.Message(msg, width=200, aspect=100, justify=tkinter.CENTER,
                        text="2048 \n\n coded by Max. Duv. , July 2022.\n"
                        "Licence = GPL").pack(padx=10, pady=10)


if __name__ == '__main__':
    Game2048().mainloop()

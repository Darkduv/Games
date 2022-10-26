"""
###########################################
#  Game of othello/reversi                #
#  References: None                       #
#                                         #
#                                         #
#                                         #
#  Version du 12/03/2016                  #
#            - Licence: GPL               #
###########################################
"""

import tkinter
from typing import Tuple, TypeAlias
import numpy as np

from game_tools import gui

Position: TypeAlias = Tuple[int, int]


class InvalidPosition(ValueError):
    """Custom error when accessing a wrong (row, col) position."""


class Grid:
    """Grid ot othello/reversi."""

    all_directions = [[0, 1], [1, 1], [1, 0], [0, -1], [-1, -1],
                      [-1, 0], [-1, 1], [1, -1]]

    def __init__(self):
        self.n_row, self.n_col = 8, 8
        self.grid = np.zeros((self.n_row, self.n_col), dtype=int)

    def init(self) -> None:
        self.grid = np.zeros((self.n_row, self.n_col), dtype=int)

        self.grid[3, 3] = 2
        self.grid[4, 4] = 2
        self.grid[3, 4] = 1
        self.grid[4, 3] = 1

    def nb_disks(self) -> dict[int, int]:
        unique, counts = np.unique(self.grid, return_counts=True)

        return dict(zip(unique, counts))

    def __getitem__(self, item: Position):
        return self.grid[item]

    def __setitem__(self, key: Position, value: int):
        self.grid[key] = value

    def valid_position(self, row: int, col: int) -> bool:
        """Is [row, col] in the grid?"""
        return 0 <= row < self.n_row and 0 <= col < self.n_col

    def valid_move_row_col(self, row: int, col: int, player: int) -> bool:
        """Is [row, col] a valid move for `player`?

        Searches over the eight (or less) possible directions"""
        if self.grid[row, col] != 0:
            return False  # place must be empty to be valid
        for direction in self.all_directions:
            if self.move_direction(direction, row, col, player):
                return True
        return False

    def all_flips_move(self, row: int, col: int, player: int) -> list[Position]:
        """Returns the list of disks flipped due to move [row, col]"""
        all_flips = []
        for direction in self.all_directions:
            all_flips.extend(self.move_direction(direction, row, col, player))
        return all_flips

    def flips_list(self, list_position: list[Position], player: int) -> None:
        # Todo : flips from a list: player should not be needed
        for position in list_position:
            self[position] = player

    def verify(self, player: int) -> list[Tuple[int, int]]:
        list_ok = []
        for i in range(self.n_row):
            for j in range(self.n_col):
                if self.valid_move_row_col(i, j, player):
                    list_ok.append((i, j))
        return list_ok

    def move_direction(self, direction, row: int, col: int,
                       player: int) -> list[Position]:
        """Test a move of `player` from row,col, in the given `direction`.

        If `test == True` only tests the move. If False, makes it."""
        di, dj = direction
        i = row + di
        j = col + dj
        l_flip_pos = []
        while self.valid_position(i, j) and\
                self.grid[i, j] not in [player, 0]:
            l_flip_pos.append((i, j))
            i += di
            j += dj
        if not l_flip_pos \
                or not self.valid_position(i, j) \
                or self.grid[i, j] != player:
            return []
        return l_flip_pos


class Panel(tkinter.Frame):
    """Game panel: game with graphics"""

    _colors = {1: 'Black', 2: 'White'}
    _board_color = "dark olive green"

    def __init__(self):
        # The panel of game is constituted of a re-scaling grid
        # containing it-self a canvas. at each re-scaling of the
        # grid,we calculate the tallest size possible for the
        # cases (squared) of the grid, et the dimensions of the
        # canvas are adapted in consequence.
        super().__init__()
        self.n_row, self.n_col = 8, 8  # initial grid = 4 x 4
        # Link of the event <resize> with an adapted manager:
        self.bind("<Configure>", self.rescale)
        # Canvas:
        self.can = tkinter.Canvas(self, bg=self._board_color, borderwidth=0,
                                  highlightthickness=1,
                                  highlightbackground="white")
        # Link of the event <click of the mouse> with its manager:
        self.can.bind("<Button-1>", self.click)
        self.can.pack(side=tkinter.LEFT)
        self.can_bis = tkinter.Label(text="Black's turn",
                                     font="Helvetica 25 normal")
        self.can_bis.pack(side=tkinter.RIGHT, padx=20)
        self.grid = Grid()  # construction of a list of lists

        self.player = 1
        self.place_ok = []
        self.init_jeu()

    @classmethod
    def color_player(cls, player: int) -> str:
        return cls._colors[player]

    @classmethod
    def disk_color(cls, player: int) -> str:
        if player == 0:
            return cls._board_color
        return cls.color_player(player).lower()

    def plot_nb_pawn(self, msg="{player}'s turn."):
        nb1, nb2 = self.nb_disks_players()
        self.can_bis.configure(
            text=f"{msg.format(player=self.color_player(self.player)):15}\n\n"
                 f"{self.color_player(1)}: {nb1: 2}\n"
                 f"{self.color_player(2)}: {nb2: 2}")

    def init_jeu(self):
        """Initialisation of the list which remember the state of the game"""
        self.grid.init()
        self.player = 1
        self.plot_nb_pawn()

    def rescale(self, _: tkinter.Event):
        """Operations made at each rescaling"""
        self.trace_grille()

    @property
    def square_side(self) -> int:
        #  maximum possible width and height for the squares:
        l_max = self.winfo_width() // self.n_col
        h_max = self.winfo_height() // self.n_row
        # the side of the square will be the smallest of these dimensions:
        return min(l_max, h_max)

    @property
    def shape(self) -> Tuple[int, int]:
        return self.square_side * self.n_col, self.square_side * self.n_row

    def change_player(self):
        self.player %= 2
        self.player += 1

    def nb_disks_players(self) -> Tuple[int, int]:
        nb_disks = self.grid.nb_disks()
        return nb_disks.get(1, 0), nb_disks.get(2, 0)

    def trace_grille(self):
        """Layout of the grid, in function of dimensions and options"""
        # -> Configuration of the new canvas dimensions:
        width, height = self.shape
        self.can.configure(width=width, height=height)
        # Layout of the grid:
        self.can.delete(tkinter.ALL)  # erasing of the past Layouts
        square_size = self.square_side
        s = square_size
        for _ in range(self.n_row - 1):  # horizontal lines
            self.can.create_line(0, s, width, s, fill="white")
            s += square_size
        s = square_size
        for c in range(self.n_col - 1):  # vertical lines
            self.can.create_line(s, 0, s, height, fill="white")
            s += square_size
        # Layout of all the pawns,
        # white or black according to the state of the game:
        for r in range(self.n_row):
            for c in range(self.n_col):
                color = self.disk_color(self.grid[r, c])
                self.draw_disk(r, c, color)

    def draw_disk(self, row: int, col: int, color: str):
        square_size = self.square_side
        self.can.create_oval(col * square_size + 3,
                             row * square_size + 3,
                             (col + 1) * square_size - 3,
                             (row + 1) * square_size - 3,
                             outline="grey", width=1, fill=color)

    def make_flips(self, list_flips: list[Position], player: int) -> None:
        """Make the flips of the move [row, col]  of `player`.

        If `test == True` only tests the move. If False, makes it."""

        self.grid.flips_list(list_flips, player)
        color = self.disk_color(player)
        for i, j in list_flips:
            self.draw_disk(i, j, color)
            self.update()
            self.can.after(200)

    def position_click(self, event: tkinter.Event) -> Position:
        """Determines the row and the column of the grid where is the click:"""
        square_size = self.square_side
        return int(event.y / square_size), int(event.x / square_size)

    def click(self, event: tkinter.Event):
        """Management of the mouse click: return the pawns"""
        row, col = self.position_click(event)
        if not self.grid.valid_position(row, col):
            return  # invalid move
        list_ok = self.grid.verify(self.player)

        if not list_ok:  # empty list
            self.end()
            return

        if (row, col) not in list_ok:
            return

        self.grid[row, col] = self.player

        # animation :
        color = self.disk_color(self.player)
        self.draw_disk(row, col, color)
        self.update()
        self.can.after(200)
        l_flips = self.grid.all_flips_move(row, col, self.player)
        self.make_flips(l_flips, self.player)
        # end of the animation

        self.change_player()
        list_ok = self.grid.verify(self.player)
        if not list_ok:  # other player can not play
            self.change_player()
            list_ok = self.grid.verify(self.player)
            if not list_ok:  # no one can play after that
                self.end()
                return
        self.plot_nb_pawn()
        self.trace_grille()

    def end(self):
        nb1, nb2 = self.nb_disks_players()
        if nb1 == nb2:
            win_msg = "It's a tie!"
        else:
            winner = 1 if nb1 > nb2 else 2
            win_msg = f"{self.color_player(winner)} wins!"
        self.plot_nb_pawn(msg=win_msg)
        self.trace_grille()


class Othello(tkinter.Tk):
    """Main window and manager of othello game"""

    def __init__(self):
        super().__init__()
        self.geometry("890x673")
        self.title(" Jeu de Othello")

        menu_config = [
            ("File", [('Restart', self.reset), ('Quit', self.destroy)]),
            ('Help', [('Principe du jeu', self.principle),
                      ('About...', self.about)])
        ]

        self.m_bar = gui.RecursiveMenuBar(self)
        self.m_bar.config_menu(menu_config)

        self.jeu = Panel()
        self.jeu.pack(expand=tkinter.YES, fill=tkinter.BOTH, padx=8, pady=8)

    def reset(self):
        """  french!  """
        self.jeu.init_jeu()
        self.jeu.trace_grille()

    def principle(self):
        """window-message containing the small description
        of the principle of this game"""
        msg = tkinter.Toplevel(self)
        tkinter.Message(msg, bg="navy", fg="ivory", width=400,
                        font="Helvetica 10 bold",
                        text="To win, you must have the most pieces ('disks')."
                             "\nOn your turn, place a disk so that you surround"
                             " some of your opponent's disks between the disk"
                             " you have placed and other disks of your colour."
                        ).pack(padx=10, pady=10)

    def about(self):
        """window-message indicating the author and the type of licence"""
        msg = tkinter.Toplevel(self)
        tkinter.Message(msg, width=200, aspect=100, justify=tkinter.CENTER,
                        text="Game of Othello\n\n"
                        "Licence = GPL").pack(padx=10, pady=10)


if __name__ == '__main__':
    Othello().mainloop()

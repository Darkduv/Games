"""
#################################################################
#  Game of Ping                                                 #
#  References: See  game of Ping in                             #
#  https://www.inforef.be/swi/download/apprendre_python3_5.pdf  #
#                                                               #
# (C) Gerard Swinnen (Verviers, Belgium)                        #
# (C) Maximin Duvillard (France)                                #
#                                                               #
#  Version du 29/09/2002 de Swinnen - Licence : GPL             #
#  Version du 09/07/2022 de Maximin - Licence : GPL             #
#################################################################
"""

import numpy as np
import tkinter

from dataclasses import dataclass

from typing import Tuple, Callable, Optional, Union
Position = Tuple[int, int]
Color = str

class Board:
    """Board : implement the game itself (the data)"""

    def __init__(self, n_row: int = 4, n_col: int = 4):
        self.state = None
        self.n_row = n_row
        self.n_col = n_col

    @property
    def shape(self) -> Position:
        return self.n_row, self.n_col

    def init_state(self) -> None:
        """Initialisation of the array storing the state of the game"""
        self.state = np.zeros(self.shape, dtype=int)

    def play(self, row: int, col: int) -> bool:
        """Tries and play the flip around (row, col) position."""
        if not self.is_in_the_grid(row, col):
            return False
        self.flip_around(row, col)
        return True

    def flip_around(self, row: int, col: int) -> None:
        """Operates the click on (lig, col).

        Returns a bool of True if play successful, of False if play failed"""
        # we treat the 8 adjacent cases :
        neighbours = np.array([[-1, -1], [-1, 0], [-1, 1],
                               [0, -1], [0, 1],
                               [1, -1], [1, 0], [1, 1]], dtype=int)
        for dr, dc in neighbours:
            row_neighbour = row + dr
            col_neighbour = col + dc
            if not self.is_in_the_grid(row_neighbour, col_neighbour):
                continue
            self.flip(row_neighbour, col_neighbour)

    def flip(self, row: int, col: int) -> None:
        """Flips the pawn in (row, col)"""
        self.state[row, col] = not self.state[row, col]

    def is_in_the_grid(self, row: int, col: int) -> bool:
        """Checks if a position (row, col) is valide"""
        return 0 <= row < self.n_row and 0 <= col < self.n_col

    def reset(self) -> None:
        """Reset the board."""
        self.init_state()

    def __getitem__(self, pos: Position) -> int:
        return self.state[pos]

    def update_shape(self, n_row: int = None, n_col: int = None) -> None:
        update = False
        if n_row is not None and n_row != self.n_row:
            self.n_row = n_row
            update = True
        if n_col is not None and n_col != self.n_col:
            self.n_col = n_col
            update = True
        if update:
            self.init_state()


@dataclass
class MenuCommand:
    """Stores a command for a menu"""
    label: str
    command: Callable
    underline: int = 0


class DropdownMenu:
    """Drop-down menu button"""

    def __init__(self, text: str = 'menu',
                 commands: Optional[list[MenuCommand]] = None):
        if commands is None:
            commands = []
        self.text = text
        self.commands = commands

    def add_to_menu_bar(self, menu_bar) -> tkinter.Menubutton:
        menu_button = tkinter.Menubutton(menu_bar, text=self.text)
        menu = tkinter.Menu(menu_button)
        menu_button.configure(menu=menu)

        for command in self.commands:
            menu.add_command(**command.__dict__)
        return menu_button

    def add_command(self, command: Union[MenuCommand, list[MenuCommand]])\
            -> None:
        if isinstance(command, list):
            self.commands.extend(command)
        else:
            self.commands.append(command)


class MenuBar(tkinter.Frame):
    """Drop-down menu bar"""

    def __init__(self):
        tkinter.Frame.__init__(self, borderwidth=2, relief=tkinter.GROOVE)

    def add_menu(self, menu: DropdownMenu):
        menu_button = menu.add_to_menu_bar(self)
        self.pack_menu(menu_button)

    @staticmethod
    def pack_menu(menu_button, side=tkinter.LEFT, pad_x=5):
        menu_button.pack(side=side, padx=pad_x)


class Panel(tkinter.Frame):
    """Panel de jeu (grille de n x m cases)"""
    _colors = ["white", "black"]

    def __init__(self):
        # The panel of game is constituted of a re-scaling grid
        # containing it-self a canvas. at each re-scaling of the
        # grid, we calculate the tallest size possible for the
        # cases (squared) of the grid, et the dimensions of the
        # canvas are adapted in consequence.
        tkinter.Frame.__init__(self)
        self.n_row, self.n_col = 4, 4  # initial grid = 4 x 4
        # Link of the event <resize> with an adapted manager :
        self.bind("<Configure>", self.rescale)
        # Canvas :
        self.can = tkinter.Canvas(self,
                                  bg="dark olive green",
                                  borderwidth=0,
                                  highlightthickness=1,
                                  highlightbackground="white")
        # Link of the event <click of the mouse> with its manager :
        self.can.bind("<Button-1>", self.click)
        self.can.pack()
        self.board = Board(4, 4)
        # pseudo random values: the geometry is configured later
        self.width, self.height = 200, 200
        self.board.init_state()  # setup state

    def rescale(self, event: tkinter.Event) -> None:
        """Operations made at each rescaling"""
        # the properties which are linked to the event of reconfiguration
        # contain all the new sizes of the panel :
        self.width, self.height = event.width - 4, event.height - 4
        # The subtraction of 4 pixels is here to compensate the width
        # of the 'highlight bordure' rolling the canvas)
        self.draw_board()

    @property
    def side_size(self):
        # maximal width and height possibles for the cases :
        l_max = self.width / self.n_col
        h_max = self.height / self.n_row
        # the side of a case would be the smallest of the two dimensions :
        return min(l_max, h_max)

    def draw_board(self) -> None:
        """Layout of the grid, in function of dimensions and options"""
        # -> establishment of new dimensions for the canvas :
        side_size = self.side_size
        wide, high = side_size * self.n_col, side_size * self.n_row
        self.can.configure(width=wide, height=high)
        # Layout of the grid:
        self.can.delete(tkinter.ALL)  # erasing of the past Layouts
        s = side_size
        for _ in range(self.n_row - 1):  # horizontal lines
            self.can.create_line(0, s, wide, s, fill="white")
            s += side_size
        s = side_size
        for _ in range(self.n_col - 1):  # vertical lines
            self.can.create_line(s, 0, s, high, fill="white")
            s += side_size
        # Layout of all the pawns,
        # white or black according to the state of the game :
        for row in range(self.n_row):
            for col in range(self.n_col):
                x1 = col * side_size + 3  # size of pawns =
                x2 = (col + 1) * side_size - 3  # size of the case - 10
                y1 = row * side_size + 3  #
                y2 = (row + 1) * side_size - 3
                color = self.color(row, col)
                self.can.create_oval(x1, y1, x2, y2, outline="grey",
                                     width=1, fill=color)

    def click(self, event: tkinter.Event):
        """Management of the mouse click : return the pawns"""
        # We start to determinate the line and the columns :
        side = self.side_size
        row, col = int(event.y / side), int(event.x / side)
        self.board.play(row, col)
        self.draw_board()

    def color(self, row: int, col: int) -> Color:
        return self._colors[self.board[row, col]]


@dataclass
class ConfigGame:
    geometry: str
    title: str


class MainWindow:
    """Main window / Manager in a game"""

    def __init__(self):
        self.frame = tkinter.Frame()
        self.m_bar = MenuBar()

    def configure_window(self, config_game: ConfigGame):
        self.frame.master.geometry(config_game.geometry)
        self.frame.master.title(config_game.title)

    def configure_menu(self, menu_list: list[DropdownMenu]):
        for dropdown in menu_list:
            self.m_bar.add_menu(dropdown)
        self.m_bar.pack(side=tkinter.TOP, expand=tkinter.NO, fill=tkinter.X)

    def message(self, pad_x=10, pad_y=10, **kwargs):
        msg = tkinter.Toplevel(self.frame)
        message = tkinter.Message(msg, **kwargs)
        message.pack(padx=pad_x, pady=pad_y)

    def mainloop(self, **kwargs):
        self.frame.mainloop(**kwargs)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def quit(self):
        self.frame.quit()

    def toplevel(self) -> tkinter.Toplevel:
        return tkinter.Toplevel(self.frame)


class Ping:
    """Actual game of ping"""
    config = ConfigGame(geometry="800x600", title="Game of Ping")

    def __init__(self):

        self.main_window = MainWindow()
        self.main_window.configure_window(self.config)
        self.main_window.configure_menu(self.create_menus())

        # ########### Config grid ############### #
        self.game = Panel()
        self.game.pack(expand=tkinter.YES, fill=tkinter.BOTH, padx=8, pady=8)

        self.main_window.pack()

    def about(self):
        """window-message indicating the author and the type of licence"""
        self.main_window.message(
            width=200, aspect=100, justify=tkinter.CENTER,
            text="Jeu de Ping\n\n"
                 "(C) Maximin Duvillard, August 2022.\nLicence = GPL")

    def principle(self):
        """Describes how the game works"""
        self.main_window.message(
            bg="navy", fg="ivory", width=400, font="Helvetica 10 bold",
            text="The pieces in this game each have one white and one black"
                 " side. When you click on a piece, all 8 adjacent pieces turn"
                 " over.\nThe game consists of trying to turn them all over.\n"
                 "\nIf the exercise is very easy with a 2 x 2 grid, it becomes"
                 " more difficult with larger grids. It is even impossible with"
                 " some grids.\nIt's up to you to find out which ones!\n"
                 "                 Reference: 'Pour la Science' magazine")

    def quit_(self):
        self.main_window.quit()

    def create_menus(self) -> list[DropdownMenu]:
        """Creation of the menus"""
        # #### Menu <File> #####
        file_menu = DropdownMenu(text='File')
        l_commands = [
            MenuCommand(label='Options', command=self.options),
            MenuCommand(label='Restart', command=self.reset),
            MenuCommand(label='Quit', command=self.quit_)
        ]
        file_menu.add_command(l_commands)

        # #### Menu <Help> #####
        help_menu = DropdownMenu(text='Help')
        l_commands = [
            MenuCommand(label='How the game works', command=self.principle),
            MenuCommand(label='About', command=self.about)
        ]
        help_menu.add_command(l_commands)

        return [file_menu, help_menu]

    def options(self):
        """Choice of the number of lines and columns for the grid"""
        opt = self.main_window.toplevel()
        cur_l = tkinter.Scale(opt, length=200, label="Number of lines:",
                              orient=tkinter.HORIZONTAL, from_=1, to=12,
                              command=self.update_nb_rows)
        cur_l.set(self.game.n_row)  # initial position of the cursor
        cur_l.pack()
        cur_h = tkinter.Scale(opt, length=200, label="Number of columns:",
                              orient=tkinter.HORIZONTAL, from_=1, to=12,
                              command=self.update_nb_cols)
        cur_h.set(self.game.n_col)
        cur_h.pack()

    def update_nb_cols(self, nb_cols):
        """Updates the number of columns."""
        nb_cols = int(nb_cols)
        self.game.n_col = nb_cols
        self.game.board.update_shape(n_col=nb_cols)
        self.game.draw_board()

    def update_nb_rows(self, nb_rows):
        """Updates the number of rows."""
        nb_rows = int(nb_rows)
        self.game.n_row = nb_rows
        self.game.board.update_shape(n_row=nb_rows)
        self.game.draw_board()

    def reset(self):
        """  french!  """
        self.game.board.reset()
        self.game.draw_board()

    def mainloop(self, **kwargs):
        self.main_window.mainloop(**kwargs)


if __name__ == '__main__':
    Ping().mainloop()

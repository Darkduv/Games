"""
###########################################
#                                         #
#              Jeu de 2048                #
#                                         #
#                                         #
#                                         #
#                                         #
#  Version du 29/02/2016 - License : Non  #
###########################################
"""

from random import randint
import tkinter
import numpy as np


class Grid:
    """Class with the numeric grid

     and add_number, refresh, turn_tableau, mvt_gauche."""

    def __init__(self):
        """
        :return: only init the game
        """
        self.matrix = np.zeros((4, 4), dtype=int)
        self.power = np.array([[0] * 4] * 4)
        self.zeros = np.argwhere(self.matrix == np.zeros((4, 4), dtype=int))
        self.nb_zeros = np.size(self.zeros, 0)
        self.add_number()
        self.add_number()

    def refresh(self):
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

        if self.nb_zeros != 0:
            n = randint(0, self.nb_zeros - 1)
            [i, j] = self.zeros[n]
            nb = self.number_random()
            if nb == 2:
                self.matrix[i][j] = 2
                self.power[i][j] = 1
            else:
                self.matrix[i][j] = 4
                self.power[i][j] = 2
            self.refresh()

    def turn_tableau(self, orientation):
        """
        Turn the grid according to orientation.

        With this method, only one move ( right to left ) needs to be coded
        :param orientation:
        """
        if orientation == "Right":
            self.matrix = np.rot90(self.matrix, 2)
            self.power = np.rot90(self.power, 2)

        elif orientation == "Up":
            self.matrix = self.matrix.T
            self.power = self.power.T

        elif orientation == "Down":
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
        self.refresh()

    def mvt_gauche(self):
        """The move in itself"""
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    if self.matrix[i][j] != 0:
                        self.power[i][j] += 1
                    for k in range(j + 1, 3):
                        self.matrix[i][k] = self.matrix[i][k + 1]
                        self.power[i][k] = self.power[i][k + 1]
                    self.matrix[i][3] = 0
                    self.power[i][3] = 0
        self.refresh()

    def equal(self, bis):
        """
        :param bis: a matrix
        :return: if matrix_bis = self.matrix
        """
        for i in range(4):
            for j in range(4):
                if self.matrix[i][j] != bis[i][j]:
                    return False
        return True


class MenuBar(tkinter.Frame):
    """Barre de menus scrolling"""

    def __init__(self, boss=None):
        super().__init__(borderwidth=2, relief=tkinter.GROOVE)
        # #### Menu <File> #####
        file_menu = tkinter.Menubutton(self, text='File')
        file_menu.pack(side=tkinter.LEFT, padx=5)
        me1 = tkinter.Menu(file_menu)
        me1.add_command(label='Restart', underline=0,
                        command=boss.reset)
        me1.add_command(label='Quit', underline=0,
                        command=boss.quit)
        file_menu.configure(menu=me1)

        # #### Menu <Help> #####
        help_menu = tkinter.Menubutton(self, text='Help')
        help_menu.pack(side=tkinter.LEFT, padx=5)
        me1 = tkinter.Menu(help_menu)
        me1.add_command(label='Principe du jeu', underline=0,
                        command=boss.principe)
        me1.add_command(label='More ...', underline=0,
                        command=boss.by_the_way)
        help_menu.configure(menu=me1)


class Panel(tkinter.Frame):
    """Panel de jeu (grille de n x m cases)"""

    def __init__(self):
        super().__init__()
        self.verified = True  # will contain if displacements still possible
        "Initialisation de la list de l'état du jeu"
        self.directions_possibles = ["Right", "Down", "Up", "Left"]
        self.matrix = Grid()
        self.n_row, self.n_col = 4, 4  # initial grid = 4 x 4

        # Canvas :
        self.can = tkinter.Canvas(self, bg="white", borderwidth=0,
                                  highlightthickness=1,
                                  highlightbackground="black")
        # self.can.bind("<Configure>", self.re_scale)
        self.can.pack()

        # weigh et height maximal possible  for the squares :
        l_max = self.winfo_width() // self.n_col
        h_max = self.winfo_height() // self.n_row
        # the side of the square will be the smallest of these dimensions :
        self.cote = min(l_max, h_max)

        self.init_jeu()

    def init_jeu(self):
        """beginning of the Game"""
        # Link of the event <key of the keyboard>to his manager :
        self.matrix = Grid()
        self.can.focus_set()
        self.can.bind("<Key>", self.move)
        self.can.pack()

    def verify(self):
        """Checks if movements are possible.

        If yes, put the list of possible moves in self.directions_possibles
        otherwise put False in `self.verified` => the player has lost.
        """
        new_tab = Grid()
        new_tab.matrix = np.copy(self.matrix.matrix)
        self.verified = True
        self.directions_possibles = ["Right", "Down", "Up", "Left"]
        sens = self.directions_possibles

        for i in range(3, -1, -1):
            new_tab.matrix = np.copy(self.matrix.matrix)
            new_tab.turn_tableau(sens[i])
            new_tab.shifts_left()
            new_tab.mvt_gauche()
            new_tab.turn_tableau(sens[i])
            new_tab.refresh()

            if self.matrix.equal(new_tab.matrix):
                self.directions_possibles.pop(i)

        if len(self.directions_possibles) == 0:
            self.verified = False

    def game_round(self, orientation):
        """One round"""
        self.verify()
        if self.verified:
            if orientation in self.directions_possibles:
                self.matrix.turn_tableau(orientation)
                self.matrix.shifts_left()
                self.matrix.mvt_gauche()
                self.matrix.turn_tableau(orientation)
                self.matrix.refresh()
                self.matrix.add_number()
                self.directions_possibles = ["Right", "Down", "Up", "Left"]
            self.verify()
            if not self.verified:
                self.trace_grille()
                message = self.can.create_text(
                    2*self.cote, 2*self.cote, text="",
                    font="Helvetica 30 bold", fill='Black')
                for _ in range(5):
                    self.can.itemconfig(message, text="You've lost!!")
                    self.can.update()
                    self.can.after(500)
                    self.can.itemconfig(message, text="")
                    self.can.update()
                    self.can.after(150)

                self.can.itemconfig(message, text="You aren't very good!!!",
                                    fill="Red")
                self.can.update()
                self.can.after(1500)

        else:
            message = self.can.create_text(2*self.cote, 2*self.cote, text="",
                                           font="Helvetica 30 bold",
                                           fill='Black')
            for _ in range(5):
                self.can.itemconfig(message, text="You've lost!!")
                self.can.update()
                self.can.after(500)
                self.can.itemconfig(message, text="")
                self.can.update()
                self.can.after(150)

            self.can.itemconfig(message,
                                text="What a pity you are !!!", fill="Red")
            self.can.update()
            self.can.after(1500)

            # def re_scale(self, event):
            # """ for rescaling the grid """
            # width, height = event.width, event.height
            # self.trace_grille(width, height)

    def trace_grille(self):
        """Layout of the grid, according to des options & dimensions"""
        # -> establishment of news dimensions for the canvas :
        # weigh et height maximal possible  for the squares :
        l_max = self.winfo_width() // self.n_col
        h_max = self.winfo_height() // self.n_row
        # the side of the square will be the smallest of these dimensions :
        self.cote = min(l_max, h_max)
        (width, height) = (self.cote * self.n_col, self.cote * self.n_row)
        self.can.configure(width=width, height=height)
        # Layout of the grid :
        self.can.delete(tkinter.ALL)  # Effacement older paints
        s = self.cote
        # horizontal lines and vertical ones because n_row = n_col
        for _ in range(self.n_row - 1):
            self.can.create_line(0, s, width, s, fill="black")
            self.can.create_line(s, 0, s, height, fill="black")
            s += self.cote
        c = self.cote
        for i in range(4):
            for j in range(4):
                color = self.matrix.power[i][j]
                self.can.create_rectangle(
                    j * c, i * c, (j+1) * c, (i + 1) * c, outline="grey",
                    width=1, fill=f"#{hex(255 - 15 * color)[2:]}"
                                  f"{hex(255 - color * (36 - 2 * color))[2:]}"
                                  f"{hex(250 - color)[2:]}")

                # self.can.create_rectangle(
                #     j * c, i * c, (j+1) * c, (i + 1) * c, outline="grey",
                #     width=0, fill=f"#{hex(255 - 15 * color)[2:]}fff")

        # Layout of all the numbers :
        for r in range(self.n_row):
            for c in range(self.n_col):
                x = int((c + 1 / 2) * self.cote)
                y = int((r + 1 / 2) * self.cote)
                # self.can.create_rectangle()
                self.can.create_text(x, y, text=str(self.matrix.matrix[r][c]),
                                     font="Helvetica 30 normal", fill="black")

    def move(self, event):
        """Handles the event <Key> """
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            self.game_round(event.keysym)
            self.trace_grille()


class Game2048(tkinter.Frame):
    """Main body of the game"""

    def __init__(self):
        super().__init__()
        self.master.geometry("500x400")
        self.master.title("Jeu de 2048")

        self.m_bar = MenuBar(self)
        self.m_bar.pack(side=tkinter.TOP, expand=tkinter.NO, fill=tkinter.X)

        self.jeu = Panel()
        self.jeu.pack(expand=tkinter.YES, fill=tkinter.BOTH, padx=8, pady=8)

        self.pack()

    def reset(self):
        """with the menu, reset the game"""
        self.jeu.init_jeu()
        self.jeu.trace_grille()

    def principe(self):
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

    def by_the_way(self):
        """window-message indicating author and type of the licence"""
        msg = tkinter.Toplevel(self)
        tkinter.Message(msg, width=200, aspect=100, justify=tkinter.CENTER,
                        text="2048 \n\n coding by Max. Duv. , February 2016.\n"
                        "Licence = none").pack(padx=10, pady=10)


if __name__ == '__main__':
    Game2048().mainloop()

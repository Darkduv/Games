"""
###########################################
#  Game of othello/reversi                #
#  References : None                      #
#                                         #
#                                         #
#                                         #
#  Version du 12/03/2016                  #
#            - Licence : GPL              #
###########################################
"""

import tkinter


class MenuBar(tkinter.Frame):
    """bar of menu rolling"""

    def __init__(self, boss=None):
        super().__init__(borderwidth=2, relief=tkinter.GROOVE)
        # #### Menu <File> #####
        file_menu = tkinter.Menubutton(self, text='File')
        file_menu.pack(side=tkinter.LEFT, padx=5)
        me1 = tkinter.Menu(file_menu)
        me1.add_command(label='Options', underline=0,
                        command=boss.options)
        me1.add_command(label='Restart', underline=0,
                        command=boss.reset)
        me1.add_command(label='Quit', underline=0,
                        command=boss.quit)
        file_menu.configure(menu=me1)

        # #### Menu <Help> #####
        help_menu = tkinter.Menubutton(self, text='Help')
        help_menu.pack(side=tkinter.LEFT, padx=5)
        me1 = tkinter.Menu(help_menu)
        me1.add_command(label='Principle of the game', underline=0,
                        command=boss.principle)
        me1.add_command(label='By the way ...', underline=0,
                        command=boss.by_the_way)
        help_menu.configure(menu=me1)


class Panel(tkinter.Frame):
    """Panel de jeu (grille de n x m cases)"""

    def __init__(self):
        # The panel of game is constituted of a re-scaling grid
        # containing it-self a canvas. at each re-scaling of the
        # grid,we calculate the tallest size possible for the
        # cases (squared) of the grid, et the dimensions of the
        # canvas are adapted in consequence.
        super().__init__()
        self.n_row, self.n_col = 8, 8  # initial grid = 4 x 4
        # Link of the event <resize> with an adapted manager :
        self.bind("<Configure>", self.rescale)
        # Canvas :
        self.can = tkinter.Canvas(self, bg="dark olive green", borderwidth=0,
                                  highlightthickness=1,
                                  highlightbackground="white")
        # Link of the event <click of the mouse> with its manager :
        self.can.bind("<Button-1>", self.click)
        self.can.pack(side=tkinter.LEFT)
        self.can_bis = tkinter.Label(text="Black's turn",
                                     font="Helvetica 25 normal")
        self.can_bis.pack(side=tkinter.RIGHT)
        self.state = []  # construction of a list of lists
        self.width, self.height = 2, 2
        self.cote = 0
        self.player = 0
        self.place_ok = []
        self.nb_pawn_player = [2, 2]
        self.init_jeu()

    def init_jeu(self):
        """Initialisation of the list which remember the state of the game"""
        self.state = []
        self.player = 0
        for _ in range(12):  # equal to a panel
            self.state.append([2] * 12)  # of 12 lines x 12 columns

        self.state[self.n_row // 2 - 1][self.n_col // 2 - 1] = 0
        self.state[self.n_row // 2][self.n_col // 2] = 0
        self.state[self.n_row // 2 - 1][self.n_col // 2] = 1
        self.state[self.n_row // 2][self.n_col // 2 - 1] = 1
        self.nb_pawn_player = [2, 2]
        self.can_bis.configure(
            text=f"{['White', 'Black'][not self.player]}'s turn.\n\n"
                 f"White: {self.nb_pawn_player[0]}\n"
                 f"Black: {self.nb_pawn_player[1]}")

    def rescale(self, event):
        """Operations made at each rescaling"""
        # the properties which are linked to the event of reconfiguration
        # contain all the new sizes of the panel :
        self.width, self.height = event.width - 4, event.height - 4
        # The subtraction of 4 pixels allowed to compensate the width
        # of the `highlightbordure` rolling the canvas
        self.trace_grille()

    def trace_grille(self):
        """Layout of the grid, in function of dimensions and options"""
        # maximal width and height possibles for the cases :
        l_max = self.width / self.n_col
        h_max = self.height / self.n_row
        # the side of a case would be the smallest of the two dimensions :
        self.cote = min(l_max, h_max)
        # -> establishment of new dimensions for the canvas :
        wide, high = self.cote * self.n_col, self.cote * self.n_row
        self.can.configure(width=wide, height=high)
        # Layout of the grid:
        self.can.delete(tkinter.ALL)  # erasing of the past Layouts
        s = self.cote
        for _ in range(self.n_row - 1):  # horizontal lines
            self.can.create_line(0, s, wide, s, fill="white")
            s += self.cote
        s = self.cote
        for c in range(self.n_col - 1):  # vertical lines
            self.can.create_line(s, 0, s, high, fill="white")
            s += self.cote
        # Layout of all the pawns,
        # white or black according to the sate of the game :
        for r in range(self.n_row):
            for c in range(self.n_col):
                x1 = c * self.cote + 3  # size of pawns =
                x2 = (c + 1) * self.cote - 3  # size of the case -10
                y1 = r * self.cote + 3  #
                y2 = (r + 1) * self.cote - 3
                color = ["white", "black", "dark olive green"][self.state[r][c]]
                self.can.create_oval(x1, y1, x2, y2, outline="grey",
                                     width=1, fill=color)

    def roll(self, i, j):
        """ return True if the case 'touch' a non-empty case, False else """
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if 0 <= x < self.n_row and 0 <= y < self.n_col \
                        and self.state[x][y] != 2:
                    return True
        return False

    def verify(self):
        list_ok = []
        self.player += 1
        self.player %= 2
        for i in range(self.n_row):
            for j in range(self.n_col):
                if self.state[i][j] == 2 and self.roll(i, j):
                    for direction in [[0, 1], [1, 1], [1, 0], [0, -1],
                                      [-1, -1], [-1, 0], [-1, 1], [1, -1]]:
                        if self.movement_direction(direction, i, j):
                            list_ok.append([i, j])
        self.player += 1
        self.player %= 2
        self.place_ok = list_ok

    def movement_direction(self, direction, row, col, test=True):
        i = row + direction[0]
        j = col + direction[1]
        nb = 0
        while 0 <= i < self.n_row and 0 <= j < self.n_col and\
                self.state[i][j] is not self.player and 2 != self.state[i][j]:
            i += direction[0]
            j += direction[1]
            nb += 1
        if nb > 0 and i != self.n_row and j != self.n_col and \
                self.state[i][j] == self.player:
            if test:
                return True
            for k in range(1, nb + 1):
                self.state[row + k * direction[0]][
                    col + k * direction[1]] = self.player
                self.nb_pawn_player[self.player] += 1
                self.nb_pawn_player[not self.player] -= 1
                color = ["white", "black", "dark olive green"][self.player]
                self.can.create_oval((col + k * direction[1]) * self.cote + 3,
                                     (row + k * direction[0]) * self.cote + 3,
                                     (col + k*direction[1] + 1) * self.cote - 3,
                                     (row + k*direction[0] + 1) * self.cote - 3,
                                     outline="grey", width=1, fill=color)
                self.update()
                self.can.after(200)
        return False

    def click(self, event):
        """Management of the mouse click : return the pawns"""
        # We start to determinate the line and the columns :
        row, col = int(event.y / self.cote), int(event.x / self.cote)
        if not self.place_ok:
            self.verify()

        if not self.place_ok:
            self.player += 1
            self.player %= 2
            self.verify()

        if 0 <= row < self.n_row and 0 <= col < self.n_col and \
                [row, col] in self.place_ok:
            self.place_ok = []
            self.player += 1
            self.player %= 2
            self.state[row][col] = self.player
            self.nb_pawn_player[self.player] += 1
            color = ["white", "black", "dark olive green"][self.player]
            self.can.create_oval(col * self.cote + 3, row * self.cote + 3,
                                 (col + 1) * self.cote - 3,
                                 (row + 1) * self.cote - 3,
                                 outline="grey", width=1, fill=color)
            self.update()
            self.can.after(200)
            for direction in [[0, 1], [1, 1], [1, 0], [0, -1], [-1, -1],
                              [-1, 0], [-1, 1], [1, -1]]:
                self.movement_direction(direction, row, col, test=False)

            self.can_bis.configure(
                text=f"{['White', 'Black'][not self.player]}'s turn.\n\n"
                     f"White: {self.nb_pawn_player[0]}\n"
                     f"Black: {self.nb_pawn_player[1]}")
        self.trace_grille()


class Ping(tkinter.Frame):
    """corps principal du programme"""

    def __init__(self):
        super().__init__()
        self.master.geometry("890x673")
        self.master.title(" Jeu de Othello")

        self.m_bar = MenuBar(self)
        self.m_bar.pack(side=tkinter.TOP, expand=tkinter.NO, fill=tkinter.X)

        self.jeu = Panel()
        self.jeu.pack(expand=tkinter.YES, fill=tkinter.BOTH, padx=8, pady=8)

        self.pack()

    def options(self):
        """Choice of the number of lines and columns for the grid"""
        opt = tkinter.Toplevel(self)
        cur_l = tkinter.Scale(opt, length=200, label="Number of lines :",
                              orient=tkinter.HORIZONTAL,
                              from_=1, to=12, command=self.update_nb_rows)
        cur_l.set(self.jeu.n_row)  # initial position of the cursor
        cur_l.pack()
        cur_h = tkinter.Scale(opt, length=200, label="Number of columns :",
                              orient=tkinter.HORIZONTAL,
                              from_=1, to=12, command=self.update_nb_cols)
        cur_h.set(self.jeu.n_col)
        cur_h.pack()

    def update_nb_cols(self, n):
        """Updates the number of columns."""
        self.jeu.n_col = int(n)
        self.jeu.trace_grille()

    def update_nb_rows(self, n):
        """Updates the number of rows."""
        self.jeu.n_row = int(n)
        self.jeu.trace_grille()

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

    def by_the_way(self):
        """window-message indicating the author and the type of licence"""
        msg = tkinter.Toplevel(self)
        tkinter.Message(msg, width=200, aspect=100, justify=tkinter.CENTER,
                        text="Game of Othello\n\n"
                        "Licence = GPL").pack(padx=10, pady=10)


if __name__ == '__main__':
    Ping().mainloop()

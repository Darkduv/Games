from tkinter import *


###########################################
#  Jeu de othello                         #
#  References : None                      #
#                                         #
#         Final Version                   #
#            (C)                          #
#                                         #
#                                         #
#  Version du 12/03/2016 - Licence : ???  #
###########################################


class MenuBar(Frame):
    """bar of menu rolling"""

    def __init__(self, boss=None):
        Frame.__init__(self, borderwidth=2, relief=GROOVE)
        # #### Menu <File> #####
        file_menu = Menubutton(self, text='File')
        file_menu.pack(side=LEFT, padx=5)
        me1 = Menu(file_menu)
        me1.add_command(label='Options', underline=0,
                        command=boss.options)
        me1.add_command(label='Restart', underline=0,
                        command=boss.reset)
        me1.add_command(label='Quit', underline=0,
                        command=boss.quit)
        file_menu.configure(menu=me1)

        # #### Menu <Help> #####
        help_menu = Menubutton(self, text='Help')
        help_menu.pack(side=LEFT, padx=5)
        me1 = Menu(help_menu)
        me1.add_command(label='Principe of the game', underline=0,
                        command=boss.principe)
        me1.add_command(label='By the way ...', underline=0,
                        command=boss.by_the_way)
        help_menu.configure(menu=me1)


class Panel(Frame):
    """Panel de jeu (grille de n x m cases)"""

    def __init__(self):
        # The panel of game is constituted of a re-scaling grid
        # containing it-self a canvas. at each re-scaling of the
        # grid,we calculate the tallest size possible for the
        # cases (squared) of the grid, et the dimensions of the
        # canvas are adapted in consequence.
        Frame.__init__(self)
        self.n_lig, self.n_col = 8, 8  # initial grid = 4 x 4
        # Link of the event <resize> with an adapted manager :
        self.bind("<Configure>", self.rescale)
        # Canvas :
        self.can = Canvas(self, bg="dark olive green", borderwidth=0,
                          highlightthickness=1, highlightbackground="white")
        # Link of the event <click of the mouse> with its manager :
        self.can.bind("<Button-1>", self.click)
        self.can.pack(side=LEFT)
        self.can_bis = Label(text="Black's turn", font="Helvetica 25 normal")
        self.can_bis.pack(side=RIGHT)
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
        for i in range(12):  # (equal to a panel
            self.state.append([2] * 12)  # of 12 lines x 12 columns)

        self.state[self.n_lig // 2 - 1][self.n_col // 2 - 1] = 0
        self.state[self.n_lig // 2][self.n_col // 2] = 0
        self.state[self.n_lig // 2 - 1][self.n_col // 2] = 1
        self.state[self.n_lig // 2][self.n_col // 2 - 1] = 1
        self.nb_pawn_player = [2, 2]
        self.can_bis.configure(text=str(["White", "Black"][not self.player]) + "'s turn.\n \n" +
                               "White : " + str(self.nb_pawn_player[0]) + "\n" +
                               "Black : " + str(self.nb_pawn_player[1]))

    def rescale(self, event):
        """Operations made at each rescaling"""
        # the properties which are linked to the event of reconfiguration
        # contain all the new sizes of the panel :
        self.width, self.height = event.width - 4, event.height - 4
        # The subtract of 4 pixels allowed to compensate the width
        # of the 'highlightbordure" rolling the canvas)
        self.trace_grille()

    def trace_grille(self):
        """Layout of the grid, in function of dimensions and options"""
        # maximal width and height possibles for the cases :
        l_max = self.width / self.n_col
        h_max = self.height / self.n_lig
        # the side of a case would be the smallest of the two dimensions :
        self.cote = min(l_max, h_max)
        # -> establishment of new dimensions for the canvas :
        wide, high = self.cote * self.n_col, self.cote * self.n_lig
        self.can.configure(width=wide, height=high)
        # Layout of the grid:
        self.can.delete(ALL)  # erasing of the past Layouts
        s = self.cote
        for l in range(self.n_lig - 1):  # horizontal lines
            self.can.create_line(0, s, wide, s, fill="white")
            s += self.cote
        s = self.cote
        for c in range(self.n_col - 1):  # vertical lines
            self.can.create_line(s, 0, s, high, fill="white")
            s += self.cote
        # Layout of all the pawns, white or black according to the sate of the game :
        for l in range(self.n_lig):
            for c in range(self.n_col):
                x1 = c * self.cote + 3  # size of pawns =
                x2 = (c + 1) * self.cote - 3  # size of the case -10
                y1 = l * self.cote + 3  #
                y2 = (l + 1) * self.cote - 3
                color = ["white", "black", "dark olive green"][self.state[l][c]]
                self.can.create_oval(x1, y1, x2, y2, outline="grey",
                                     width=1, fill=color)

    def roll(self, i, j):
        """ return True if the case 'touch' a non-empty case, False else """
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if 0 <= x < self.n_lig and 0 <= y < self.n_col and self.state[x][y] != 2:
                    return True
        return False

    def verify(self):
        list_ok = []
        self.player += 1
        self.player %= 2
        for i in range(self.n_lig):
            for j in range(self.n_col):
                if self.state[i][j] == 2 and self.roll(i, j):
                    for direction in [[0, 1], [1, 1], [1, 0], [0, -1], [-1, -1], [-1, 0], [-1, 1], [1, -1]]:
                        if self.movement_direction(direction, i, j):
                            list_ok.append([i, j])
        self.player += 1
        self.player %= 2
        self.place_ok = list_ok

    def movement_direction(self, direction, lig, col, test=True):
        i = lig + direction[0]
        j = col + direction[1]
        nb = 0
        while 0 <= i < self.n_lig and 0 <= j < self.n_col and self.state[i][j] is not self.player and 2 != \
                self.state[i][j]:
            i += direction[0]
            j += direction[1]
            nb += 1
        if nb > 0 and i != self.n_lig and j != self.n_col and self.state[i][j] == self.player:
            if test:
                return True
            for k in range(1, nb + 1):
                self.state[lig + k * direction[0]][col + k * direction[1]] = self.player
                self.nb_pawn_player[self.player] += 1
                self.nb_pawn_player[not self.player] -= 1
                color = ["white", "black", "dark olive green"][self.player]
                self.can.create_oval((col + k * direction[1]) * self.cote + 3,
                                     (lig + k * direction[0]) * self.cote + 3,
                                     (col + k * direction[1] + 1) * self.cote - 3,
                                     (lig + k * direction[0] + 1) * self.cote - 3,
                                     outline="grey", width=1, fill=color)
                self.update()
                self.can.after(200)
        return False

    def click(self, event):
        """Management of the mouse click : return the pawns"""
        # We start to determinate the line and the columns :
        lig, col = int(event.y / self.cote), int(event.x / self.cote)
        if not self.place_ok:
            self.verify()

        if not self.place_ok:
            self.player += 1
            self.player %= 2
            self.verify()

        if 0 <= lig < self.n_lig and 0 <= col < self.n_col and [lig, col] in self.place_ok:
            self.place_ok = []
            self.player += 1
            self.player %= 2
            self.state[lig][col] = self.player
            self.nb_pawn_player[self.player] += 1
            color = ["white", "black", "dark olive green"][self.player]
            self.can.create_oval(col * self.cote + 3, lig * self.cote + 3,
                                 (col + 1) * self.cote - 3, (lig + 1) * self.cote - 3,
                                 outline="grey", width=1, fill=color)
            self.update()
            self.can.after(200)
            for direction in [[0, 1], [1, 1], [1, 0], [0, -1], [-1, -1], [-1, 0], [-1, 1], [1, -1]]:
                self.movement_direction(direction, lig, col, test=False)

            self.can_bis.configure(text=str(["White", "Black"][not self.player]) + "'s turn.\n \n" +
                                   "White : " + str(self.nb_pawn_player[0]) + "\n" +
                                   "Black : " + str(self.nb_pawn_player[1]))
        self.trace_grille()


class Ping(Frame):
    """corps principal du programme"""

    def __init__(self):
        Frame.__init__(self)
        self.master.geometry("890x673")
        self.master.title(" Jeu de Othello")

        self.m_bar = MenuBar(self)
        self.m_bar.pack(side=TOP, expand=NO, fill=X)

        self.jeu = Panel()
        self.jeu.pack(expand=YES, fill=BOTH, padx=8, pady=8)

        self.pack()

    def options(self):
        """Choice of the number of lines and columns for the grid"""
        opt = Toplevel(self)
        cur_l = Scale(opt, length=200, label="Number of lines :",
                      orient=HORIZONTAL,
                      from_=1, to=12, command=self.maj_lines)
        cur_l.set(self.jeu.n_lig)  # initial position of the cursor
        cur_l.pack()
        cur_h = Scale(opt, length=200, label="Number of columns :",
                      orient=HORIZONTAL,
                      from_=1, to=12, command=self.maj_columns)
        cur_h.set(self.jeu.n_col)
        cur_h.pack()

    def maj_columns(self, n):
        """maj_columns
        :type self: Ping
        """
        self.jeu.n_col = int(n)
        self.jeu.trace_grille()

    def maj_lines(self, n):
        """for giving a major of n"""
        self.jeu.n_lig = int(n)
        self.jeu.trace_grille()

    def reset(self):
        """  french!  """
        self.jeu.init_jeu()
        self.jeu.trace_grille()

    def principe(self):
        """window-message containing the small description of the principe of this game"""
        msg = Toplevel(self)
        Message(msg, bg="navy", fg="ivory", width=400,
                font="Helvetica 10 bold",
                text="To win, you must have the most of pawns.\n "
                     "At your turn, put a pawn down so as to surround some adversary's"
                     " pawns between the pawn you've put down and others pawns of your color.\n\n"
                     "Réf : I don't know") \
            .pack(padx=10, pady=10)

    def by_the_way(self):
        """window-message indicating the author and the type of licence"""
        msg = Toplevel(self)
        Message(msg, width=200, aspect=100, justify=CENTER,
                text="Jeu de Othello\n\n(C) \n"
                     "Licence = ????").pack(padx=10, pady=10)


if __name__ == '__main__':
    Ping().mainloop()

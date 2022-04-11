from tkinter import *

################################################
#  Game of Ping                                #
#  References: See the article in the journal  #
#  <Pour la science>, August 2002              #
#                                              #
# (C) Gerard Swinnen (Verviers, Belgium)       #
# http://www.ulg.ac.be/cifen/inforef/swi       #
#                                              #
#  Version du 29/09/2002 - Licence : GPL       #
################################################


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
        me1.add_command(label='Principle of the game', underline=0,
                        command=boss.principle)
        me1.add_command(label='By the way ...', underline=0,
                        command=boss.by_the_way)
        help_menu.configure(menu=me1)


class Panel(Frame):
    """Panel de jeu (grille de n x m cases)"""

    def __init__(self):
        # The panel of game is constituted of a re-scaling grid
        # containing it-self a canvas. at each re-scaling of the
        # grid, we calculate the tallest size possible for the
        # cases (squared) of the grid, et the dimensions of the
        # canvas are adapted in consequence.
        Frame.__init__(self)
        self.n_lig, self.n_col = 4, 4  # initial grid = 4 x 4
        # Link of the event <resize> with an adapted manager :
        self.bind("<Configure>", self.rescale)
        # Canvas :
        self.can = Canvas(self, bg="dark olive green", borderwidth=0,
                          highlightthickness=1, highlightbackground="white")
        # Link of the event <click of the mouse> with its manager :
        self.can.bind("<Button-1>", self.click)
        self.can.pack()
        self.state = []  # construction of a list of lists
        self.width, self.height = 2, 2
        self.cote = 0
        self.init_jeu()

    def init_jeu(self):
        """Initialisation of the list which remember the state of the game"""
        self.state = []
        for i in range(12):  # (equal to a panel
            self.state.append([0] * 12)  # of 12 lines x 12 columns)

    def rescale(self, event):
        """Operations made at each rescaling"""
        # the properties which are linked to the event of reconfiguration
        # contain all the new sizes of the panel :
        self.width, self.height = event.width - 4, event.height - 4
        # The subtraction of 4 pixels is here to compensate the width
        # of the 'highlight bordure' rolling the canvas)
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
        for _ in range(self.n_lig - 1):  # horizontal lines
            self.can.create_line(0, s, wide, s, fill="white")
            s += self.cote
        s = self.cote
        for _ in range(self.n_col - 1):  # vertical lines
            self.can.create_line(s, 0, s, high, fill="white")
            s += self.cote
        # Layout of all the pawns, white or black according to the s_ate of the game :
        for l_ in range(self.n_lig):
            for c_ in range(self.n_col):
                x1 = c_ * self.cote + 3  # size of pawns =
                x2 = (c_ + 1) * self.cote - 3  # size of the case -10
                y1 = l_ * self.cote + 3  #
                y2 = (l_ + 1) * self.cote - 3
                color = ["white", "black"][self.state[l_][c_]]
                self.can.create_oval(x1, y1, x2, y2, outline="grey",
                                     width=1, fill=color)

    def click(self, event):
        """Management of the mouse click : return the pawns"""
        # We start to determinate the line and the columns :
        lig, col = int(event.y / self.cote), int(event.x / self.cote)
        # we treat then the 8 adjacent cases :
        for l_ in range(lig - 1, lig + 2):
            if l_ < 0 or l_ >= self.n_lig:
                continue
            for c_ in range(col - 1, col + 2):
                if c_ < 0 or c_ >= self.n_col:
                    continue
                if l_ == lig and c_ == col:
                    continue
                # Return of the pawn by logic inversion :
                self.state[l_][c_] = not (self.state[l_][c_])
        self.trace_grille()


class Ping(Frame):
    """Main body of the ping game"""
    def __init__(self):
        Frame.__init__(self)
        self.master.geometry("800x600")
        self.master.title("Game of ping")

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

    def principle(self):
        """window-message containing the small description of the principle of this game"""
        msg = Toplevel(self)
        Message(msg, bg="navy", fg="ivory", width=400,
                font="Helvetica 10 bold",
                text="This is to do "
                     "de"
                     " grilles.\n A  !\n\n"
                     "Réf : revue 'Pour la Science' - August 2002") \
            .pack(padx=10, pady=10)

    def quit(self):
        pass

    def by_the_way(self):
        """window-message indicating the author and the type of licence"""
        msg = Toplevel(self)
        Message(msg, width=200, aspect=100, justify=CENTER,
                text="Jeu de Ping\n\n(C) Gerard Swinnen, August 2002.\n"
                     "Licence = GPL").pack(padx=10, pady=10)


if __name__ == '__main__':
    Ping().mainloop()

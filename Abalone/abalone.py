from math import sqrt

from tkinter import *


###########################################
#                                         #
#                                         #
#           Jeu de Abalone                #
#                                         #
#       Implementation in progress        #
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
        self.n_lig, self.n_col = 9, 9  # initial grid = 9 x 9
        self.state = [[0] * 9] * 9  # 0 = vacuum case
        # Link of the event <resize> with an adapted manager :
        self.bind("<Configure>", self.rescale)
        # Canvas :
        self.can = Canvas(self, bg="dark olive green", borderwidth=0,
                          highlightthickness=1, highlightbackground="white")
        self.width, self.height = 2, 2
        self.cote = 0
        self.init_jeu()
        # Link of the event <click of the mouse> with its manager :

        self.several_x_y = [[]]
        self.can.bind("<Button-1>", self.click)
        # self.can.bind("<Button1-Motion>", self.mouse_move)
        # self.can.bind("<Button1-ButtonRelease>", self.mouse_up)
        self.can.pack(side=LEFT)
        self.can_bis = Label(text="player 1")
        self.can_bis.pack(side=RIGHT)
        self.player = 1
        self.direction = [None, None]
        self.tte_directions = [[-1, 0], [-1, 1], [-1, -1], [0, 1], [0, -1], [1, -1]]
        # self.state = []  # construction of a list of lists

    def init_jeu(self):
        """Initialisation of the list which remember the state of the game"""
        self.state = [[0] * 9] * 9  # 0 = vacuum case
        self.state[0] = [None, None, None, None, 1, 1, 1, 1, 1]
        self.state[1] = [None, None, None, 1, 1, 1, 1, 1, 1]
        self.state[2] = [None, None, 0, 0, 1, 1, 1, 0, 0]
        self.state[3] = [None, 0, 0, 0, 0, 0, 0, 0, 0]
        self.state[4] = [0] * 9
        self.state[5] = [0, 0, 0, 0, 0, 0, 0, 0, None]
        self.state[6] = [0, 0, 2, 2, 2, 0, 0, None, None]
        self.state[7] = [2, 2, 2, 2, 2, 2, None, None, None]
        self.state[8] = [2, 2, 2, 2, 2, None, None, None, None]
        self.trace_grille()

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
        h_max = self.height / (1 + sqrt(3) * 4)
        # the side of a case would be the smallest of the two dimensions :
        self.cote = min(l_max, h_max)
        # -> establishment of new dimensions for the canvas :
        wide, high = self.cote * self.n_col, self.cote * self.n_lig
        self.can.configure(width=wide, height=high)
        # Layout of the grid:
        self.can.delete(ALL)  # erasing of the past Layouts
        # Layout of all the pawns, white or black according to the sate of the game :
        for l in range(self.n_lig):
            x0 = (l - 4) * 1 / 2 * self.cote + 3
            for c in range(self.n_col):
                if self.state[l][c] is not None:
                    y1 = l * sqrt(3)/2 * self.cote + 3  # size of pawns =
                    y2 = (l * sqrt(3)/2 + 1) * self.cote - 3  # size of the case -6
                    x1 = c * self.cote + x0
                    x2 = x1 + self.cote - 6
                    color = ["dark olive green", "white", "black"][self.state[l][c]]
                    self.can.create_oval(x1, y1, x2, y2, outline="grey",
                                         width=1, fill=color)

    def click(self, event):
        print(self.several_x_y)
        """Management of the mouse click : move the pawns"""
        # We start to determinate the line and the columns of the pawn touched:
        lig = int(2 * event.y / (self.cote * sqrt(3) + sqrt(3) / 2 + 1))
        col = int((event.x - (lig - 4) * 1 / 2 * self.cote) / self.cote)
        """if len(self.several_x_y) == 2:
            if self.state[lig][col] == self.player:
                self.several_x_y = [[]]
                self.several_x_y[0].append([lig, col])
                self.can.itemconfig(self.can.find_closest(event.x, event.y), width=3, outline='red')"""
        if len(self.several_x_y[0]) == 3:  # theoretically elif
            # if self.verify1(lig, col, pawn=0):
            self.can.itemconfig(self.can.find_closest(event.x, event.y), width=3, outline='yellow')
            self.several_x_y.append([lig, col])
            print(self.several_x_y)
            self.move()
            self.several_x_y = [[]]
            # else:
            # self.several_x_y = []
        else:
            print("good morning")
            if self.state[lig][col] == self.player:
                self.several_x_y[0].append([lig, col])
                self.can.itemconfig(self.can.find_closest(event.x, event.y), width=3, outline='red')
                print("several=", self.several_x_y)

    def mouse_move(self, event):
        # We start to determinate the line and the columns of the pawn touched:
        # lig = int(2 * event.y / (self.cote * sqrt(3) + sqrt(3) / 2 + 1))
        # col = int((event.x - (lig - 4) * 1 / 2 * self.cote) / self.cote)

        # print('self.several=', self.several_x_y, "...", self.several_x_y[0])
        if len(self.several_x_y) != 2 and len(self.several_x_y) != 0:
            lig = int(2 * event.y / (self.cote * sqrt(3) + sqrt(3) / 2 + 1))
            col = int((event.x - (lig - 4) * 1 / 2 * self.cote) / self.cote)
            print(lig, col)
            if self.several_x_y[0] and [lig, col] not in self.several_x_y[0] and self.verify1(lig, col):
                self.several_x_y[0].append([lig, col])
                self.can.itemconfig(self.can.find_closest(event.x, event.y), width=3, outline='red')

    def mouse_up(self, event):
        self.trace_grille()
        if len(self.several_x_y) == 2:
            self.trace_grille()
            self.move()
            self.direction = [None, None]
        else:
            self.several_x_y = [[]]
            type(event)

    def move(self):
        l2, c2 = self.several_x_y[1]
        l1, c1 = self.several_x_y[0][0]
        direction = l2-l1, c2-c1
        l, c = direction
        l3, c3 = self.several_x_y[0][2]
        if self.state[l3 + l][c3 + c] == (self.player % 2) + 1:
            self.state[l1][c1] = 0
            self.state[l3 + l][c3 + c] = self.player
            try:
                while self.state[l3+l][c3+c] != 0:
                    l3 += l
                    c3 += c
                    if self.state[l3][c3] is None or l3 < 0 or l3 > 8 or c3 < 0 or c3 > 8 or c3 < 4-l3 or c3 > 12-l3:
                        print([3][4])
                self.state[l3+l][c3+c] = (self.player % 2) + 1
            except IndexError:
                print("Player "+["white", "black"][(self.player % 2)]+" has lost a marble")
            self.player %= 2
            self.player += 1
            self.trace_grille()
            print("I don't know how do this moving")
        else:
            l, c = direction
            for pawn in self.several_x_y[0][::-1]:
                i, j = pawn
                self.state[i+l][j+c] = self.player
                self.state[i][j] = 0
            self.trace_grille()
            self.player %= 2
            self.player += 1

        # print("not made", self.player)

    #  def verify_right(self, x1, y1, x2, y2):  # todo finish!
    #  if x1 == x2 and y1 == y2:

    def verify1(self, lig, col, pawn=-1):
        print("hello")
        [x, y] = self.several_x_y[0][pawn]
        if pawn == -1:
            if self.state[lig][col] == self.player:
                direction = [lig - x, col - y]
                if self.direction:
                    if self.direction == direction:
                        return True
                    return False
                elif direction in self.tte_directions:
                    self.direction = direction
                    return True
                return False
            return False
        else:
            direction = [lig - x, col - y]
            if self.direction:
                if self.direction != direction:
                    return True
                return False
            elif direction in self.tte_directions:
                self.direction = direction
                return True
            return False


class Ping(Frame):
    """corps principal du programme"""

    def __init__(self):
        Frame.__init__(self)
        self.master.geometry("900x750")
        self.master.title(" Game of abalone")

        self.m_bar = MenuBar(self)
        self.m_bar.pack(side=TOP, expand=NO, fill=X)

        self.jeu = Panel()
        self.jeu.pack(expand=YES, fill=BOTH, padx=8, pady=8)

        self.pack()

    def reset(self):
        """  french!  """
        self.jeu.init_jeu()
        self.jeu.trace_grille()

    def principe(self):
        """window-message containing the small description of the principe of this game"""
        msg = Toplevel(self)
        Message(msg, bg="navy", fg="ivory", width=400,
                font="Helvetica 10 bold",
                text="This is to do "
                     "de"
                     " grilles.\n A  !\n\n"
                     "Réf : revue 'Pour la Science' - August 2002") \
            .pack(padx=10, pady=10)

    def by_the_way(self):
        """window-message indicating the author and the type of licence"""
        msg = Toplevel(self)
        Message(msg, width=200, aspect=100, justify=CENTER,
                text="Jeu de Abalone\n\n(C) Gerard Swinnen, August 2002.\n"
                     "Licence = GPL").pack(padx=10, pady=10)


if __name__ == '__main__':
    Ping().mainloop()

#! /usr/bin/python
# -*- coding: utf-8 -*-
# #########Allumettes###########

from turtle import *
from tkinter import *


# Fonction qui permet d'autoriser l'effaçage d'une allumette en fonction de plusieurs choses, tout d'abord bien sur si
# le joueur clique sur une allumette, et ensuite si il n'a pas déjà effacé pendant son tour une allumette
# d'un autre étage.

def efface(x, y):
    a = [x, y]
    global line_select
    global state
    for index, value in enumerate(list_matchstick):
        z = value.pos()
        if (abs(a[0] - z[0]) < 10 and abs(a[1] - z[1]) < 25) and (
                        line_select.get() == -1 or z[1] == line_select.get()):
            value.ht()
            state -= 1
            win()
            if line_select.get() == -1:
                line_select.set(z[1])


# La variable état représente le nombre d'allumettes restantes en jeux, quand elle est a 0, l'avant dernier joueur est
# le gagnant.

def win():
    if state == 0:
        window_toto2 = Toplevel(window_toto)
        announce = Label(window_toto2, text="Congratulations Player %d, you've won !!!" % state_player.get())
        announce.pack()
        ok_btn = Button(window_toto2, text="OK", command=window_toto2.destroy)
        ok_btn.pack()

        pos_x = window_toto2.winfo_screenwidth()
        pos_y = window_toto2.winfo_screenheight()
        diff_x = 300
        diff_y = 50
        x = (pos_x / 2) - (diff_x / 2)
        y = (pos_y / 2) - (diff_y / 2)
        window_toto2.geometry('%dx%d+%d+%d' % (diff_x, diff_y, x, y))


# Fonction qui ré-initialise les variable afin de pouvoir faire une nouvelle partie
def new_part():
    global state, state_player, line_select, list_matchstick
    state = 16
    state_player.set(2)
    line_select.set(-1)
    for match in list_matchstick:
        match.st()


# Création d'une fenêtre TK pour pouvoir y placer les radioboutton, ainsi que le bouton recommencer

window_toto = Tk()
window_toto.title("Matchstick")

posx = window_toto.winfo_screenwidth()
posy = window_toto.winfo_screenheight()
# Dimension de la fenêtre 800x600
diffx = 800
diffy = 600
x0 = (posx / 2) - (diffx / 2)
y0 = (posy / 2) - (diffy / 2)
window_toto.geometry('%dx%d+%d+%d' % (diffx, diffy, x0, y0))

canvas1 = Canvas(window_toto, width=800, height=600)
canvas1.pack()
screen1 = TurtleScreen(canvas1)
state_player = IntVar()
line_select = IntVar()

# Création des 16 curseurs qui auront l'image d'une allumette

a1 = RawTurtle(screen1)
a2 = RawTurtle(screen1)
a3 = RawTurtle(screen1)
a4 = RawTurtle(screen1)
a5 = RawTurtle(screen1)
a6 = RawTurtle(screen1)
a7 = RawTurtle(screen1)
a8 = RawTurtle(screen1)
a9 = RawTurtle(screen1)
a10 = RawTurtle(screen1)
a11 = RawTurtle(screen1)
a12 = RawTurtle(screen1)
a13 = RawTurtle(screen1)
a14 = RawTurtle(screen1)
a15 = RawTurtle(screen1)
a16 = RawTurtle(screen1)

# On les place dans une liste afin de faciliter leur gestions (leur assigner l'image de l'allumette, les placer au bon
# endroit etc
list_matchstick = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16]

screen1.register_shape("Allumettes/allumettes.gif")
screen1.bgpic("Allumettes/alu2.gif")

for i in list_matchstick:
    i.shape("Allumettes/allumettes.gif")

# Cette liste contient les positions de chaque allumette, afin qu'elles représente un triangle
triangle_toto = [[0, 210], [-30, 140], [0, 140], [30, 140], [-60, 70], [-30, 70], [0, 70], [30, 70], [60, 70], [-90, 0],
                 [-60, 0], [-30, 0], [0, 0], [30, 0], [60, 0], [90, 0]]

# On place les allumettes correctement
for index, value in enumerate(triangle_toto):
    list_matchstick[index].up()
    list_matchstick[index].goto(value)
    list_matchstick[index].down()

new_part()

for i in list_matchstick:
    i.onclick(efface, btn=1)

# Création des 2 radiobuttons pour changer de joueur et du bouton recommencer
player_1 = Radiobutton(text="Joueur 1", variable=state_player, value=2, command=lambda: [line_select.set(-1)])
player_2 = Radiobutton(text="Joueur 2", variable=state_player, value=1, command=lambda: [line_select.set(-1)])
reco = Button(text="Nouvelle Partie", command=new_part)

# On les place correctement
player_1.place(x=150, y=100)
player_2.place(x=150, y=150)
reco.place(x=150, y=200)

window_toto.mainloop()

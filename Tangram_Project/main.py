#! /usr/bin/python
# -*- coding: utf-8 -*-
from turtle import *
from turtle import TK
from tkinter import *
from random import randrange
import os
import pickle


# Fonctions
from math import sqrt


def distance(x, y):
    '''Cette fonction calcule la distance entre deux points x,y assimilables à des tuples'''
    dist = sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))
    return dist


def detection():
    '''Cette fonction détecte si le niveau est terminé ou non'''
    test = True
    # on initialise le le test comme étant vrai, si l'une des conditions du niveau n'est pas remplit il deviendra faux.
    for i, pt in enumerate(tabl_end):

        # premier test : les positions.
        if i == 0:
            if distance(tabl[0], pt) <= 5 or distance(tabl[1], pt) <= 5:
                d1 = distance(tabl[0], pt)
                d2 = distance(tabl[1], pt)
                if d1 < d2:
                    C_tri1.goto(tabl_end[0])
                elif d1 - d2 < 5:
                    C_tri1.goto(tabl_end[0])
                    C_tri2.goto(tabl_end[0])
                else:
                    C_tri2.goto(tabl_end[0])
            else:
                test = False

        if i == 1:
            if distance(tabl[1], pt) <= 5 or distance(tabl[0], pt) <= 5:
                d1 = distance(tabl[0], pt)
                d2 = distance(tabl[1], pt)
                if d1 < d2:
                    C_tri1.goto(tabl_end[1])
                elif d1 - d2 < 5:
                    C_tri1.goto(tabl_end[1])
                    C_tri2.goto(tabl_end[1])
                else:
                    C_tri2.goto(tabl_end[1])
            else:
                test = False
                # les deux grands triangles

        if i == 3:
            if distance(tabl[3], pt) <= 5 or distance(tabl[4], pt) <= 5:
                d1 = distance(tabl[3], pt)
                d2 = distance(tabl[4], pt)
                if d1 < d2:
                    C_tripe1.goto(tabl_end[3])
                elif d1 - d2 < 5:
                    C_tripe1.goto(tabl_end[3])
                    C_tripe2.goto(tabl_end[3])
                else:
                    C_tripe2.goto(tabl_end[3])
            else:
                test = False

        if i == 4:
            if distance(tabl[4], pt) <= 5 or distance(tabl[3], pt) <= 5:
                d1 = distance(tabl[3], pt)
                d2 = distance(tabl[4], pt)
                if d1 < d2:
                    C_tripe1.goto(tabl_end[4])
                elif d1 - d2 < 5:
                    C_tripe1.goto(tabl_end[4])
                    C_tripe2.goto(tabl_end[4])
                else:
                    C_tripe2.goto(tabl_end[4])
            else:
                test = False
                # les deux petits triangles

                # Ces 4 premiers tests sont plus complexes car on ne sait pas quel triangle le joueur va choisir
                # (2 emplacements pour chaque triangle).

        if i == 2:
            if distance(tabl[i], pt) <= 5:
                C_trimoy.goto(pt)
            else:
                test = False
                # le triangle moyen

        if i == 5:
            if distance(tabl[i], pt) <= 5:
                C_carre.goto(pt)
            else:
                test = False
                # le carré

        if i == 6:
            if distance(tabl[i], pt) <= 5:
                C_para.goto(pt)
            else:
                test = False
                # le parallélogramme

                # Cette première partie fait donc en sorte qu'un élément a une distance > à 5 de sa position finale se
                # met à celle-ci

    for i, cpt in enumerate(comp):
        if i == 0:
            if cpt != comp_end[0] and cpt != comp_end[1]:
                test = False
        if i == 1:
            if cpt != comp_end[0] and cpt != comp_end[1]:
                test = False
        if i == 3:
            if cpt != comp_end[3] and cpt != comp_end[4]:
                test = False
        if i == 4:
            if cpt != comp_end[3] and cpt != comp_end[4]:
                test = False
        if i == 2:
            if cpt != comp_end[i]:
                test = False
        if i == 5:
            if cpt != comp_end[i]:
                test = False
        if i == 6:
            if cpt != comp_end[i]:
                test = False
    # deuxieme test qui regarde si la rotation des éléments est la bonne

    if reverse != reverse_end:
        test = False
    # Dernier test vérifiant si le parallélogramme doit ou non être inverser

    s1.update()

    if test:
        # le test est vrai, annonçons le au joueur
        fen3 = Toplevel()
        fen3.title("Bravo !")

        fond = Label(fen3, image=image6)
        # Initialisation d'une fenêtre qui a un fond que l'on affiche grâce à un label ( qui est ici une image )
        res = Button(fond, image=image7, command=lambda: [restart(),
                                                          fen3.destroy()
                                                          ]
                     )
        by = Button(fond, image=image8, command=fen.quit)

        # création d'un bouton recommencer et d'un bouton quitter ( qui quitte le jeu entièrement)

        fond.pack()
        res.place(x=xres, y=yres)
        by.place(x=xby, y=yby)
        posx = fen3.winfo_screenwidth()
        posy = fen3.winfo_screenheight()
        diffx = T_fen_end
        diffy = T_fen_end2
        x = (posx / 2) - (diffx / 2)
        y = (posy / 2) - (diffy / 2)
        fen3.geometry('%dx%d+%d+%d' % (diffx, diffy, x, y))
        # affichage et centrage de la fenêtre.


def restart():
    '''Cette fonction permet de recomencer un niveau'''

    global comp, tabl, reverse, helped
    # récupération des variables à modifier en tant que variable globale

    tabl = list(carre[0])
    comp = list(carre[1])
    reverse = carre[2]
    # modification (ou création) du tableau de positition et du tableau de rotation courant ainsi que de la variable
    # indiquant si le parallélogramme est inversé
    helped = 2
    # la variable helped est remise à deux pour pouvoir réutiliser l'aide ( voir fonction see())
    init()
    # appel de la fonction init pour que les changements prennent effets


def init():
    '''Cette fonction initialise les éléments avec leur position et rotation respective qui sont dans comp et tabl'''

    C_tri1.up()
    C_tri2.up()
    C_tripe1.up()
    C_tripe2.up()
    C_trimoy.up()
    C_carre.up()
    C_para.up()

    C_tri1.shape("tri1")
    C_tri2.shape("tri2")
    C_tripe1.shape("tripe1")
    C_tripe2.shape("tripe2")
    C_trimoy.shape("trimoy")
    C_carre.shape("carre")
    C_para.shape("para1")

    C_tri1.seth(comp[0] * 15)
    C_tri1.goto(tabl[0])
    C_tri2.seth(comp[1] * 15)
    C_tri2.goto(tabl[1])
    C_trimoy.seth(comp[2] * 15)
    C_trimoy.goto(tabl[2])
    C_tripe1.seth(comp[3] * 15)
    C_tripe1.goto(tabl[3])
    C_tripe2.seth(comp[4] * 15)
    C_tripe2.goto(tabl[4])
    C_carre.seth(comp[5] * 15)
    C_carre.goto(tabl[5])
    C_para.seth(comp[6] * 15)
    C_para.goto(tabl[6])
    color_init()
    # appel de la fonction color_init pour récupérer et afficher les couleurs des éléments


def color_init():
    '''Cette fonction met à jour la couleur des éléments du tangram (permet au joueur de personnaliser son jeu'''
    C_para.color(C_color7.get())
    C_carre.color(C_color6.get())
    C_tripe2.color(C_color5.get())
    C_tripe1.color(C_color4.get())
    C_trimoy.color(C_color3.get())
    C_tri2.color(C_color2.get())
    C_tri1.color(C_color1.get())

    s1.update()


def sav_color():
    '''Cette fonction récupère et sauvegarde dans un fichier les couleurs choisies par le joueur pour son tangram'''
    with open("sav_color.txt", "wb") as sauvegarde_couleur:
        sav = pickle.Pickler(sauvegarde_couleur)
        sav.dump(C_color1.get())
        sav.dump(C_color2.get())
        sav.dump(C_color3.get())
        sav.dump(C_color4.get())
        sav.dump(C_color5.get())
        sav.dump(C_color6.get())
        sav.dump(C_color7.get())


def sav_res(res):
    '''Cette fonction change la résolution par défaut par celle sélectionnée par le joueur et la place dans le fichier
    qui est lu au démarage du jeu
    pour initialiser les fenêtres'''
    with open("sav_res.txt", "wb") as sauvegarde_resolution:
        sav = pickle.Pickler(sauvegarde_resolution)
        sav.dump(res)

    advise = Toplevel()
    redem = Label(advise, text="Vous devez relancer l'application pour que les changements prennent effet !")
    btn_quit = Button(advise, text="Fermer l'application", command=fen.quit)
    redem.pack()
    btn_quit.pack()

    posx = advise.winfo_screenwidth()
    posy = advise.winfo_screenheight()
    diffx = 500
    diffy = 50
    x = (posx / 2) - (diffx / 2)
    y = (posy / 2) - (diffy / 2)
    advise.geometry('%dx%d+%d+%d' % (diffx, diffy, x, y))
    # création et centrage d'une fenêtre demandant au joueur de redémarrer l'application pour que les changements
    # prennent effet


def rotation0(x, y):
    '''fonction de rotation pour C_tri1'''
    comp[0] += 1
    C_tri1.seth(comp[0] * 15)
    if comp[0] == 24:
        comp[0] = 0
    s1.update()


def rotation1(x, y):
    '''fonction de rotation pour C_tri2'''
    comp[1] += 1
    C_tri2.seth(comp[1] * 15)
    if comp[1] == 24:
        comp[1] = 0
    s1.update()


def rotation2(x, y):
    '''fonction de rotation pour C_trimoy'''
    comp[2] += 1
    C_trimoy.seth(comp[2] * 15)
    if comp[2] == 24:
        comp[2] = 0
    s1.update()


def rotation3(x, y):
    '''fonction de rotation pour C_tripe1'''
    comp[3] += 1
    C_tripe1.seth(comp[3] * 15)
    if comp[3] == 24:
        comp[3] = 0
    s1.update()


def rotation4(x, y):
    '''fonction de rotation pour C_tripe2'''
    comp[4] += 1
    C_tripe2.seth(comp[4] * 15)
    if comp[4] == 24:
        comp[4] = 0
    s1.update()


def rotation5(x, y):
    '''fonction de rotation pour C_carre'''
    comp[5] += 1
    C_carre.seth(comp[5] * 15)
    if comp[5] == 6:
        comp[5] = 0
    s1.update()


def rotation6(x, y):
    '''fonction de rotation pour C_para'''
    comp[6] += 1
    C_para.seth(comp[6] * 15)
    if comp[6] == 12:
        comp[6] = 0
    s1.update()


'''les 6 fonctions rotations sont necessaires car on ne peut pas récupérer l'objet curseur actif au moment du clic
de plus, une fonction lambda ne peut pas recevoir d'argument ce qui rend son utilisation avec onclick impossible
Ces dernières mettent aussi à jour la table des rotation (comp)'''


def reverse_para(event):
    '''Cette fonction récupere la forme de l'objet C_para et lui assigne sa forme symétrique'''
    global reverse

    forme = C_para.shape()
    if forme == "para1":
        reverse = True
        C_para.shape("para2")
    if forme == "para2":
        reverse = False
        C_para.shape("para1")
    s1.update()


def where(event):
    '''Cette fonction met a jour la table des positions (tabl)'''
    tabl[0] = C_tri1.position()
    tabl[1] = C_tri2.position()
    tabl[2] = C_trimoy.position()
    tabl[3] = C_tripe1.position()
    tabl[4] = C_tripe2.position()
    tabl[5] = C_carre.position()
    tabl[6] = C_para.position()

    detection()
    # lance la fonction détection pour voir si le tangram est terminé


def level(lvl):
    '''Cette fonction configure le jeu pour afficher le niveau choisi par l'utilisateur'''
    global tabl_end, comp_end, reverse_end

    tabl_end = lvl[0]
    comp_end = lvl[1]
    reverse_end = lvl[2]
    bgc = lvl[3]
    s1.bgpic(bgc)
    # mise de tabl_end comp_end et reverse_end qui sont utilisées dans detection et mise à jour du fond d'écran

    restart()


def see():
    '''Cette fonction permet au joueur d'obtenir de l'aide si le joueur en demande'''
    global helped

    helped -= 1
    # on décrémente helped (appelé en global) car l'aide est limitée à deux par jeu

    if helped >= 0:
        # si le joueur à droit à un peu d'aide, on l'aide
        curseur = [C_tri1, C_tri2, C_trimoy, C_tripe1, C_tripe2, C_carre, C_para]
        fond = s1.bgpic()
        # récupération du fond d'écran (permet de savoir à quel niveau on est
        cpt = len(curseur)
        j = randrange(0, cpt)
        # on tire un curseur au hasard
        if fond == "HT/1000x700/canard.gif" or fond == "HT/500x350/canard.gif":
            curseur[j].goto(canard[0][j])
            curseur[j].seth(canard[1][j] * 15)
            tabl[j] = canard[0][j]
            comp[j] = canard[1][j]
            if reverse != canard[3] and (curseur[j].shape() == "para1" or curseur[j].shape() == "para2"):
                reverse_para(False)
        if fond == "HT/1000x700/lapin.gif" or fond == "HT/500x350/lapin.gif":
            curseur[j].goto(lapin[0][j])
            curseur[j].seth(lapin[1][j] * 15)
            tabl[j] = lapin[0][j]
            comp[j] = lapin[1][j]
            if reverse != lapin[3] and (curseur[j].shape() == "para1" or curseur[j].shape() == "para2"):
                reverse_para(False)
        if fond == "HT/1000x700/prosterne.gif" or fond == "HT/500x350/prosterne.gif":
            curseur[j].goto(prosterne[0][j])
            curseur[j].seth(prosterne[1][j] * 15)
            tabl[j] = prosterne[0][j]
            comp[j] = prosterne[1][j]
            if reverse != prosterne[3] and (curseur[j].shape() == "para1" or curseur[j].shape() == "para2"):
                reverse_para(False)
        if fond == "HT/1000x700/figure.gif" or fond == "HT/500x350/figure.gif":
            curseur[j].goto(figure[0][j])
            curseur[j].seth(figure[1][j] * 15)
            tabl[j] = figure[0][j]
            comp[j] = figure[1][j]
            if reverse != figure[3] and (curseur[j].shape() == "para1" or curseur[j].shape() == "para2"):
                reverse_para(False)
                # pour le niveau courant, on met le curseur tiré au hasard à sa place on le tourne correctement
                # et on met à jour la table des positions et des rotations si le curseur tiré est C_para,
                # on regarde en plus s'il doit être retourné et on lance la fonction reverse_para
                # qui se charge de mettre à jour reverse
    else:
        fen4 = Toplevel()
        attention = Label(fen4, text="Attention vous avez utilisé l'aide trop de fois ! ")
        btnok = Button(fen4, text="OK", command=fen4.destroy)
        attention.pack()
        btnok.pack()

        posx = fen4.winfo_screenwidth()
        posy = fen4.winfo_screenheight()
        diffx = 300
        diffy = 50
        x = (posx / 2) - (diffx / 2)
        y = (posy / 2) - (diffy / 2)
        fen4.geometry('%dx%d+%d+%d' % (diffx, diffy, x, y))

        # si le joueur a utilisé deux fois l'aide, on lui signale qu'il ne peut plus utiliser cette fonction pour
        # le moment à l'aide d'une fenetre

    s1.update()


def Tangram():
    '''Cette fonction est le coeur du programme elle gère le tangram même'''
    # Init
    global s1, C_tri1, C_tri2, C_trimoy, C_tripe1, C_tripe2, C_carre, C_para, C_color1, C_color2, C_color3, C_color4, \
        C_color5, C_color6, C_color7, helped

    fen2 = Toplevel()
    # Création d'une nouvelle fenètre
    cv1 = Canvas(fen2, width=T_fen, height=T_fen2)
    s1 = TurtleScreen(cv1)
    p = RawTurtle(s1)
    # Création d'un canvas Tkinter dans lequel on crée un écran turtle et un premier curseur nommé p.

    C_tri1 = RawTurtle(s1)
    C_tri2 = RawTurtle(s1)
    C_trimoy = RawTurtle(s1)
    C_tripe1 = RawTurtle(s1)
    C_tripe2 = RawTurtle(s1)
    C_carre = RawTurtle(s1)
    C_para = RawTurtle(s1)
    # création des curseurs qui seront les éléments du Tangram

    cv1.pack()
    # affichage du canvas(et donc de l'écran turtle)

    C_color1 = StringVar()
    C_color2 = StringVar()
    C_color3 = StringVar()
    C_color4 = StringVar()
    C_color5 = StringVar()
    C_color6 = StringVar()
    C_color7 = StringVar()
    # création des objets qui contiendront les couleurs des curseurs, on utilise ici des objets pour permettre la mise
    # à jour simple des couleurs grâce à des radiobutton

    with open("sav_color.txt", "rb") as sauvegarde_couleur:
        color_val = pickle.Unpickler(sauvegarde_couleur)
        colorset[0] = color_val.load()
        colorset[1] = color_val.load()
        colorset[2] = color_val.load()
        colorset[3] = color_val.load()
        colorset[4] = color_val.load()
        colorset[5] = color_val.load()
        colorset[6] = color_val.load()
    # lecture des couleurs sauvegardées par le joueur dans le fichier sav_color.txt

    C_color1.set(colorset[0])
    C_color2.set(colorset[1])
    C_color3.set(colorset[2])
    C_color4.set(colorset[3])
    C_color5.set(colorset[4])
    C_color6.set(colorset[5])
    C_color7.set(colorset[6])
    # assignation des chaînes contenant le nom des couleurs aux objets créés plus tôt

    # Nous allons à présent créer le menu qui est situé en haut de la fenêtre de jeu
    menu1 = Menu(fen2)

    fichier = Menu(menu1, tearoff=0)
    menu1.add_cascade(label="Fichier", menu=fichier)
    fichier.add_command(label="Recommencer", command=restart)
    # la commande Fichier/recommencer permet au joueur de remettre son niveau à 0 grâce à la fonction restart
    options = Menu(fichier, tearoff=0)
    fichier.add_cascade(label="Options", menu=options)
    color = Menu(options, tearoff=1)
    options.add_cascade(label="Couleur", menu=color)
    triangle1 = Menu(options, tearoff=0)
    triangle2 = Menu(options, tearoff=0)
    trianglemoy = Menu(options, tearoff=0)
    trianglepe1 = Menu(options, tearoff=0)
    trianglepe2 = Menu(options, tearoff=0)
    carree = Menu(options, tearoff=0)
    paral = Menu(options, tearoff=0)
    # ici nous allons définir un menu pour chaque élément du tangram qui permetra au joueur de personnaliser les
    # couleurs de son jeu qui sont automatiquement mis à jour grâce à la fonction color_init()

    liste_init = [["Triangle 1", triangle1, C_color1], ["Triangle 2", triangle2, C_color2],
                  ["Triangle Moyen", trianglemoy, C_color3], ["Petit Triangle 1", trianglepe1, C_color4],
                  ["Petit Triangle 2", trianglepe2, C_color5], ["Carre", carree, C_color6],
                  ["Parallélogramme", paral, C_color7]]
    liste_init_color = [["Rouge", "red"], ["Bleu", "blue"], ["Vert", "green"], ["Jaune", "yellow"], ["Rose", "pink"],
                        ["Violet", "purple"], ["Noir", "black"], ["Blanc", "white"], ["Orange", "orange"],
                        ["Bleu Ciel", "skyblue"], ["Or", "gold"], ["Marron", "brown"]]

    for i in liste_init:
        color.add_cascade(label=i[0], menu=i[1])
        for j in liste_init_color:
            i[1].add_radiobutton(label=j[0], value=j[1], variable=i[2], command=color_init)

    color.add_separator()
    color.add_command(label="Défaut", command=lambda: [C_color1.set(color_default[0]), C_color2.set(color_default[1]),
                                                       C_color3.set(color_default[2]), C_color4.set(color_default[3]),
                                                       C_color5.set(color_default[4]), C_color6.set(color_default[5]),
                                                       C_color7.set(color_default[6]), color_init()])
    # permet au joueur de remettre les couleurs par défaut du jeu
    color.add_separator()
    color.add_command(label="Sauvegarder", command=sav_color)
    # sauvegarde la configuration des couleurs grâce a la fonction
    resolution = Menu(options, tearoff=0)
    options.add_cascade(label="Résolution", menu=resolution)
    resolution.add_command(label="1000x700", command=lambda: sav_res("1000x700"))
    resolution.add_command(label="500x350", command=lambda: sav_res("500x350"))
    # permet de modifier la résolution courante
    fichier.add_command(label="Quitter", command=fen.quit)
    # permet au joueur de quitter complètement le programme

    niveaux = Menu(menu1, tearoff=0)
    menu1.add_cascade(label="Niveau", menu=niveaux)

    niveaux.add_command(label="Canard", command=lambda: level(canard))
    niveaux.add_command(label="Lapin", command=lambda: level(lapin))
    niveaux.add_command(label="Homme prosterné", command=lambda: level(prosterne))
    niveaux.add_command(label="Homme Rigolant", command=lambda: level(figure))
    # permet de choisir le niveau

    aide = Menu(menu1, tearoff=0)
    menu1.add_cascade(label="Aide", menu=aide)

    aide.add_command(label="Coups de pouce : 2 par partie", command=see)
    # lance la fonction see pour placer un des éléments du Tangram
    aide.add_command(label="Comment Jouer ?", command=lambda: os.system("gedit comment_jouer.txt"))
    # affiche dans gedit le fichier commen_jouer.txt

    bonus = Menu(menu1, tearoff=0)
    menu1.add_cascade(label="Bonus", menu=bonus)
    bonus.add_command(label="Taquin", command=lambda: os.system("python Taquin/taquin.py"))
    bonus.add_command(label="Allumettes", command=lambda: os.system("python Allumettes/allumettes.py"))
    # permet de lancer les scripts contenant les jeux bonus : le jeu de Allumette et le Taquin

    fen2.config(menu=menu1)
    # affectation du menu à notre fenêtre de jeu

    posx = fen2.winfo_screenwidth()
    posy = fen2.winfo_screenheight()
    diffx = T_fen
    diffy = T_fen2
    x = (posx / 2) - (diffx / 2)
    y = (posy / 2) - (diffy / 2)
    fen2.geometry('%dx%d+%d+%d' % (diffx, diffy, x, y))
    # centrage de la fenêtre de jeu

    p._tracer(8, 25)
    # configure la vitesse de tracer du curseur p de façon à ce que l'on ne remarque pas l'initialisation des curseurs

    # Création des curseurs

    p.ht()
    p.up()

    p.begin_poly()
    p.fd(cote / 4)
    p.right(135)
    p.fd((cote * sqrt(2)) / 4)
    p.right(90)
    p.fd((cote * sqrt(2)) / 4)
    p.seth(0)
    p.fd(cote / 4)
    p.end_poly()
    tripe1 = p.get_poly()
    s1.register_shape("tripe1", tripe1)
    s1.register_shape("tripe2", tripe1)

    p.begin_poly()
    p.fd(cote / 2)
    p.right(135)
    p.fd((cote * sqrt(2)) / 2)
    p.right(90)
    p.fd((cote * sqrt(2)) / 2)
    p.seth(0)
    p.fd(cote / 2)
    p.end_poly()
    tri1 = p.get_poly()
    s1.register_shape("tri1", tri1)
    s1.register_shape("tri2", tri1)

    p.begin_poly()
    p.left(90)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 4)
    p.right(90)
    p.fd(cote / 8)
    p.right(90)
    p.fd(cote / 4)
    p.seth(225)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 2)
    p.seth(90)
    p.fd(cote / 2)
    p.seth(45)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 2)
    p.seth(270)
    p.fd(cote / 4)
    p.right(90)
    p.fd(cote / 8)
    p.goto(0, 0)
    p.seth(0)
    p.end_poly()
    para1 = p.get_poly()
    s1.register_shape("para1", para1)

    p.begin_poly()
    p.right(90)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 4)
    p.left(90)
    p.fd(cote / 8)
    p.right(90)
    p.fd(cote / 4)
    p.seth(135)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 2)
    p.seth(90)
    p.fd(cote / 2)
    p.seth(315)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 2)
    p.seth(0)
    p.right(90)
    p.fd(cote / 4)
    p.right(90)
    p.fd(cote / 8)
    p.goto(0, 0)
    p.end_poly()
    para2 = p.get_poly()
    s1.register_shape("para2", para2)

    p.begin_poly()
    p.left(90)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 4)
    p.right(90)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 4)
    p.right(90)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 2)
    p.right(90)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 2)
    p.right(90)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 2)
    p.right(90)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 4)
    p.right(90)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 4)
    p.seth(0)
    p.end_poly()
    carre = p.get_poly()
    s1.register_shape("carre", carre)

    p.begin_poly()
    p.left(45)
    p.fd(sqrt((cote / 2) ** 2 + (cote / 2) ** 2) / 2)
    p.right(135)
    p.fd(cote / 2)
    p.right(90)
    p.fd(cote / 2)
    p.goto(0, 0)
    p.end_poly()
    trimoy = p.get_poly()
    s1.register_shape("trimoy", trimoy)

    # pour créer les curseurs on enregistre une forme que l'on dessine avec le curseur p puis on l'enregistre en temps
    # que shape pour notre écran turtle

    # Corps

    level(canard)
    # on choisi le niveau par défaut

    # le jeu est prêt on fait donc un restart pour que l'initialisation se termine et que le joueur puisse commencer
    # la partie
    restart()

    C_tri1.onclick(rotation0, btn=3)
    C_tri2.onclick(rotation1, btn=3)
    C_trimoy.onclick(rotation2, btn=3)
    C_tripe1.onclick(rotation3, btn=3)
    C_tripe2.onclick(rotation4, btn=3)
    C_carre.onclick(rotation5, btn=3)
    C_para.onclick(rotation6, btn=3)

    C_tri1.ondrag(C_tri1.goto)
    C_tri2.ondrag(C_tri2.goto)
    C_tripe1.ondrag(C_tripe1.goto)
    C_tripe2.ondrag(C_tripe2.goto)
    C_trimoy.ondrag(C_trimoy.goto)
    C_carre.ondrag(C_carre.goto)
    C_para.ondrag(C_para.goto)
    # initialisation des bindings pour que le joueur puisse faire tourner l'élément et le déplacer

    cv1.bind("<ButtonRelease-1>", where)
    cv1.bind("<Double-Button-1>", reverse_para)
    # 2 derniers binds pour metre à jour tabl et pour permettre au joueur de faire le symétrique du parallélogramme

    s1.listen()
    # il ne reste plus qu'à attendre un évenement


# Création des première variable : les couleurs, les couleurs par défaut et le nombre d'aides disponibles

colorset = ["brown", "purple", "pink", "yellow", "blue", "red", "green"]

color_default = ["brown", "purple", "pink", "yellow", "blue", "red", "green"]

helped = 2

# Première fenêtre

fen = TK.Tk()
fen.title("Tangram Project")

# Initialisation de la résolution

with open("sav_res.txt", "rb") as sauvegarde_resolution:
    res_val = pickle.Unpickler(sauvegarde_resolution)
    res = res_val.load()
# lecture dans sav_res.txt de la résolution du programme ( par défaut 1000x700 )

if res == "1000x700":
    image1 = PhotoImage(file="HT/1000x700/Tangram.gif")
    image2 = PhotoImage(file="HT/1000x700/main.gif")
    image3 = PhotoImage(file="HT/1000x700/Jouer.gif")
    image4 = PhotoImage(file="HT/1000x700/Crédits.gif")
    image5 = PhotoImage(file="HT/1000x700/Quitter.gif")
    image6 = PhotoImage(file="HT/1000x700/end.gif")
    image7 = PhotoImage(file="HT/1000x700/reco.gif")
    image8 = PhotoImage(file="HT/1000x700/quitter_end.gif")
    # importation des images qui dépendent de la résolution (le fond des fenètres)
    T_fen = 1000
    T_fen2 = 700
    T_fen_end = 300
    T_fen_end2 = 210
    # configuration de la taille des fenêtres principales et de la fenêtre de fin de jeu
    cote = 200
    # taille du coté principal des éléments du tangram
    xbtn = 410
    ybtn = 252
    xbtn1 = 400
    ybtn1 = 375
    xbtn2 = 400
    ybtn2 = 490
    xres = 5
    yres = 140
    xby = 180
    yby = 137
    # configuration des emplacements des diffèrents bouton qui dépendent de la résolution contenu dans les fenetre
    carre = [[(409.00, 2.00), (308.00, -99.00), (257.00, 52.00), (358.00, 103.00), (258.00, 1.00), (308.00, 53.00),
              (232.00, -34.00)], [0, 18, 18, 6, 12, 3, 6], False]
    canard = [
        [(-161.00, -21.00), (-160.00, -21.00), (-262.00, -91.00), (-384.00, 10.00), (-60.00, 30.00), (-334.00, 61.00),
         (-309.00, -25.00)], [0, 12, 15, 12, 6, 3, 6], False, "HT/1000x700/canard.gif"]
    prosterne = [
        [(-230.00, 26.00), (-154.00, 18.00), (-292.00, -21.00), (-304.00, 28.00), (-86.00, -107.00), (-39.00, -25.00),
         (-319.00, -55.00)], [16, 13, 13, 19, 16, 2, 1], False, "HT/1000x700/prosterne.gif"]
    lapin = [[(-281.00, -115.00), (-251.00, -44.00), (-253.00, 128.00), (-200.00, -81.00), (-250.00, -30.00),
              (-216.00, 59.00), (-198.00, 137.00)], [3, 0, 21, 0, 12, 0, 4], False, "HT/1000x700/lapin.gif"]
    figure = [
        [(-223.00, 16.00), (-240.00, -111.00), (-228.00, 138.00), (-285.00, 26.00), (-322.00, 33.00), (-219.00, -39.00),
         (-184.00, 131.00)], [15, 9, 0, 12, 9, 3, 9], True, "HT/1000x700/figure.gif"]
    # tableaux contenant toutes les informations pour la réalisation des niveaux ( 1 : emplacement,2 : rotation,
    # 3: value de reverse, 4: emplacement de l'image de fond associées)

else:
    image1 = PhotoImage(file="HT/500x350/Tangram.gif")
    image2 = PhotoImage(file="HT/500x350/main.gif")
    image3 = PhotoImage(file="HT/500x350/Jouer.gif")
    image4 = PhotoImage(file="HT/500x350/Crédits.gif")
    image5 = PhotoImage(file="HT/500x350/Quitter.gif")
    image6 = PhotoImage(file="HT/500x350/end.gif")
    image7 = PhotoImage(file="HT/500x350/reco.gif")
    image8 = PhotoImage(file="HT/500x350/quitter_end.gif")
    # importation des images qui dépendent des de la résolution (le fond des fenètres)
    T_fen = 500
    T_fen2 = 350
    T_fen_end = 150
    T_fen_end2 = 105
    # configuration de la taille des fenètres principales et de la fenetre de fin de jeu
    cote = 100
    # taille du coté principal des éléments du tangram
    xbtn = 205
    ybtn = 126
    xbtn1 = 200
    ybtn1 = 188
    xbtn2 = 200
    ybtn2 = 245
    xres = 3
    yres = 70
    xby = 90
    yby = 69
    # configuration des emplacements des différents boutons qui dépendent de la résolution contenue dans les fenêtres
    carre = [[(204.5, 1.0), (154.0, -49.5), (128.5, 26.0), (179.0, 51.5), (129.0, 0.5), (154.0, 26.5), (116.0, -17.0)],
             [0, 18, 18, 6, 12, 3, 6], False]
    canard = [[(-80.5, -10.5), (-80.0, -10.5), (-131.0, -45.5), (-192.0, 5.0), (-30.0, 15.0), (-167.0, 30.5),
               (-154.5, -12.5)], [0, 12, 15, 12, 6, 3, 6], False, "HT/500x350/canard.gif"]
    prosterne = [[(-115.0, 13.0), (-77.0, 9.0), (-146.0, -10.5), (-152.0, 14.0), (-43.0, -53.5), (-19.5, -12.5),
                  (-159.5, -27.5)], [16, 13, 13, 19, 16, 2, 1], False, "HT/500x350/prosterne.gif"]
    lapin = [[(-140.5, -57.5), (-125.5, -22.0), (-126.5, 64.0), (-100.0, -40.5), (-125.0, -15.0), (-108.0, 29.5),
              (-99.0, 68.5)], [3, 0, 21, 0, 12, 0, 4], False, "HT/500x350/lapin.gif"]
    figure = [[(-111.5, 8.0), (-120.0, -55.5), (-114.0, 69.0), (-142.5, 13.0), (-161.0, 16.5), (-109.5, -19.5),
               (-92.0, 65.5)], [15, 9, 0, 12, 9, 3, 9], True, "HT/500x350/figure.gif"]
    # tableaux contenant toutes les informations pour la réalisation des niveaux ( 1 : emplacement,2 : rotation,
    # 3: value de reverse, 4: emplacement de l'image de fond associée)


# Fin de l'initialisation de la fenêtre

lab0 = Label(fen, image=image1)
# Ce label contient l'image de fond ( la première de l'animation)
btn = Button(lab0, text="Jouer", command=Tangram, image=image3)
btn1 = Button(lab0, text="Crédits", command=lambda: os.system("gedit Crédits.txt"), image=image4)
btn2 = Button(lab0, text="Quitter", command=fen.quit, image=image5)
# Création de 3 boutons permettant de jouer au tangram, de quitter le jeu ou d'afficher dans gedit le fichier crédits.txt

posx = fen.winfo_screenwidth()
posy = fen.winfo_screenheight()
# récupération de la position de la fenêtre ( ne marche que sous linux )
diffx = T_fen
diffy = T_fen2
x = (posx / 2) - (diffx / 2)
y = (posy / 2) - (diffy / 2)
fen.geometry('%dx%d+%d+%d' % (diffx, diffy, x, y))
# centrage de la fenêtre

lab0.pack(side='top', fill='both', expand='yes')
# affichage du fond

fen.after(2500, lambda: [lab0.configure(image=image2),
                         btn.place(x=xbtn, y=ybtn),
                         btn1.place(x=xbtn1, y=ybtn1),
                         btn2.place(x=xbtn2, y=ybtn2)]
          )
# après 2,5 seconde, on change l'image de fond et on affiche les boutons configurés plus haut, cette ligne permet de
# créer l'animation du début

fen.mainloop()
fen.destroy()
# on entre dans la boucle principale et on détruit la fenêtre principale si l'on en sort.

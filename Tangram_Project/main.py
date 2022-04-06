#! /usr/bin/python
# -*- coding: utf-8 -*-
from turtle import *
from tkinter import *
from random import randrange
import os
import pickle

# Fonctions
from math import sqrt


def distance(p1, p2):
    """Cette fonction calcule la distance entre deux points p1, p2 assimilables à des tuples"""
    dist = sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))
    return dist


def geometry_fenetre(_fen: Tk | Toplevel, _diff_x, _diff_y):
    _pos_x, _pos_y = _fen.winfo_screenwidth(), _fen.winfo_screenheight()
    _x = int((_pos_x / 2) - (_diff_x / 2))
    _y = int((_pos_y / 2) - (_diff_y / 2))
    _fen.geometry(f'{_diff_x}x{_diff_y}+{_x}+{_y}')


def fin_niveau_tangram():
    fen3 = Toplevel()
    fen3.title("Bravo !")

    fond = Label(fen3, image=image6)
    # Initialisation d'une fenêtre qui a un fond que l'on affiche grâce à un label
    #  (qui est ici une image)
    res = Button(fond, image=image7, command=lambda: [restart(),
                                                      fen3.destroy()
                                                      ]
                 )
    by = Button(fond, image=image8, command=fen.quit)

    # création d'un bouton recommencer et d'un bouton quitter (qui quitte le jeu entièrement)

    fond.pack()
    res.place(x=xres, y=yres)
    by.place(x=xby, y=yby)
    geometry_fenetre(fen3, T_fen_end, T_fen_end2)
    # affichage et centrage de la fenêtre.


def detection_fin():
    """Cette fonction détecte si le niveau est terminé ou non"""
    test = True
    # on initialise le test comme étant vrai, si l'une des conditions du niveau n'est pas remplie
    # il deviendra faux.
    for i, pt in enumerate(tabl_end):

        # premier test : les positions.
        if i == 0 or i == 1:
            if distance(tabl[i], pt) <= 5 or distance(tabl[1-i], pt) <= 5:
                d1 = distance(tabl[0], pt)
                d2 = distance(tabl[1], pt)
                if d1 < d2:
                    dict_piece['tri1'].goto(tabl_end[i])
                elif d1 - d2 < 5:
                    dict_piece['tri1'].goto(tabl_end[i])
                    dict_piece['tri2'].goto(tabl_end[i])
                else:
                    dict_piece['tri2'].goto(tabl_end[i])
            else:
                return
                # les deux grands triangles

        if i == 3 or i == 4:
            if distance(tabl[i], pt) <= 5 or distance(tabl[7-i], pt) <= 5:
                d1 = distance(tabl[3], pt)
                d2 = distance(tabl[4], pt)
                if d1 < d2:
                    dict_piece['tripe1'].goto(tabl_end[i])
                elif d1 - d2 < 5:
                    dict_piece['tripe1'].goto(tabl_end[i])
                    dict_piece['tripe2'].goto(tabl_end[i])
                else:
                    dict_piece['tripe2'].goto(tabl_end[i])
            else:
                return
                # les deux petits triangles

                # Ces 4 premiers tests sont plus complexes, car on ne sait pas quel triangle
                #  le joueur va choisir (2 emplacements pour chaque triangle).

        if i == 2 or i == 5 or i == 6:
            if distance(tabl[i], pt) <= 5:
                dict_piece[name_pieces[i]].goto(pt)
            else:
                return
                # le triangle moyen, le carré et le parallélogramme

                # Cette première partie fait donc en sorte qu'un élément a une distance < à 5
                #  de sa position finale se met à celle-ci

    for i, cpt in enumerate(comp):
        if i == 0 or i == 1:
            if cpt != comp_end[0] and cpt != comp_end[1]:
                return
        elif i == 3 or i == 4:
            if cpt != comp_end[3] and cpt != comp_end[4]:
                return
        elif i == 2 or i == 5 or i == 6:
            if cpt != comp_end[i]:
                return
    # deuxième test qui regarde si la rotation des éléments est la bonne

    if reverse != reverse_end:
        return
    # Dernier test vérifiant si le parallélogramme doit ou non être inversé

    s1.update()

    if not test:  # on ne peut pas arriver là normalement
        return
    # le test est vrai, annonçons-le au joueur
    fin_niveau_tangram()


def restart():
    """Cette fonction permet de recommencer un niveau"""

    global comp, tabl, reverse, helped
    # récupération des variables à modifier en tant que variable globale

    tabl = list(carre[0])
    comp = list(carre[1])
    reverse = carre[2]
    # modification (ou création) du tableau de position et du tableau de rotation courant
    #  ainsi que de la variable indiquant si le parallélogramme est inversé
    helped = 2
    # la variable helped est remise à deux pour pouvoir réutiliser l'aide ( voir fonction see())
    init()
    # appel de la fonction init pour que les changements prennent effets


def init():
    """Initialise les éléments avec leur position et rotation respective

    Celles-ci sont dans comp et tabl"""

    for i, name in enumerate(name_pieces):
        dict_piece[name].up()

        dict_piece[name].shape(name if name != 'para' else 'para1')

        dict_piece[name].seth(comp[i] * 15)
        dict_piece[name].goto(tabl[i])
    color_init()
    # appel de la fonction color_init pour récupérer et afficher les couleurs des éléments


def color_init():
    """Met à jour la couleur des éléments du tangram

    (permet au joueur de personnaliser son jeu)"""
    for i, name in enumerate(name_pieces):
        dict_piece[name].color(l_color[i].get())

    s1.update()


def sav_color():
    """Récupère et sauvegarde dans un fichier les couleurs choisies
    par le joueur pour son tangram"""
    global l_color
    with open("sav_color.txt", "wb") as sauvegarde_couleur:
        sav = pickle.Pickler(sauvegarde_couleur)
        for col in l_color:
            sav.dump(col.get())


def sav_res(res):
    """Change la résolution par défaut par celle sélectionnée par le joueur
     et la place dans le fichier qui est lu au démarrage du jeu
      pour initialiser les fenêtres"""
    with open("sav_res.txt", "wb") as saved_resolution:
        sav = pickle.Pickler(saved_resolution)
        sav.dump(res)

    advise = Toplevel()
    redem = Label(advise, text="Vous devez relancer l'application"
                               " pour que les changements prennent effet !")
    btn_quit = Button(advise, text="Fermer l'application", command=fen.quit)
    redem.pack()
    btn_quit.pack()

    geometry_fenetre(advise, 500, 50)
    # création et centrage d'une fenêtre demandant au joueur de redémarrer l'application
    #  pour que les changements prennent effet


l_seuil_rotation = [24, 24, 24, 24, 24, 6, 12]


def rotation_i(i_):
    """Fonction de rotation pour dict_piece[name_pieces[i_]]"""
    def aux(x, y):
        comp[i_] += 1
        comp[i_] %= l_seuil_rotation[i_]
        dict_piece[name_pieces[i_]].seth(comp[i_] * 15)
        s1.update()
    return aux


l_rotations = [rotation_i(i) for i in range(7)]

# Les 6 fonctions rotations sont nécessaires, car on ne peut pas récupérer l'objet curseur actif
# au moment du clic. De plus, une fonction lambda ne peut pas recevoir d'argument ce qui rend son
# utilisation avec onclick impossible.
# Ces dernières mettent aussi à jour la table des rotations (comp)


def reverse_para(event):
    """Récupère la forme de l'objet C_para et lui assigne sa forme symétrique"""
    global reverse

    forme = dict_piece['para'].shape()
    if forme == "para1":
        reverse = True
        dict_piece['para'].shape("para2")
    if forme == "para2":
        reverse = False
        dict_piece['para'].shape("para1")
    s1.update()


def where(event):
    """Cette fonction met à jour la table des positions (tabl)"""
    for i, name in enumerate(name_pieces):
        tabl[i] = dict_piece[name].position()

    detection_fin()
    # lance la fonction détection pour voir si le tangram est terminé


def level(lvl):
    """Cette fonction configure le jeu pour afficher le niveau choisi par l'utilisateur"""
    global tabl_end, comp_end, reverse_end

    tabl_end = lvl[0]
    comp_end = lvl[1]
    reverse_end = lvl[2]
    bgc = lvl[3]
    s1.bgpic(bgc)
    # mise de tabl_end comp_end et reverse_end qui sont utilisées dans detection
    # et mise à jour du fond d'écran

    restart()


def see():
    """Cette fonction permet au joueur d'obtenir de l'aide si le joueur en demande"""
    global helped

    helped -= 1
    # on décrémente helped (appelé en global) car l'aide est limitée à deux par jeu

    if helped >= 0:
        # si le joueur à droit à un peu d'aide, on l'aide
        curseur = [dict_piece[name] for name in name_pieces]
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
            if reverse != canard[3] \
                    and (curseur[j].shape() == "para1" or curseur[j].shape() == "para2"):
                reverse_para(False)
        if fond == "HT/1000x700/lapin.gif" or fond == "HT/500x350/lapin.gif":
            curseur[j].goto(lapin[0][j])
            curseur[j].seth(lapin[1][j] * 15)
            tabl[j] = lapin[0][j]
            comp[j] = lapin[1][j]
            if reverse != lapin[3] \
                    and (curseur[j].shape() == "para1" or curseur[j].shape() == "para2"):
                reverse_para(False)
        if fond == "HT/1000x700/prosterne.gif" or fond == "HT/500x350/prosterne.gif":
            curseur[j].goto(prosterne[0][j])
            curseur[j].seth(prosterne[1][j] * 15)
            tabl[j] = prosterne[0][j]
            comp[j] = prosterne[1][j]
            if reverse != prosterne[3] \
                    and (curseur[j].shape() == "para1" or curseur[j].shape() == "para2"):
                reverse_para(False)
        if fond == "HT/1000x700/figure.gif" or fond == "HT/500x350/figure.gif":
            curseur[j].goto(figure[0][j])
            curseur[j].seth(figure[1][j] * 15)
            tabl[j] = figure[0][j]
            comp[j] = figure[1][j]
            if reverse != figure[3] \
                    and (curseur[j].shape() == "para1" or curseur[j].shape() == "para2"):
                reverse_para(False)
                # pour le niveau courant, on met le curseur tiré au hasard à sa place
                # on le tourne correctement et on met à jour la table des positions et des rotations
                # si le curseur tiré est dict_piece['para'],
                # on regarde en plus s'il doit être retourné
                # et on lance la fonction reverse_para qui se charge de mettre à jour reverse
    else:
        fen4 = Toplevel()
        attention = Label(fen4, text="Attention vous avez utilisé l'aide trop de fois ! ")
        btn_ok = Button(fen4, text="OK", command=fen4.destroy)
        attention.pack()
        btn_ok.pack()

        geometry_fenetre(fen4, 300, 50)

        # Si le joueur a utilisé deux fois l'aide, on lui signale à l'aide d'une fenêtre
        #  qu'il ne peut plus utiliser cette fonction pour le moment.

    s1.update()


name_pieces = ['tri1', 'tri2', 'trimoy', 'tripe1', 'tripe2', 'carre', 'para']


def tangram():
    """Cette fonction est le cœur du programme elle gère le tangram même"""
    # Init
    global s1, helped, dict_piece, l_color

    fen2 = Toplevel()
    # Création d'une nouvelle fenêtre
    cv1 = Canvas(fen2, width=T_fen, height=T_fen2)
    s1 = TurtleScreen(cv1)
    p = RawTurtle(s1)
    # Création d'un canvas Tkinter dans lequel on crée un écran turtle et un premier curseur nommé p
    dict_piece = {name: RawTurtle(s1) for name in name_pieces}
    # création des curseurs qui seront les éléments du Tangram

    cv1.pack()
    # affichage du canvas(et donc de l'écran turtle)
    l_color = []
    for i in range(7):
        l_color.append(StringVar())
    # création des objets qui contiendront les couleurs des curseurs,
    # On utilise ici des objets pour permettre la mise à jour simple des couleurs
    # grâce à des radiobutton

    with open("sav_color.txt", "rb") as sauvegarde_couleur:
        color_val = pickle.Unpickler(sauvegarde_couleur)
        for i in range(7):
            # lecture des couleurs sauvegardées par le joueur dans le fichier sav_color.txt
            color_set[i] = color_val.load()
            # assignation des chaînes contenant le nom des couleurs aux objets créés plus tôt
            l_color[i].set(color_set[i])

    # Nous allons à présent créer le menu qui est situé en haut de la fenêtre de jeu
    menu1 = Menu(fen2)

    fichier = Menu(menu1, tearoff=0)
    menu1.add_cascade(label="Fichier", menu=fichier)
    fichier.add_command(label="Recommencer", command=restart)
    # la commande Fichier/recommencer permet au joueur de remettre son niveau à 0
    # grâce à la fonction restart
    options = Menu(fichier, tearoff=0)
    fichier.add_cascade(label="Options", menu=options)
    color = Menu(options, tearoff=1)
    options.add_cascade(label="Couleur", menu=color)
    list_menus = [Menu(options, tearoff=0) for _ in range(7)]
    # ici nous allons définir un menu pour chaque élément du tangram qui permetra au joueur
    # de personnaliser les couleurs de son jeu qui sont automatiquement mises à jour
    # grâce à la fonction color_init()

    liste_init = [["Triangle 1", list_menus[0], l_color[0]],
                  ["Triangle 2", list_menus[1], l_color[1]],
                  ["Triangle Moyen", list_menus[2], l_color[2]],
                  ["Petit Triangle 1", list_menus[3], l_color[3]],
                  ["Petit Triangle 2", list_menus[4], l_color[4]],
                  ["Carre", list_menus[5], l_color[5]],
                  ["Parallélogramme", list_menus[6], l_color[6]]]
    liste_init_color = [["Rouge", "red"], ["Bleu", "blue"], ["Vert", "green"], ["Jaune", "yellow"],
                        ["Rose", "pink"], ["Violet", "purple"], ["Noir", "black"],
                        ["Blanc", "white"], ["Orange", "orange"], ["Bleu Ciel", "skyblue"],
                        ["Or", "gold"], ["Marron", "brown"]]

    for i in liste_init:
        color.add_cascade(label=i[0], menu=i[1])
        for j in liste_init_color:
            i[1].add_radiobutton(label=j[0], value=j[1], variable=i[2], command=color_init)

    color.add_separator()

    def apply_color_default():
        for i in range(7):
            l_color[i].set(color_default[i])
        color_init()

    color.add_command(label="Défaut", command=apply_color_default)
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
    # affiche dans gedit le fichier comment_jouer.txt

    bonus = Menu(menu1, tearoff=0)
    menu1.add_cascade(label="Bonus", menu=bonus)
    bonus.add_command(label="Taquin", command=lambda: os.system("python Taquin/taquin.py"))
    bonus.add_command(label="Allumettes",
                      command=lambda: os.system("python Allumettes/allumettes.py"))
    # permet de lancer les scripts contenant les jeux bonus : le jeu d'Allumette et le Taquin

    fen2.config(menu=menu1)
    # affectation du menu à notre fenêtre de jeu

    geometry_fenetre(fen2, T_fen, T_fen2)
    # centrage de la fenêtre de jeu

    p._tracer(8, 25)
    # configure la vitesse de tracer du curseur p
    # de façon à ce que l'on ne remarque pas l'initialisation des curseurs

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

    # pour créer les curseurs on enregistre une forme que l'on dessine avec le curseur p
    # puis on l'enregistre en tant que shape pour notre écran turtle

    # Corps

    level(canard)
    # on choisit le niveau par défaut

    # le jeu est prêt on fait donc un restart pour que l'initialisation se termine
    # et que le joueur puisse commencer la partie
    restart()

    for i, name in enumerate(name_pieces):
        dict_piece[name].onclick(l_rotations[i], btn=3)

        dict_piece[name].ondrag(dict_piece[name].goto)
    # initialisation des bindings pour que le joueur puisse faire tourner l'élément et le déplacer

    cv1.bind("<ButtonRelease-1>", where)
    cv1.bind("<Double-Button-1>", reverse_para)
    # 2 derniers binds pour metre à jour tabl
    # et pour permettre au joueur de faire le symétrique du parallélogramme

    s1.listen()
    # il ne reste plus qu'à attendre un évènement


# Création des premières variables : les couleurs, les couleurs par défaut
# et le nombre d'aides disponibles

color_set = color_default = ["brown", "purple", "pink", "yellow", "blue", "red", "green"]

helped = 2

# Première fenêtre

fen = Tk()
fen.title("Tangram Project")

# Initialisation de la résolution

with open("sav_res.txt", "rb") as saved_resolution:
    res_val = pickle.Unpickler(saved_resolution)
    res = res_val.load()
# lecture dans sav_res.txt de la résolution du programme (par défaut 1000x700)


image1 = PhotoImage(file=f"HT/{res}/Tangram.gif")
image2 = PhotoImage(file=f"HT/{res}/main.gif")
image3 = PhotoImage(file=f"HT/{res}/Jouer.gif")
image4 = PhotoImage(file=f"HT/{res}/Crédits.gif")
image5 = PhotoImage(file=f"HT/{res}/Quitter.gif")
image6 = PhotoImage(file=f"HT/{res}/end.gif")
image7 = PhotoImage(file=f"HT/{res}/reco.gif")
image8 = PhotoImage(file=f"HT/{res}/quitter_end.gif")

if res == "1000x700":
    # importation des images qui dépendent de la résolution (le fond des fenêtres)
    T_fen = 1000
    T_fen2 = 700
    T_fen_end = 300
    T_fen_end2 = 210
    # configuration de la taille des fenêtres principales et de la fenêtre de fin de jeu
    cote = 200
    # taille du côté principal des éléments du tangram
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
    # configuration des emplacements des différents boutons
    # qui dépendent de la résolution contenue dans les fenêtres
    carre = [[(409.00, 2.00), (308.00, -99.00), (257.00, 52.00), (358.00, 103.00), (258.00, 1.00),
              (308.00, 53.00), (232.00, -34.00)], [0, 18, 18, 6, 12, 3, 6], False]
    canard = [
        [(-161.00, -21.00), (-160.00, -21.00), (-262.00, -91.00), (-384.00, 10.00), (-60.00, 30.00),
         (-334.00, 61.00), (-309.00, -25.00)], [0, 12, 15, 12, 6, 3, 6], False,
        f"HT/{res}/canard.gif"]
    prosterne = [
        [(-230.00, 26.00), (-154.00, 18.00), (-292.00, -21.00), (-304.00, 28.00), (-86.00, -107.00),
         (-39.00, -25.00), (-319.00, -55.00)], [16, 13, 13, 19, 16, 2, 1], False,
        f"HT/{res}/prosterne.gif"]
    lapin = [[(-281.00, -115.00), (-251.00, -44.00), (-253.00, 128.00), (-200.00, -81.00),
              (-250.00, -30.00),
              (-216.00, 59.00), (-198.00, 137.00)], [3, 0, 21, 0, 12, 0, 4], False,
             f"HT/{res}/lapin.gif"]
    figure = [
        [(-223.00, 16.00), (-240.00, -111.00), (-228.00, 138.00), (-285.00, 26.00),
         (-322.00, 33.00), (-219.00, -39.00),
         (-184.00, 131.00)], [15, 9, 0, 12, 9, 3, 9], True, "HT/1000x700/figure.gif"]
    # tableaux contenant toutes les informations pour la réalisation des niveaux
    # ( 1 : emplacement, 2 : rotation, 3 : valeur de reverse,
    #  4 : emplacement de l'image de fond associée)

elif res == "500x350":
    # import des images qui dépendent de la résolution (le fond des fenêtres)
    T_fen = 500
    T_fen2 = 350
    T_fen_end = 150
    T_fen_end2 = 105
    # configuration de la taille des fenêtres principales et de la fenêtre de fin de jeu
    cote = 100
    # taille du côté principal des éléments du tangram
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
    # configuration des emplacements des différents boutons
    # qui dépendent de la résolution contenue dans les fenêtres
    carre = [[(204.5, 1.0), (154.0, -49.5), (128.5, 26.0), (179.0, 51.5), (129.0, 0.5),
              (154.0, 26.5), (116.0, -17.0)],
             [0, 18, 18, 6, 12, 3, 6], False]
    canard = [[(-80.5, -10.5), (-80.0, -10.5), (-131.0, -45.5), (-192.0, 5.0), (-30.0, 15.0),
               (-167.0, 30.5), (-154.5, -12.5)],
              [0, 12, 15, 12, 6, 3, 6], False, f"HT/{res}/canard.gif"]
    prosterne = [[(-115.0, 13.0), (-77.0, 9.0), (-146.0, -10.5), (-152.0, 14.0), (-43.0, -53.5),
                  (-19.5, -12.5), (-159.5, -27.5)],
                 [16, 13, 13, 19, 16, 2, 1], False, f"HT/{res}/prosterne.gif"]
    lapin = [[(-140.5, -57.5), (-125.5, -22.0), (-126.5, 64.0), (-100.0, -40.5), (-125.0, -15.0),
              (-108.0, 29.5), (-99.0, 68.5)],
             [3, 0, 21, 0, 12, 0, 4], False, f"HT/{res}/lapin.gif"]
    figure = [[(-111.5, 8.0), (-120.0, -55.5), (-114.0, 69.0), (-142.5, 13.0), (-161.0, 16.5),
               (-109.5, -19.5), (-92.0, 65.5)],
              [15, 9, 0, 12, 9, 3, 9], True, f"HT/{res}/figure.gif"]
    # tableaux contenant toutes les informations pour la réalisation des niveaux
    # ( 1 : emplacement,2 : rotation, 3: value de reverse,
    # 4 : emplacement de l'image de fond associée)
else:
    raise ValueError("Seules les résolutions 1000x700 ou 500x350 sont prévues.")

# Fin de l'initialisation de la fenêtre

lab0 = Label(fen, image=image1)
# Ce label contient l'image de fond (la première de l'animation)
btn = Button(lab0, text="Jouer", command=tangram, image=image3)
btn1 = Button(lab0, text="Crédits", command=lambda: os.system("gedit Crédits.txt"), image=image4)
btn2 = Button(lab0, text="Quitter", command=fen.quit, image=image5)
# Création de 3 boutons permettant de jouer au tangram,
# de quitter le jeu ou d'afficher dans gedit le fichier crédits.txt

# récupération de la position de la fenêtre (ne marche que sous linux)
geometry_fenetre(fen, T_fen, T_fen2)
# centrage de la fenêtre

lab0.pack(side='top', fill='both', expand=1)
# affichage du fond

fen.after(2500, lambda: [lab0.configure(image=image2),
                         btn.place(x=xbtn, y=ybtn),
                         btn1.place(x=xbtn1, y=ybtn1),
                         btn2.place(x=xbtn2, y=ybtn2)]
          )
# après 2,5 secondes, on change l'image de fond et on affiche les boutons configurés plus haut,
#  cette ligne permet de créer l'animation du début

fen.mainloop()
fen.destroy()
# on entre dans la boucle principale et on détruit la fenêtre principale si l'on en sort.

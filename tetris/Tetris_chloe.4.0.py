# TETRIS.4.0  ###### vivement le 10.1 :-)
from tkinter import *
import time
from random import randint
import numpy as np

fen = Tk()
dl = 20  # elementary length of a square
terrain = Canvas(fen, width=10 * dl, height=21 * dl, bg="light yellow")
terrain.pack(anchor=CENTER)
terrain.update()


# VARIABLES

# Grille = np.zeros((21, 10), dtype='int')
# Grille[20] = 8


class Shape:
    """Describe a piece of the tetris game."""
    
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color

    def __str__(self):
        return f"Shape(\n{self.shape}, {self.color}\n)"

    def rotate_piece(self, k):
        """Rotate a piece `k` times."""
        mat = self.shape
        for _ in range(k):
            mat = np.flip(mat.T, 1)
        self.shape = mat


shape_list = [(np.array([[1, 0], [1, 0], [1, 0], [1, 0]]), 'red'),
              (np.array([[2, 2], [2, 2], [0, 0], [0, 0]]), "pink"),
              (np.array([[3, 0], [3, 0], [3, 3], [0, 0]]), "purple"),
              (np.array([[0, 4], [0, 4], [4, 4], [0, 0]]), "blue"),
              (np.array([[5, 0], [5, 5], [5, 0], [0, 0]]), "green"),
              (np.array([[0, 6], [6, 6], [6, 0], [0, 0]]), "brown"),
              (np.array([[7, 0], [7, 7], [0, 7], [0, 0]]), "orange")]


# FONCTIONS

def range_i_j(n, p):
    """Give two iterations on n and p nested."""
    for k in range(n*p):
        yield divmod(k, n)


def choose_piece():
    """Choose a random piece in the existing list"""
    a = randint(0, 6)
    return Shape(*shape_list[a])


def draw_square(c, i, j, color):
    """Draw a square of given color to given coordinates"""
    rec = terrain.create_rectangle((c - 1 + j) * dl, i * dl,
                                   (c + j) * dl, (i + 1) * dl, fill=color)
    return rec


# on cherche à faire une piece de la taille du terrain.
# puis la descendre dans le tableau jusqu'à plus possible...
# demander c avant la fonction
def descendre_piece(piece: Shape, grille, c):
    """Take down a piece"""
    M = np.zeros((21, 10), dtype='int')
    N = np.zeros((21, 10), dtype='int')
    mat = piece.shape
    n, p = mat.shape

    for i in range(n):
        for j in range(p):  # création de la pièce géante
            if 9 >= c-1 + j >= 0:  # si ce 'if' n'est pas respecté,
                # alors des zéros débordent, pas de souci
                if mat[i][j] == 0:
                    M[i][c - 1 + j] = 0
                else:
                    M[i][c - 1 + j] = draw_square(c, i, j, piece.color)
    # si M*T=O la piece peut descendre dans le tableau sinon message d'erreur -1
    if (M * grille).any():
        return -1
    else:
        piece_geante = np.array(M)  # la matrice M est intacte
        while (piece_geante * grille == N).all():
            M = np.array(piece_geante)
            # print(M + T)
            piece_geante = np.zeros((21, 10), dtype='int')
            for s in range(20):
                piece_geante[s + 1] = M[s]
                for i in range(10):
                    if M[s][i] != 0:
                        terrain.move(M[s][i], 0, dl)
            time.sleep(0.02)
            terrain.update()
    return M + grille


def supprimer_lignes(grille):
    """Remove filled lines"""
    # supprime les lignes pleines et ajoute une ligne de 0 au-dessus
    T = grille
    J = np.zeros((1, 10), dtype='int')

    def aux(i_line):
        if 0 in T[i_line]:
            return False
        return True

    for i in range(0, 20):
        if aux(i):
            l_to_erase = []
            for j in range(10):
                a = T[i][j]
                if a not in l_to_erase:
                    l_to_erase.append(a)
            for rec in l_to_erase:
                terrain.delete(rec)
            for k in range(i):
                for j in range(10):
                    a = T[k][j]
                    if a != 0:
                        terrain.move(a, 0, dl)
            T = np.delete(T, i, axis=0)
            T = np.insert(T, 0, J, axis=0)
    return T


def is_piece_in_grid(c, mat):
    """Check if the piece is within the grid"""
    n, p = mat.shape
    if c + p - 1 > 10:
        for i in range(n):
            for j in range(c+p-1 - 10, p):
                if mat[i][j] != 0:
                    return False
    elif c <= 0:
        for i in range(n):
            for j in range(0, 1 - c):
                if mat[i][j] != 0:
                    return False
    return True


def tetris():
    grille = np.zeros((21, 10), dtype='int')
    grille[20] = 8
    print("Si vous voulez quitter, taper 'quit()' ")
    while (grille[0] == 0).any():  # tant que nous pouvons insérer une piece
        piece = choose_piece()
        print(grille)
        print("\nSi vous voulez quitter, taper 'quit()' \n")
        print('voici la piece:')
        print(piece)
        k = input('\ncombien de fois voulez vous tourner la piece: ')
        if k == "quit()":
            print("Good bye! See you soon!")
            print("\nConfirm quit with <Return>")
            _ = input()
            fen.quit()
            break
        k = int(k)
        piece.rotate_piece(k)
        print(piece)
        ok = False
        c = None
        while not ok:
            c = input('quelle colonne: ')
            if c == "quit()":
                print("\nGood bye! See you soon!")
                print("\nConfirm quit with <Return>")
                c = input()
                fen.quit()
                return
            c = int(c)
            ok = is_piece_in_grid(c, piece.shape)
            if not ok:
                print("la pièce sort de la grille, désolé ...", c, "ne marche pas")

        grille = descendre_piece(piece, grille, c)

        if type(grille) != np.ndarray:
            print("Who could win this game??")
            print("\nConfirm quit with <Return>")
            c = input()
            fen.quit()
            break
        grille = supprimer_lignes(grille)


tetris()

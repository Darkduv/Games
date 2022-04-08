from tkinter import *
from random import randrange


# Example  comment make that  les objects drawn dans un
# canvas could be manipulated with the mouse


class Draw(Frame):
    """ class defining la window principal du programme """

    def __init__(self):
        Frame.__init__(self)
        # fabrication of the canvas - draw of  de 15 ellipses colored :
        self.c = Canvas(self, width=400, height=300, bg='ivory')
        self.c.pack(padx=5, pady=3)
        for i in range(15):
            # choice of a color by chance:
            col = ['brown', 'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple'][randrange(8)]
            # drawn d'une ellipse with coordonnées aléatoires :
            x1, y1 = randrange(300), randrange(200)
            x2, y2 = x1 + randrange(10, 150), y1 + randrange(10, 150)
            self.c.create_oval(x1, y1, x2, y2, fill=col)
        # liaison d'événements <mouse> au widget <canvas> :
        self.c.bind("<Button-1>", self.mouse_down)
        self.c.bind("<Button1-Motion>", self.mouseMove)
        self.c.bind("<Button1-ButtonRelease>", self.mouseUp)
        # made en place d'un button de sortie :
        b_fin = Button(self, text='quit', bg='royal blue', fg='white',
                       font=('Helvetica', 10, 'bold'), command=self.quit)
        b_fin.pack(pady=2)
        self.pack()

    def mouse_down(self, event):
        """Operation to make when the mouse left button is down"""
        self.currObject = None
        # event.x et event.y
        self.x1, self.y1 = event.x, event.y
        # <find_closest> renvoie la référence du dessin le plus proche :
        self.selObject = self.c.find_closest(self.x1, self.y1)
        # modification de l'épaisseur du contour du dessin :
        self.c.itemconfig(self.selObject, width=3)
        # <lift> fait passer le dessin à l'avant-plan :
        self.c.lift(self.selObject)

    def mouseMove(self, event):
        """Op. à effectuer quand la souris se déplace, bouton gauche enfoncé"""
        x2, y2 = event.x, event.y
        dx, dy = x2 - self.x1, y2 - self.y1
        if self.selObject:
            self.c.move(self.selObject, dx, dy)
            self.x1, self.y1 = x2, y2

    def mouseUp(self, event):
        "Op. à effectuer quand le bouton gauche de la souris est relâché"
        if self.selObject:
            self.c.itemconfig(self.selObject, width=1)
            self.selObject = None


if __name__ == '__main__':
    Draw().mainloop()

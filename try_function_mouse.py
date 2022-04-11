from tkinter import *
from random import randrange


# Example of how to make the objects drawn in a canvas could be manipulated with the mouse


class Draw(Frame):
    """ class defining la window principal du programme """
    l_colors = ['brown', 'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple']

    def __init__(self):
        Frame.__init__(self)
        # fabrication of the canvas - draw of  de 15 ellipses colored :
        self.c = Canvas(self, width=400, height=300, bg='ivory')
        self.c.pack(padx=5, pady=3)
        for i in range(15):
            # choice of a color by chance:
            col = self.l_colors[randrange(8)]
            # drawn d'une ellipse with coordonnées aléatoires :
            x1, y1 = randrange(300), randrange(200)
            x2, y2 = x1 + randrange(10, 150), y1 + randrange(10, 150)
            self.c.create_oval(x1, y1, x2, y2, fill=col)
        # ### liaison d'événements <mouse> au widget <canvas> :
        self.c.bind("<Button-1>", self.mouse_down)
        # when the mouse moves while button1 is pressed :
        self.c.bind("<Button1-Motion>", self.mouse_move)
        self.c.bind("<Button1-ButtonRelease>", self.mouse_up)
        # made en place d'un button de sortie :
        b_fin = Button(self, text='Quit', bg='royal blue', fg='white',
                       font=('Helvetica', 10, 'bold'), command=self.quit)
        b_fin.pack(pady=2)
        self.pack()

        self.selObject = None
        self.x1 = None
        self.y1 = None

    def mouse_down(self, event):
        """Operation to make when the mouse left button is down"""
        # event.x et event.y
        self.x1, self.y1 = event.x, event.y
        # <find_closest> returns the reference of the closest drawn object :
        self.selObject = self.c.find_closest(self.x1, self.y1)
        # Changing the thickness of the drawing outline
        self.c.itemconfig(self.selObject, width=3)
        # <lift> brings the drawing to the forefront :
        self.c.lift(self.selObject)

    def mouse_move(self, event):
        """Move the selected object following the mouse"""
        x2, y2 = event.x, event.y
        dx, dy = x2 - self.x1, y2 - self.y1
        if self.selObject:
            self.c.move(self.selObject, dx, dy)
            self.x1, self.y1 = x2, y2

    def mouse_up(self, event):
        """Deselect the object"""
        if self.selObject:
            self.c.itemconfig(self.selObject, width=1)
            self.selObject = None
            self.x1 = None
            self.y1 = None


if __name__ == '__main__':
    Draw().mainloop()

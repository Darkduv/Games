"""Example of how the objects drawn in a canvas
 could be manipulated with the mouse"""

import tkinter
from random import randrange


class Draw(tkinter.Frame):
    """Main window of the program"""
    l_colors = ['brown', 'red', 'orange', 'yellow',
                'green', 'cyan', 'blue', 'purple']

    def __init__(self):
        tkinter.Frame.__init__(self)

        # making the parameters storing data on the selected object :
        self.sel_object = None
        self.x1 = None
        self.y1 = None

        # Making the canvas
        self.c = tkinter.Canvas(self, width=400, height=300, bg='ivory')
        self.c.pack(padx=5, pady=3)
        self.fill_init_canvas()
        # ### Binding <mouse> events to the widget <canvas>:
        self.c.bind("<Button-1>", self.mouse_down)
        # when the mouse moves while button1 is pressed :
        self.c.bind("<Button1-Motion>", self.mouse_move)
        self.c.bind("<Button1-ButtonRelease>", self.mouse_up)

        # making an exit button:
        b_fin = tkinter.Button(self, text='Quit', bg='royal blue', fg='white',
                               font=('Helvetica', 10, 'bold'),
                               command=self.quit)
        b_fin.pack(pady=2)

        self.pack()

    @classmethod
    def rand_color(cls):
        """Gives a randomly chosen color from the list"""
        index = randrange(len(cls.l_colors))
        return cls.l_colors[index]

    def fill_init_canvas(self, nb=15):
        """Fill the canvas with `nb` randomly made ellipses"""
        for _ in range(nb):
            # Choosing a random color:
            col = self.rand_color()
            # Drawing an ellipse with random coordinates
            x1, y1 = randrange(300), randrange(200)
            x2, y2 = x1 + randrange(10, 150), y1 + randrange(10, 150)
            self.c.create_oval(x1, y1, x2, y2, fill=col)

    def mouse_down(self, event: tkinter.Event):
        """Operation to make when the mouse left button is down"""
        self.x1, self.y1 = event.x, event.y
        # <find_closest> returns the reference of the closest drawn object :
        # it returns an int but in a tuple : (int,).
        self.sel_object, = self.c.find_closest(self.x1, self.y1)
        # Changing the thickness of the drawing outline
        self.c.itemconfig(self.sel_object, width=3)
        # <lift> brings the drawing to the forefront :
        self.c.lift(self.sel_object)

    def mouse_move(self, event):
        """Move the selected object following the mouse"""
        if not self.sel_object:
            return
        x2, y2 = event.x, event.y
        dx, dy = x2 - self.x1, y2 - self.y1
        self.c.move(self.sel_object, dx, dy)
        self.x1, self.y1 = x2, y2

    def mouse_up(self, _: tkinter.Event):
        """Deselect the object"""
        if not self.sel_object:
            return
        self.c.itemconfig(self.sel_object, width=1)
        self.sel_object = None
        self.x1 = None
        self.y1 = None


if __name__ == '__main__':
    Draw().mainloop()

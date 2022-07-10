"""Try creating a resizing canvas"""

import tkinter


class ResizingCanvas(tkinter.Canvas):
    """A subclass of Canvas for dealing with resizing of windows"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        w_scale = float(event.width) / self.width
        h_scale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale(tkinter.ALL, 0, 0, w_scale, h_scale)


def main():
    root = tkinter.Tk()
    my_frame = tkinter.Frame(root)
    my_frame.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    my_canvas = ResizingCanvas(my_frame, width=850, height=400, bg="red",
                               highlightthickness=0)
    my_canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    # add some widgets to the canvas
    my_canvas.create_line(0, 0, 200, 100)
    my_canvas.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))
    my_canvas.create_rectangle(50, 25, 150, 75, fill="blue")

    def undo(_: tkinter.Event):
        print("undo undo undo undo")

    root.bind("<Control-u>", undo)
    root.mainloop()


if __name__ == "__main__":
    main()

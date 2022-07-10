"""Test/Example using canvas"""
import tkinter

root = tkinter.Tk()
drawing_zone = tkinter.Canvas(root, width=500, height=500)
drawing_zone.pack()
drawing_zone.create_line(0, 0, 500, 500)
drawing_zone.create_rectangle(490, 200, 500, 100)
drawing_zone.create_text(100, 100, text="hello")

# Oval inscribed in the rectangle whose x1, y1, x2, y2 are given
drawing_zone.create_oval(400, 400, 300, 300, outline="gray",
                         width=1, fill="#%02x%02x%02x" % (255, 3, 77))
# Example of drawing a polygon: the coordinates of the points must be given
drawing_zone.create_polygon(100, 200, 200, 200, 250, 290, 200, 380,
                            100, 380, 50, 290,
                            outline="red", width=2, fill="yellow")


def quit_(event):
    """Destroy the canvas and the 'root', if the top arrow is pressed"""
    if event.keysym == "Up":
        drawing_zone.destroy()
        root.destroy()


exit_button = tkinter.Button(root, text="Exit", command=root.destroy)
exit_button.pack()

drawing_zone.focus_set()
drawing_zone.bind("<Up>", quit_)
drawing_zone.pack()

root.mainloop()

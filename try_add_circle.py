from tkinter import *

racine = Tk()
zone_dessin = Canvas(racine, width=500, height=500)
zone_dessin.pack()
zone_dessin.create_line(0, 0, 500, 500)
zone_dessin.create_rectangle(490, 200, 500, 100)
zone_dessin.create_text(100, 100, text="hello")


# zone_dessin.create_oval(100, 100, 200, 200, outline ="grey",
#                                      width =1, fill =[255,3,77])
# zone_dessin.create_polygon(100,100,200,100,250,190,200,280,100,280,50,190, outline="red", width=2, fill= "yellow")


def qzuit(event):
    if event.keysym == "Up":
        zone_dessin.destroy()
        racine.destroy()


bouton_sortir = Button(racine, text="Sortir", command=racine.destroy)
bouton_sortir.pack()

zone_dessin.focus_set()
zone_dessin.bind("<Up>", qzuit)
zone_dessin.pack()

racine.mainloop()

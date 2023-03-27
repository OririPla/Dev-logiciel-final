
from tkinter import *
from tkinter import ttk
import  tkinter as tk

from PIL import Image, ImageTk



fen1 = Tk()
width= fen1.winfo_screenwidth()
height= fen1.winfo_screenheight()
fen1.geometry("%dx%d" % (width, height))
label = ttk.Label(fen1, text="Bonjour et bienvenue, logiciel de déposition de plainte par portrait robot. Nous allons  vous montrer des photos et vous en choisirez certaines" )
label.pack()


load = Image.open("IMG/000010.jpg")
render = ImageTk.PhotoImage(load)

img = Label(fen1, image=render)
img.image = render
img.pack()

#b1=button = tk.Button(fen1, image=im4)
#b1.pack(side = LEFT, padx=10)

fen1.mainloop()

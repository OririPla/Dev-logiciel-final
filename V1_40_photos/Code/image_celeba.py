from tkinter import *
from tkinter import ttk
import  tkinter as tk

from PIL import Image, ImageTk


class image_celeba :
    def __init__(self, afilename, anumber, matrix, P):
        self.filename_jpg=afilename
        
        self.number=anumber
        self.matrix=matrix
        self.P=P
        self.im = Image.open(self.filename_jpg)

    # methode nécessaire ?
    def get_filename_jpg(self):
        return self.filename_jpg

    def RESIZING (self,x,y): 
        #resize image and keep ratio
        self.im.thumbnail((x, y))
        #self.im.save('resized_'+self.filename_jpg)
        self.im.save(self.filename_jpg)


#main
"""
fen1 = Tk()
width= fen1.winfo_screenwidth()
height= fen1.winfo_screenheight()
fen1.geometry("%dx%d" % (width, height))
fen1.title("test")


label = ttk.Label(fen1, text="Bonjour et bienvenue, logiciel de déposition de plainte par portrait robot. Nous allons  vous montrer des photos et vous en choisirez certaines" )
label.pack()

#creation image olivetti
test_img=image_celeba("IMG/000010.jpg", 1)
test_img_resized=test_img.RESIZING(110,110)
#peut que diminuer
print(test_img.filename_jpg)


render = ImageTk.PhotoImage(test_img.im)

#img = Label(fen1, image=render)
#img.image = render
#img.pack()

b1 = tk.Button(fen1, image=render)
b1.pack()

fen1.mainloop()

"""
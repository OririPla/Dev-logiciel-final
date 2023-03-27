 #####    PREMIERE FENETRE    ######

from tkinter import *
from tkinter import ttk
import  tkinter as tk

import A2_photo_win as p 

import webbrowser
from PIL import ImageTk, Image

from PIL import Image

class first_win:
    def __init__(self, string_titre):
        self.win = Tk()
        width= self.win.winfo_screenwidth()
        height= self.win.winfo_screenheight()
        self.win.geometry("%dx%d" % (width, height))
        self.win.title(string_titre)
        
        self.label1 = ttk.Label( self.win, text="Bonjour et bienvenue, logiciel de déposition de plainte par portrait robot." )
        self.label1.pack(pady=100)

        self.label2 = ttk.Label( self.win, text="Nous allons  vous montrer des photos et vous pourrez en choisirez une ou deux." )
        self.label2.pack(pady=10)

        self.button1 = ttk.Button( self.win, text="Commencer",
                                   command=self.start )
        self.button1.pack(pady=100)

        image_insa=tk.PhotoImage(file='IMG/resized_logo_INSA.png')
        self.button_web = tk.Button(self.win, image=image_insa, command=self.lien_insa)
        self.button_web.pack(padx=100)

        self.win.mainloop()
    
    def lien_insa(self):
        webbrowser.open('https://www.insa-lyon.fr')

    def close_win(self):

        self.win.destroy()
   
    def start( self ):
        #commande qui ouvre deuxieme fenetre et ferme première
        self.close_win()
        #p.photo_win("Fenetre avec photos et  Algorithme")
        print( "starting" )
 
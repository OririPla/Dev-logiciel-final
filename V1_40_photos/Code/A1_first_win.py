 #####    PREMIERE FENETRE    ######

from tkinter import *
from tkinter import ttk
import  tkinter as tk

import A2_photo_win as p 

import webbrowser

from PIL import Image


class first_win:
    def __init__(self, string_titre):
        self.fen1 = Tk()
        width= self.fen1.winfo_screenwidth()
        height= self.fen1.winfo_screenheight()
        self.fen1.geometry("%dx%d" % (width, height))
        self.fen1.title(string_titre)
        
        self.label = ttk.Label( self.fen1, text="Bonjour et bienvenue, logiciel de déposition de plainte par portrait robot." )
        self.label.pack(pady=100)

        self.label = ttk.Label( self.fen1, text="Nous allons  vous montrer des photos et vous pourrez en choisirez une ou deux." )
        self.label.pack(pady=10)

        self.button1 = ttk.Button( self.fen1, text="Commencer",
                                   command=self.start )
        self.button1.pack(pady=100)
        self.fen1.mainloop()
        

    def close_win(self):
        self.fen1.destroy()
   
    def start( self ):
        #commande qui ouvre deuxieme fenetre et ferme première
        self.close_win()
        p.photo_win("Fenetre avec photos et  Algorithme")
        print( "starting" )
 
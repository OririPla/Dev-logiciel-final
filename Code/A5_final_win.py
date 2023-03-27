
from tkinter import *
from tkinter import ttk
import  tkinter as tk


class final_win:
    def __init__(self):
        self.win = Tk()
        width= self.win.winfo_screenwidth()
        height= self.win.winfo_screenheight()
        self.win.geometry("%dx%d" % (width, height))
        self.win.title("FINAL")
        
        self.label_1 = ttk.Label(self.win, text="C'est la fin du logiciel. On espère que tout s'est déroulé comme vous le souhaitiez. licence.. remerciements.. souhaitez vous  refaire ?" )
        self.label_1.pack(pady=20)
        
      
        Button(self.win,text='Oui ', command= self.reponse_oui).pack()
        
        exit_button = Button(self.win, text="Non et quitter logiciel", command=self.win.destroy)
        exit_button.pack(pady=30)
        
        self.win.mainloop()

    def close_win(self):
        #self.win.destroy()
        self.close_win()
        
    def reponse_oui( self ):
        #commande qui reouvrivra au début
        self.close_win()
        print( "re-starting" )



#MAIN

#final_win()

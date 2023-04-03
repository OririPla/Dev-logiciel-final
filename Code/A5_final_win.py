
from tkinter import *
from tkinter import ttk
import  tkinter as tk

import A1_first_win as f

class final_win:
    """
    A class to represent the final window of the application.
    Attributes:
        win (Tk) :
            The Tkinter root window for the application.
        label_1 (Tkinter.ttk.Label) :
            The label widget for instructions.
    """
    def __init__(self):
        """
        Initializes the final_win object and creates the GUI
        """
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
        """
        Closes the final window.
        """
        self.close_win()
        
    def reponse_oui( self ):
        """
        Handles the affirmative "Oui" button and restarts the application
        """
        
        print( "re-starting" )
        f.first_win("Recommencer")
        self.close_win()


 #####    MAIN    ######

#final_win()

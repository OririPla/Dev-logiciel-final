#####    FIRST WINDOW    ######

from tkinter import *
from tkinter import ttk
import  tkinter as tk

import A2_photo_win as p 
import Tuto as t

import webbrowser
from PIL import ImageTk, Image

#Path
import pathlib
path=str(pathlib.Path(__file__).parent.resolve().parent.resolve())

class first_win:
    """
    Creates a GUI with a welcome message and a button to start using the application.
    This module uses the tkinter library to create a GUI with a label and a button. The label displays a welcome message to the user, while the button allows the user to start the application. When the button is clicked, it closes the current window and opens a second window.
    Attributes:
        win (Tk object) :
            The main window object.
        text (tkinter.StringVar) :
            The text shown in the window.
        label1 (ttk.Label) :
            A label object used to display a message in the window.
        label2 (ttk.Label) :
            A label object used to display a message in the window.
        button_tuto (ttk.Button) :
            A button to access to the tutorial
        button1 (ttk.Button) :
            A button to begin the program
        button_web (ttk.Button) :
            A button to access to the web site of INSA
    """
    def __init__(self, string_titre):
        """
        Constructs and initializes the GUI window with string_titre as its title.
        input :
            string_titre (str) :
                Name of the first window
        """
        self.win = Tk()
        width= self.win.winfo_screenwidth()
        height= self.win.winfo_screenheight()
        self.win.geometry("%dx%d" % (width, height))
        self.win.title(string_titre)

        self.label1 = ttk.Label( self.win, text="Bonjour et bienvenue dans ce logiciel de déposition de plainte par portrait robot." )
        self.label1.pack(pady=100)

        self.label2 = ttk.Label( self.win, text="Nous allons vous montrer des photos et vous pourrez en choisir une ou plusieurs." )
        self.label2.pack(pady=10)

        self.button_tuto = ttk.Button( self.win, text="Tutoriel pour comprendre le logiciel",
                                   command=self.tuto )
        self.button_tuto.pack(pady=100)

        self.button1 = ttk.Button( self.win, text="Commencer",
                                   command=self.start )
        self.button1.pack(pady=100)

        image_insa=tk.PhotoImage(file=path+'/IMG/resized_logo_INSA.png')
        self.button_web = tk.Button(self.win, image=image_insa, command=self.lien_insa)
        self.button_web.pack(padx=100)

        self.win.mainloop()
    
    def tuto(self):
        """
        Add a button to a link to the tutoriel (explication of how works the logiciel).
        """
        t.tutoriel()
        

    def lien_insa(self):
        """
        Add a logo INSA that allows to access to a web site.
        """
        webbrowser.open('https://www.insa-lyon.fr')

    def close_win(self):
        """
        Destroys the GUI window.
        """
        self.win.destroy()
   
    def start( self ):
        """
        Closes the current window and opens a second window.
        """
        self.close_win()
        p.photo_win("Fenetre avec photos et  Algorithme")
        #print( "starting" )
 

#####    MAIN test  ######
#first_win("test")
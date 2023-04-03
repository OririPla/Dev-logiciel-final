from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

import  tkinter as tk

import time

class loading_win:
    """
    Creates an intermediate window when the program is running but when there are no results yet
    Attributes:
        win (Tk object) :
            The main window object.
        label_load (ttk.Label) :
            A label object used to display a message in the window.
        Progress_Bar (ttk.Label) :
            A label object used to display a loading bar
    """    
    def __init__(self):
        """
        Initializes the window and creates the widgets.
        """
        self.win = Tk()
        self.win.geometry("600x250")
        self.win.eval('tk::PlaceWindow . center')
        self.win.title("Chargement")
        
        self.label_load = ttk.Label(self.win, text="Chargement en cours..." )
        self.label_load.pack(pady=20)
        
   
        self.Progress_Bar=Progressbar(self.win,orient=HORIZONTAL,length=250,mode='determinate')
        self.Progress_Bar.pack(pady=10)
        
        test=4
        Button(self.win,text='Run', command=lambda: self.Slide(test)).pack(pady=10)
        
        self.win.mainloop()

    def close_win(self):
        """
        Destroys the current window
        """
        self.win.destroy()

    def Slide(self, number):
        """
        Update the Progress_Bar to show how progress the program
        input :
            number (int) : 
                The number of options to choose from.
        """
        self.Progress_Bar['value']=20
        self.win.update_idletasks()
        time.sleep(1)
        self.Progress_Bar['value']=50
        self.win.update_idletasks()
        time.sleep(1)
        self.Progress_Bar['value']=80
        self.win.update_idletasks()
        time.sleep(1)
        self.Progress_Bar['value']=100    
        time.sleep(1)
        self.label_load.config(text = "Chargement terminé !")
        time.sleep(1)
        self.close_win()
    
     
#####    MAIN test  ######
#first = loading_window()
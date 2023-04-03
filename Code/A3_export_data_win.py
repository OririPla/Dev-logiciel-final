from tkinter import *
from tkinter import ttk
import  tkinter as tk
from PIL import Image,  ImageTk

### CLASS IMPORTATION
import A4_pdf_win as p

class export_data_win:
    """
    A class to create a window for exporting data, with an image and two buttons.

    Methods:
        __init__(self, choosen_photo): Initializes the export_data_win class
        close_win(self): Closes the export_data_win window
        reponse_oui(self): Closes the current window and opens a new one for exporting data

    Attributes:
        choosen : str
            The file path of the chosen photo.
        win : Tkinter.Tk
            The window object.
        label_1 : Tkinter.ttk.Label
            The label widget for instructions.

    """

    def __init__(self, choosen_photo):
        """
        Initializes the export_data_win class.

        input :
            self(export_data_win)
            choosen_photo: A PhotoImage object representing the chosen photo to display.
        output :

        """

        print(choosen_photo)
        self.choosen=choosen_photo
        self.win = Tk()
        width= self.win.winfo_screenwidth()
        height= self.win.winfo_screenheight()
        self.win.geometry("%dx%d" % (width, height))
        self.win.title("Processus terminé, Photo finale ")
        self.label_1 = ttk.Label(self.win, text="Votre portrait robot est finalisé, vous pouvez le visualiser ci-dessous." )
        self.label_1.pack()


        im1=ImageTk.PhotoImage(self.choosen)
        lab_image = tk.Label(image=im1)
        #self.b1 = tk.Button(self.can1, image=self.im1, command=lambda: self.choice(0))
        #self.b1.pack(side = LEFT, padx=10)

        #img_choisie = tk.PhotoImage(file=self.im)
        lab_image.pack()


        self.label_proposition = ttk.Label(self.win, text="Souhaitez-vous enregistrer vos données ?" )
        self.label_proposition.pack(pady=100)


        Button(self.win,text='Oui ', command= self.reponse_oui).pack()

        exit_button = Button(self.win, text="Non et quitter logiciel", command=self.win.destroy)
        exit_button.pack(pady=30)

        self.win.mainloop()

    def close_win(self):
        """
        Closes the export_data_win window.

        input :
            self(export_data_win)

        output :

        """
        self.win.destroy()

    def reponse_oui(self):
        """
        Closes the current window and opens a new one for exporting data.

        input :
            self(export_data_win)

        output :

        """

        self.close_win()
        p.pdf_win(self.choosen)
        print( "starting" )


#export_data_win()

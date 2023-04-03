from tkinter import *
from tkinter import ttk
import  tkinter as tk
from PIL import Image,  ImageTk

### CLASS IMPORTATION
import A4_pdf_win as p
import image_celeba as i

class export_data_win:
    """
    A class to create a window for exporting data, with an image and two buttons.
    Attributes:
        choosen (str):
            The file path of the chosen photo.
        win (Tkinter.Tk):
            The window object.
        label_1 (Tkinter.ttk.Label):
            The label widget for instructions.
    """
    def __init__(self, choosen_photo):
        """
        Initializes the export_data_win class.
        input:
            choosen_photo (image_celeba) : a image_celeba object linked to the chosen photo to display.
        """
        self.choosen=choosen_photo
        self.win = Tk()
        width= self.win.winfo_screenwidth()
        height= self.win.winfo_screenheight()
        self.win.geometry("%dx%d" % (width, height))
        self.win.title("Processus terminé, photo finale ")
        self.label_1 = ttk.Label(self.win, text="Votre portrait robot est finalisé, vous pouvez le visualiser ci-dessous." )
        self.label_1.pack()

    
        im1=ImageTk.PhotoImage(self.choosen.im)
        lab_image = tk.Label(image=im1)
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
        """
        self.win.destroy()
        
    def reponse_oui( self ):
        """
        Closes the current window and opens a new one for exporting data.
        """
        self.close_win()
        print("filename =", self.choosen.filename_jpg)
        p.pdf_win(self.choosen.filename_jpg)


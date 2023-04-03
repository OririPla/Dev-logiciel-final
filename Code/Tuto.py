from tkinter import *
from tkinter import ttk
import  tkinter as tk

#Path
import pathlib
path=str(pathlib.Path(__file__).parent.resolve().parent.resolve())


from PIL import ImageTk, Image

class tutoriel:
    """
    This class create a tutorial to explain to the user how to use the logiciel
    Attributes:
        win (Tk object) :
            The main window object
        image_list (list(ImageTk)) :
            List of the images used for the tutorial
        counter (int) :
            It allows to display the number of the page of the tutorial that is looked by the visualiser
        tuto_end (ttk.Button) :
            A button that leads direct to the end of the tutorial
        imageLabel (ttk.Label) :
            Display the legend of the image
        infoLabel (ttk.Label) :
            Display the information about what show the image
    """
    def __init__(self):
        self.win = Tk()
        width= self.win.winfo_screenwidth()
        height= self.win.winfo_screenheight()
        self.win.geometry("550x750")
        self.win.title("Tutoriel")


        # set up the images
        image1 = ImageTk.PhotoImage(Image.open(path+"/IMG/tuto/Ima_tuto_1.png").resize((600, 350)), master=self.win)
        image2 = ImageTk.PhotoImage(Image.open(path+"/IMG/tuto/Ima_tuto_2.png").resize((600, 350)), master=self.win)
        image3 = ImageTk.PhotoImage(Image.open(path+"/IMG/tuto/Ima_tuto_3.png").resize((600, 350)), master=self.win)
        image4 = ImageTk.PhotoImage(Image.open(path+"/IMG/tuto/Ima_tuto_4.png").resize((600, 350)), master=self.win)
        image5 = ImageTk.PhotoImage(Image.open(path+"/IMG/tuto/Ima_tuto_5.png").resize((600, 350)), master=self.win)
        image6 = ImageTk.PhotoImage(Image.open(path+"/IMG/tuto/Ima_tuto_6.png").resize((600, 350)), master=self.win)
        # add them to the list
        self.image_list = [image1, image2, image3, image4, image5,image6]
        # counter integer
        self.counter = 0

        # change image function
        self.tuto_end= ttk.Button( self.win, text="Quitter",command=self.close_win )
        self.tuto_end.pack(side="bottom", pady=10)

        # set up the components
        self.imageLabel = Label(self.win, image=image1)
        self.infoLabel = Label(self.win, text="Explication 1 sur 5", font="Helvetica, 20")
       
        button_f = Button(self.win, text="Suivant --> ", width=15, height=2, command=lambda: self.ChangeImage(1))
        button_r = Button(self.win, text="<-- Précédent", width=15, height=2, command=lambda: self.ChangeImage(-1))
        # display the components
        self.imageLabel.pack()
        self.infoLabel.pack()        
        button_r.pack(side=LEFT, padx=30)
        button_f.pack(side=RIGHT, padx=30)


        self.win.mainloop()


    def close_win(self):
        """
        Closes the tutorial window.
        """
        self.win.destroy()

    def ChangeImage(self, infos_avance_retour):
        """
        Enables the user to change the displayed image explanation by pressing a forward or reverse button
        """
        self.counter += infos_avance_retour
        if self.counter > len(self.image_list) - 1:
            self.counter = 0            
        if self.counter < 0:
            self.counter = len(self.image_list) - 1    
            
        self.imageLabel.config(image=self.image_list[self.counter])
        self.infoLabel.config(text="Explication " + str(self.counter + 1) + " sur " + str(len(self.image_list)))


#####    MAIN    ######

#tutoriel()
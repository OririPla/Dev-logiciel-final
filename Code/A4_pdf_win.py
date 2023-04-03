### MODULES IMPORTATION
from tkinter import *
from tkinter import ttk
import  tkinter as tk

from fpdf import FPDF
from datetime import datetime

from PIL import Image, ImageTk

#Path
import pathlib
path=str(pathlib.Path(__file__).parent.resolve().parent.resolve())


### CLASS IMPORTATION
import A5_final_win as f
import image_celeba as imc

class pdf_win:
    """
    A class that generates a window to obtain input from the user and generate a PDF file.
    Attributes:
        choosen_photo (str) :
            The file path of the chosen photo.
        win (Tkinter.Tk) :
            The window object.
        label_1 (Tkinter.ttk.Label) :
            The label widget for instructions.
        lname_entry (Tkinter.Entry) :
            The entry widget for last name input.
        fname_entry (Tkinter.Entry) :
            The entry widget for first name input.
        date_entry (Tkinter.Entry) :
            The entry widget for date of birth input.
        recap (Tkinter.Label) :
            The label widget for showing the user input.
        b_gen_pdf (Tkinter.Button) :
            The button widget to generate PDF.
        T (str) :
            A string that holds the formatted user input.
        t (list of str) :
            A list of strings that holds the unformatted user input.
    """

    def __init__(self, choosen_photo_name):
        """
        Initializes the class by creating the window and widgets
        input:
            choosen_photo_name (str):
                The file path of the chosen photo
        """
        self.win = Tk()
        width= self.win.winfo_screenwidth()
        height= self.win.winfo_screenheight()
        self.win.geometry("%dx%d" % (width, height))
        self.win.title("Exporter vos données")
        self.photo_name=choosen_photo_name

        self.label_1 = ttk.Label(self.win, text="Renseigner vos informations :" )
        self.label_1.pack(pady=20)

        self.T=""
        self.t=""

        lname = Label(self.win, text = "Nom : ")
        lname.pack()
        self.lname_entry = Entry ( self.win, width= 22 )
        self.lname_entry.pack()

        #Prenom
        fname = Label(self.win, text = "Prénom : ")
        fname.pack()
        self.fname_entry = Entry ( self.win, width= 22)
        self.fname_entry.pack()

        #Date
        date=Label(self.win, text = "Date de naissance (jj/mm/aaaa): ")
        date.pack()
        self.date_entry = Entry(self.win, width= 22)
        self.date_entry.pack()


        #Create a Button to get the input data
        ttk.Button(self.win, text= "Entrer", command= self.get_data).pack()


        #Inititalize a Label widget
        self.recap= Label(self.win, text="", font=('Helvetica 14'))
        self.recap.pack()
        self.b_gen_pdf=Button(self.win,text='Générer PDF ', command= self.validate)


        self.win.mainloop()


    def get_data(self) :
        """
        Retrieves the user input and formats it into a string to show to the user
        """

        self.t=["VOICI LE RECAPITULATIF DE VOS INFORMATIONS :", "Nom : ", self.lname_entry.get(), "Prénom : ", self.fname_entry.get(), "Date de naissance : ", self.date_entry.get(), "Si les informations ci-dessus sont correctes, vous pouvez valider. \n Sinon, vous pouvez encore les modifier et appuyer à nouveau sur entrer."," Les informations seront générées sous format PDF avec pour nom de fichier : Finalinfos.pdf "]
        self.T=self.t[0]+"\n \n" + self.t[1]+self.t[2]+"\n"+self.t[3]+self.t[4]+"\n"+ self.t[5]+self.t[6]+"\n\n\n\n"+self.t[7]+"\n"+self.t[8]
        # print(self.t)
        self.recap.config(text=self.T, font= ('Helvetica 14'))
        self.b_gen_pdf.pack()

    def close_win(self):
        """
        Destroys the window
        """
        self.win.destroy()

    def validate(self):
        """
        Generates the pdf, retrieves the information and opens the last window of gratitudes.
        """
        #Creation of the pdf
        monPdf = FPDF()
        monPdf.add_page()
        monPdf.set_font("Arial", size=12)

        monPdf.cell(200, 10, txt="Rapport Final", border = 1, ln=1, align="C", fill = False)
        monPdf.set_font("Times", "B", size=20)
        monPdf.cell(0, 80, "Portrait simulé du sujet observé en activité criminelle.", ln=1, align="C")
        monPdf.image(self.photo_name, x=85, y = 92.5)

        monPdf.set_font("Times", "I", size=20)
        monPdf.cell(0, 100, txt=self.t[0], ln=1, align="C")

        for i in range(1,7):
            monPdf.set_font('Arial', '', 16)
            monPdf.cell(0,10, txt = self.t[i], ln=1, align="C")
            monPdf.ln(1)

        
        

    

        monPdf.output(path+"infos.pdf")

        self.close_win()
        f.final_win()
        print( "PDF généré" )



#####    MAIN test   ######
#first = pdf_win()

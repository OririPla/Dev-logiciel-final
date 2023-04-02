### MODULES IMPORTATION
from tkinter import *
from tkinter import ttk
import  tkinter as tk

from fpdf import FPDF
from datetime import datetime

from PIL import Image, ImageTk


### CLASS IMPORTATION
import A5_final_win as f

class pdf_win:
    
    def __init__(self, choosen_photo):
        self.win = Tk()
        self.choosen=choosen_photo
        width= self.win.winfo_screenwidth()
        height= self.win.winfo_screenheight()
        self.win.geometry("%dx%d" % (width, height))
        self.win.title("Exporter vos données")
        
        self.label_1 = ttk.Label(self.win, text="Renseigner vos informations :" )
        self.label_1.pack(pady=20)
        
        self.T=""
        self.t=""
        #Nom
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
        self.recap= Label(self.win, text="", font=('Helvetica 13'))
        self.recap.pack()
        self.b_gen_pdf=Button(self.win,text='Générer PDF ', command= self.validate)
        
        self.win.mainloop()


    def get_data(self) :
        #list de texte pour eviter les acolades
        self.t=["VOICI LE RECAPITULATIF DE VOS INFORMATIONS :", "Nom : ", self.lname_entry.get(), "Prénom : ", self.fname_entry.get(), "Date de naissance : ", self.date_entry.get(), "Si les informations ci-dessus sont correctes, vous pouvez valider. \n Sinon, vous pouvez encore les modifier et appuyer à nouveau sur entrer."," Les informations seront générées sous format PDF avec pour nom de fichier : infos.pdf "]
        self.T=self.t[0]+"\n \n" + self.t[1]+self.t[2]+"\n"+self.t[3]+self.t[4]+"\n"+ self.t[5]+self.t[6]+"\n\n\n\n"+self.t[7]+"\n"+self.t[8]
        self.recap.config(text=self.T, font= ('Helvetica 13'))
        #afficher le button aussi
        self.b_gen_pdf.pack()
        
    def close_win(self):
        self.win.destroy()
            
    def validate( self ):
        #génère le pdf et ouvre derniere fenetre de remerciements

        #Création de ma page PDF
        monPdf = FPDF()
        monPdf.add_page()
        monPdf.set_font("Arial", size=10)

        #Image_choisie=Image.open(self.choosen)
        #monPdf.image(Image_choisie, x = 85, y = 32.5, type = '', link = '')

        #Récupère les informations
        monPdf.cell(200, 10, txt="Final Report", ln=1, align="C")
        monPdf.cell(0, 100, txt=self.t[0], ln=1, align="C")
        
        for i in (1,6):
            monPdf.cell(0,10, txt=self.t[i], ln=1, align="C")
            monPdf.ln(1)
       

        monPdf.output("infos.pdf")
        


        self.close_win()
        f.final_win()
        print( "PDF généré" )



### MAIN

#first = pdf_win()


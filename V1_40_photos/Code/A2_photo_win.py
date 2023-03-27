from tkinter import *
from tkinter import ttk
import  tkinter as tk
from tkinter.messagebox import *

import A2_loading_win as l
import A3_export_data_win as e

import webbrowser

from PIL import ImageTk, Image

import Algo_main_CelebA as a
import  image_celeba as imc

    #####     FENETRES avec PHOTOS    ######
class photo_win:

    def __init__(self, string_titre):
        self.fen1 = Tk()
        self.width= self.fen1.winfo_screenwidth()
        self.height= self.fen1.winfo_screenheight()
        self.fen1.geometry("%dx%d" % (self.width, self.height))
        self.fen1.title(string_titre)

        self.text=tk.StringVar()
        self.text.set("Choississez une image qui correspond en cliquant dessus.")
        self.label = ttk.Label( self.fen1, textvariable=self.text)
        self.label.pack(pady=10)

        self.label2 = ttk.Label(self.fen1, text="Si aucune image ne correspond ou que vous souhaitez recommencer, vous pouvez appuyez sur ce bouton pour obtenir 5 nouvelles photos de la base de données: " )
        self.label2.pack()
        end_button = Button(self.fen1, text="Ré-initialiser", command=self.reinitialise)
        end_button.pack()

        
        self.L_photos=[]
        self.L_photos=a.initialisation_Liste_5_premiers()

        self.can1 = Canvas(self.fen1,bg='white',height=400,width=self.width)
        self.can1.pack(pady=100)

        self.can2 = Canvas(self.fen1,height=600,width=self.width)
        self.can2.pack()

        self.chosen_number=0
        self.iteration =0
         ### pas utilisé ?
    
        #celeba
        self.mise_a_j_img()


        self.fen1.mainloop()
    
    def mise_a_j_img(self):
        # Créer les boutons avec les images
        #doit rajouter master=self.fen1 pour éviter problemes avec ma
        #pour éviter le pyimage doesn't exite sur la creation du bouton
        self.im1=ImageTk.PhotoImage(self.L_photos[0].im, master=self.fen1)
        self.im2=ImageTk.PhotoImage(self.L_photos[1].im, master=self.fen1)
        self.im3=ImageTk.PhotoImage(self.L_photos[2].im, master=self.fen1)
        self.im4=ImageTk.PhotoImage(self.L_photos[3].im, master=self.fen1)
        self.im5=ImageTk.PhotoImage(self.L_photos[4].im, master=self.fen1)

        self.b1 = tk.Button(self.can1, image=self.im1, command=lambda: self.choice(0))
        self.b1.pack(side = LEFT, padx=10)

        self.b2 = tk.Button(self.can1, image=self.im2, highlightcolor="green", highlightthickness=3, activebackground='green', command=lambda: self.choice(1))
        self.b2.pack(side = LEFT, padx=10)

        self.b3 = tk.Button(self.can1, image=self.im3, highlightcolor="green", highlightthickness=3, activebackground='green', command=lambda: self.choice(2))
        self.b3.pack(side = LEFT, padx=10)
    
        self.b4 = tk.Button(self.can1, image=self.im4, highlightcolor="green", highlightthickness=3, activebackground='green', command=lambda: self.choice(3))
        self.b4.pack(side = LEFT, padx=10)

        self.b5 = tk.Button(self.can1, image=self.im5, highlightcolor="green", highlightthickness=3, activebackground='green', command=lambda: self.choice(4))
        self.b5.pack(side = LEFT, padx=10)

    def reinitialise(self):
        for c in self.can1.winfo_children():
           c.destroy() 

        for c in self.can2.winfo_children():
           c.destroy() 
        self.L_photos=a.initialisation_Liste_5_premiers()
        self.mise_a_j_img()


    def close_win(self):
        self.fen1.destroy()

    def choice(self, number) :
        self.chosen_number=number
        print("you chose", self.chosen_number+1)
        for c in self.can2.winfo_children():
           c.destroy()

        texte_avec_numero=str("Vous avez choisi l'image "+ str(self.chosen_number+1) + " (entourée de vert). Voulez vous : ")
        self.label = ttk.Label(self.can2, text=texte_avec_numero )
        self.label.pack(pady=20)
        end_button = Button(self.can2, text="Générer d'autres photos à partir de celle choisie", command=self.generate_image)
        end_button.pack(pady=20)
        end_button = Button(self.can2, text="Valider cette photo comme photo finale", command=self.validate)
        end_button.pack()
        #l.loading_window()

    def generate_image(self):
        self.iteration+=1
        #algo génétique avec image numero self.a de la liste initiale    et   genere nouvelle liste :
        print("dans generate imgage :" + str(self.L_photos[self.chosen_number].number))
    
        self.L_photos=a.generate_5_new_photos(self.L_photos[self.chosen_number],  self.iteration)

        t="Choississez à nouveau l'image qui correspond le plus en cliquant dessus (itération : " + str(self.iteration) + " )"
        self.text.set(t)
        
        for c in self.can1.winfo_children():
           c.destroy() 

        for c in self.can2.winfo_children():
           c.destroy() 

        self.mise_a_j_img()
        

    def validate(self) :
        choice_final=askokcancel(title="Confirmation de validation", message="Etes-vous sur de vouloir choisir cette photo comme photo finale ? ")
        if choice_final :
            self.close_win()

            chosen_photo=self.L_photos[self.chosen_number].im
            e.export_data_win(chosen_photo)



 #####    MAIN    ######
"""
RESIZING("logo_INSA.png", 300,  300)
RESIZING("PNG.png", 300,  300)
"""


#test mise en commun
#liste des noms des photos créées en jpg
#les supprimer quand non  choisies  ?
#écrasée car même nom
#photo_win("test mise en commun")
from tkinter import *
from tkinter import ttk
import  tkinter as tk

from PIL import Image, ImageTk


class image_celeba :
    """
    A class to handle CelebA dataset images and resizing.
    Attributes:
        filename_jpg (str) :
            The path of the jpg file.
        number (int) :
            The number of the image in the dataset.
        matrix (list) :
            A 40x2 matrix of features.
        P (np.array) :
            The list of the images into their encoded form, so it's a list of vector
        im (PIL.Image) :
            The image object.
    """
    def __init__(self, afilename, anumber, matrix, P):
        """
        Initialisation of the object image_celeba
        input:
            afilename (str):
                The path of the jpg file.
            anumber (int) :
                The number of the image in the dataset.
            matrix (list) :
                A 40x2 matrix of features.
            P (np.array) :
                The list of the images into their encoded form, so it's a list of vector
        """
        self.filename_jpg=afilename
        self.number=anumber
        self.matrix=matrix
        self.P=P
        self.im = Image.open(self.filename_jpg)


    def RESIZING (self,x,y): 
        """
        Resize the image to fit in a (x,y) box and save the resized image.
        input:
            x (int) :
                The width of the box.
            y (int) :
                The height of the box.
        """
        #resize image and keep ratio
        self.im.thumbnail((x, y))
        #self.im.save('resized_'+self.filename_jpg)
        self.im.save(self.filename_jpg)


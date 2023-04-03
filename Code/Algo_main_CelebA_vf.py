# IMPORTATIONS
import numpy as np
import matplotlib
#mac
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from skimage import io, transform
from skimage.transform import resize


import os, time, sys, json, glob
import csv
import cv2
import math, random

from importlib import reload

import tensorflow as tf
from tensorflow import keras
from keras.models import Model
from keras.callbacks import TensorBoard
from keras import layers

#Path
import pathlib
path=str(pathlib.Path(__file__).parent.resolve().parent.resolve())

import image_celeba as ic

# DOWNLOAD THE DATASET
dataset_img=path+'/f_annexes/img_align_celeba_607'

# DOWNLOAD THE ATTRIBUTES OF THE IMAGES
def load_attr():
    """
    Create the liste of filesnames and sexe of the images
    output :
        sexe (list) :
            To use just some images at the start and not all images
        filesnames (list) :
            To give numerotation to the images
    """

    db=pd.read_csv(path+'/f_annexes/new_list_attr_celba.csv',sep=",",usecols=['nb_pic','Male'],low_memory=False)
    file=open(path+"/f_annexes/filesnames607.txt", "r")
    filesnames=[]
    for line in file :
        new=line.split('\n')
        filesnames.append(new[0])
    sexe=[]
    for i in range(len(filesnames)):
        sexe.append(int(db[db.nb_pic==filesnames[i]]["Male"]))
    return(list(sexe),filesnames)


def import_images(sexe,filesnames,nb_images = 607,start = 0):
    """
    Import images of the dataset. Import nb_images, strat with the images number start and take the same number of male and female.
    input :
        nb_images (int) :
            Number of images that we will use
        start (int) :
            To use just some images at the start and not all images
        sexe (list) :
            To know the sexe presented on the images
        filesnames (list) :
            To give numerotation to the images
    output :
        x_data (numpy array) :
            List of the images as np.array
    """
    dataset_img=path+'/f_annexes/img_align_celeba_607'
    x=[]
    compt_Male=0
    compt_Female=0
    for i in range(start,start+nb_images):
        # take into account the sexe to have the same number of male and female
        if sexe[i]==1:
            compt_Male+=1
            if compt_Male<=nb_images/2:
                image=io.imread(f'{dataset_img}/{filesnames[i]}') #download image
                image_resize=resize(image,(128,128)) #resize picture with size 128x128
                x.append(image_resize)
        else :
            compt_Female+=1
            if compt_Female<=nb_images/2:
                image=io.imread(f'{dataset_img}/{filesnames[i]}') #download image
                image_resize=resize(image,(128,128)) #resize picture with size 128x128
                x.append(image_resize)


    x_data=np.array(x) #transform list into numpy array
    x=None
    return(x_data)


# DOWNLOAD AUTOENCODER
autoencodeur=tf.keras.models.load_model(path+'/f_annexes/autoencodeurFLATTEN4.tf')
decodeur=autoencodeur.decoder
encodeur=autoencodeur.encoder


# ALGO GENETIQUE
def mutation_function_flatten(vec, lap) :
    """
    It includes modifications into one of the selected vectors (so into an image in the latent space),
    in order to move in the latent space. Thus creating some mutations to the previous face.
    The modification are random but depend of the lap : the more the lap is small, the more there are mutations
    input :
        vec (np.array) :
            One vector (that represents a face in the latent space)
        lap (int) :
            The number of laps already completed vector
    output :
        vec (np.array) :
            The vector after modifications
    """
    new_vec = vec.copy()
    n = len(vec)
    new_vec += np.random.randn(n).reshape(new_vec.shape)*(30-lap)*0.6

    return new_vec


def mutations_test(x_data) :
    """
    This method allow to check if the mutation_function_flatten works well.
    We plot an original face (randomly selected), then we plot its version after the VAE
    with which we will compare the result of the mutation_function_flatten.
    """
    i = random.randint(0,len(x_data))
    print("Num of the selected face : ", i)
    plt.figure(figsize=(10,2))

    img = x_data[i]
    plt.imshow(tf.squeeze(img))
    plt.title("origine")

    encoded_imgs=encodeur(x_data)
    img_2 = encoded_imgs[i]
    P = np.array([img_2])
    img_2 = decodeur.predict(P)
    plt.figure(figsize=(10,2))
    plt.imshow(tf.squeeze(img_2))
    plt.title("reconstructed")

    P_mut = np.array([mutation_function_flatten(P[0],lap = 0)])
    plt.figure(figsize=(10,2))
    img_3 = decodeur.predict(P_mut)
    plt.imshow(tf.squeeze(img_3))
    plt.title("mutation lap = 0")

    P_mut2 = np.array([mutation_function_flatten(P[0],lap = 25)])
    plt.figure(figsize=(10,2))
    img_4 = decodeur.predict(P_mut2)
    plt.imshow(tf.squeeze(img_4))
    plt.title("mutation lap = 25")

    plt.show()

# mutations_test(x_data)
# The face decoded is not well, so with the mutations, it does not look like a precised face.
# Nevertheless, we can see that the mutations according to the loop (lap) works quite well :
# there are much more mutations at lap = 0 than at lap = 25, that means that whenthe more the user use the software
# the more we reduce the possibilities of variations.


def crossing_over_function_flatten(r, selected_pop, lap) :
    """
    It includes crossing over in one of the selected vectors, in order to move in the latent space
    The crossing over is the exchange of some 'points' of the latent space between some vectors
    It depends of the selected vectors and of the lap
    input :
        r (int) :
            The indice of the selected vector (of the list selected_pop) with which we willd do the crossing-over
        selected_pop (np.array) :
            The vectors selected
        lap (int) :
            The number of laps already completed
    output :
        new_pop[r] (np.array) :
            The selected vector after the crossing over
    """

    new_pop = np.copy(selected_pop)
    shape = new_pop.shape

    if (shape[0] == 1) :
        print("Pas de crossing-over")
    else :
        for indc in range(0,shape[0]) : # each loop corresponds to a crossing over with the vector at indice "indc" in the selected_pop
            if indc != r :
                if lap < 10 :
                    i = 0
                    j = int(shape[1]/6) ; print("j",j)
                    for l in range(0, 3) :
                        # Positions in the selected vector (= selected_pop[r]) that will be exchanged :
                        pos_x1 = random.randint(i, i + j -1)
                        pos_x2 = random.randint(i, i + j -1)
                        # Values of the selected vector that will be exchanged with the vector at indice "indc" :
                        v_selected = selected_pop[r][min(pos_x1,pos_x2):max(pos_x1,pos_x2) + 1]
                        # We define a new vector cp (for copy) that takes all the values that will be exchanged (v_selected) of the vector at indice "indc"
                        cp = selected_pop[indc][min(pos_x1,pos_x2):max(pos_x1,pos_x2) + 1]
                        # We replace the values v_selected of the selected vector by the values cp of the vector at indice "indc"
                        new_pop[r][min(pos_x1,pos_x2):max(pos_x1,pos_x2) + 1] = cp
                        i += j ; print("i", i)
                else :
                    pos_x1 = random.randint(0, shape[1]-1)
                    pos_x2 = random.randint(0, shape[1]-1)
                    cp = selected_pop[indc][min(pos_x1,pos_x2):max(pos_x1,pos_x2) + 1]
                    new_pop[r][min(pos_x1,pos_x2):max(pos_x1,pos_x2) + 1] = cp
    return new_pop[r]

def initialisation_Liste_5_premiers():
    """
    Create a list of the initial images for x_data that will be printed in the
    screen and a list of the same images but into their encoded form (so as vectors)
    input :
    output :
        List_images (list(np.array)) :
            List of the initial images as object "image_celeba"
    """

    encoded_imgs=encodeur(x_data) # We use the encoded images (so the images in the latent space)
    initial_img=[] # the nb_faces first images used and then presented to the user are selected randoml among the nb_images selected encoded
    list_img_non_encoded =[]

    for i in range(nb_faces):
        r=random.randint(0,len(encoded_imgs))
        initial_img.append(encoded_imgs[r])
        list_img_non_encoded.append(x_data[r])

    P=np.array(initial_img)
    List_images=saving_images_and_getting_list_initial(P, list_img_non_encoded)

    return List_images


def saving_images_and_getting_list_initial(P, list_img_non_encoded):
    """
    Save the initial images passed in list_img_non_encoded in .jpg and return the
    list of the same images as object "image_celeba"
    input :
        P (np.array) : the initial images into their encoded form
        list_img_non_encoded (list) : the initial images into their form before the encoder
    output :
        List_images (list(np.array)) : list of the initial images as object "image_celeba"
    """

    List_images=[]
    plt.figure(figsize=(20, 4))
    for i in range(nb_faces):
        ##### Save the images into format jpg
        # Display reconstruction
        plt.clf()
        ax = plt.subplot(2, nb_faces, i + 1 + nb_faces)
        plt.imshow(tf.squeeze(list_img_non_encoded[i]))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        jpg_name=path+"/IMG/Celeb_"+str(i)+".jpg"
        plt.imsave(jpg_name, list_img_non_encoded[i])
        im=ic.image_celeba(jpg_name, i,P[i],P)

        List_images.append(im)

    return List_images

def saving_images_and_getting_list(P):
    """
    Save the selected images, passed into their encoded form in P, and return the
    list of the same images as object "image_celeba"
    input :
        P (np.array) : the selected images into their encoded form
    output :
        List_images (list(np.array)) : list of the selected images as object "image_celeba"
    """


    List_images=[]
    decoded_imgs = decodeur.predict(P)
    plt.figure(figsize=(20, 4))
    for i in range(nb_faces):
        ##### Save the images into format jpg
        # Display reconstruction
        plt.clf()
        ax = plt.subplot(2, nb_faces, i + 1 + nb_faces)
        plt.imshow(tf.squeeze(decoded_imgs[i]))
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        jpg_name=path+"/IMG/Celeb_"+str(i)+".jpg"
        plt.imsave(jpg_name, decoded_imgs[i])
        im=ic.image_celeba(jpg_name, i,P[i],P)
        List_images.append(im)
    return List_images

def generate_5_new_photos (img_list, img_number_choosen,lap):
    """
    Generated new nb_faces images, into their encoded, and return the
    list of the same images as object "image_celeba"
    input :
        img_list (list(image_celeba)) : list of the images as object "image_celeba" selected by the user
        img_number_choosen (list(int)) : indices of the selected images in the previous P list
        lap (int) : the number of laps already completed vector
    output :
        List_images (list(np.array)) : list of the selected images as object "image_celeba"
    """

    P=img_list[0].P # the list of the faces, into their encoded form, that were printed in the previous lap
    sorted_P = [] # the list of the faces, into their encoded form, that the will be selected by the user

    for a_number in img_number_choosen :
        sorted_P.append(P[a_number]) # we add the encoded form of the selected face. So now in sorted_P we have the vectors selected by the user

    l = len(sorted_P)
    print("You have selected : ",l, " faces.") # number of images selected by the user

    sorted_P = np.array(sorted_P) # # transformation of the list of the selected vectors (= selected images into their encoded form) into a np.array

    new_P = np.copy(P)
    for i in range(nb_faces) : # for each new face that the program will create the program apply the genetic algorithm
        r = random.randint(0, l-1) ; print("r : ",r) # selection of a selected vector (so one of the encoded images in the latent space),
        new_P[i] = mutation_function_flatten(sorted_P[r], lap) # the program does modifications on the selected vector
        new_P[i] = crossing_over_function_flatten(r, sorted_P, lap) # the program does crossing-over between with the selected vectors
    P = new_P # the program replace the old images (into their encoded form) by the new images form
    lap += 1
    print("lap=", lap)

    #saving the new photos
    List_new_images=saving_images_and_getting_list(P)

    return List_new_images



##### MAIN ######

# Parameters for initialisation (outisde functions)
nb_faces = 5 # nb of faces that we want print at each iteration
lap = 0 # lap counts the iterations
C = True # C is the condition to continue or not the iterations (if C == False : it is the end of the program)
a = "{}".format(nb_faces) # string version of the number of faces
#nb_images = 1000 # number of images that we will use for the program
sexes, filenames = load_attr() # download of information about the sexe of the people of the image and the name of the image
# start = random.randint(0,len(filenames) - 1001) # the position of the first image in the dataset (to have different faces at each use of the program)
start = 0 # by default
nb_images = 607
x_data = import_images(sexes, filenames, nb_images, start) # download of the images that we will use
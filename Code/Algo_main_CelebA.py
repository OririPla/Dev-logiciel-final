# IMPORTATIONS
# !pip install tensorflow
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


#to hide warning about tensorflow, hides but doens't rebuild
#but then also doen't hide 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import image_celeba as ic

# DOWNLOAD THE DATASET
dataset_img='IMG/img_align_celeba-2'

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))

        if img is not None:
            images.append(img)
    return images

filesnames=[]
with open('f_annexes/list_attr_celebra.txt',"r") as file:
    for line in file :
        per_line=line.split(" ")
        name=per_line[0]
        filesnames.append(name)
filesnames=filesnames[2:]

nb_images=1000

x=[]
for i in range(0,nb_images):
    image=io.imread(f'{dataset_img}/{filesnames[i]}')
    image_resize=resize(image,(128,128))
    x.append(image_resize)

x_data=np.array(x)
x=None


# DOWNLOAD AUTOENCODER

autoencodeur=tf.keras.models.load_model('f_annexes/autoencodeurNONFlatten3.tf')
decodeur=autoencodeur.decoder
encodeur=autoencodeur.encoder


# ALGO GENETIQUE
def cost_function(mx, mx_selected, lap):
    """
    Calculation of the cost of the matrix.
    The cost depends of the number of laps already completed and of difference
    between this matrix and the matrix selected by the user

    Args:
        mx(np.array) : the matrix for which we calculate its cost
        mx_selected(np.array): the matrix selected by the user
        lap(int): the number of laps already completed
    Return:
        cost(float) : the cost of the matrix
    """

    mx_dimensions = mx.shape
    cost = 0 ;
    for i in range(mx_dimensions[0]):
        for j in range(mx_dimensions[1]):
            for k in range(mx_dimensions[2]):
                cost += (25 - lap) * abs((mx_selected[i][j][k] - mx[i][j][k])) # arbitrary function

    return round(cost,2)

def sorted_pop(pop, mx_selected, lap):
    """
    To sort the population allows to form new matrices, so new faces.
    The sorting depends of the cost of each matrix

    Args:
        pop(np.array) : the list of the different matrices
        mx_selected(np.array): the matrix selected by the user
        lap(int): the number of laps already completed
    Return:
        sorted_pop : the matrices sorted by their cost
    """
    pop_cost = np.zeros(len(pop)) # cost of each matrix
    for i in range(len(pop)) :
        pop_cost[i] = cost_function(pop[i], mx_selected, lap)

    indices = np.argsort(pop_cost)
    sorted_pop = pop[indices]

    return sorted_pop

def mutation_function(mx, Tm, lap) :
    """
    It includes modifications in the selected matrix, in order to move in the latent space
    The modification is random but depends of the mutation rate (Tm) and of the lap

    Args:
        mx(np.array) : one matrix (that represents a face in the latent space)
        Tm(float) : the mutation rate is the probability that a 'point' in the matrix has to mute
        lap(int): the number of laps already completed
    Return:
        mx : the matrix after modifications
    """
    n,m,l = mx.shape
    M = mx.copy()
    for i in range (n):
        for j in range (m):
            for k in range (l):
                t = random.random()
                if t < Tm:
                    if t < Tm/2 :
                        a = round((mx[i][j][k] + (25 - lap)*0.01),3)
                        if a > 10 :
                            a = 10
                    else :
                        a = round((mx[i][j][k] - (25 - lap)*0.01),3)
                        if a < 0 :
                            a = 0
                    # print("i : ", i, "j : ", j, "a : ", (25 - 2*lap)*0.01)
                    M[i][j][k] = a
    return M

def crossing_over_function(sorted_pop, Tc, lap) :
    """
    It includes crossing over in the selected matrix, in order to move in the latent space
    The crossing over is the exchange of some 'points' of the latent space between some matrices
    It depends of the mutation rate (Tm), of the lap and of the order of the matrices according their cost

    Args:
        sorted_pop(np.array) : the matrices sorted by their cost
        Tc(float) : the crossing over rate is the probability that a serie of points in the matrix has to be exhanged
        lap(int): the number of laps already completed
    Return:
        mx : the matrix after modifications
    """

    new_pop = np.copy(sorted_pop)
    shape = new_pop.shape
    #print(shape)
    t = random.random()
    if t < Tc :

        # Index of the matrix (of the pop) with which the cross takes place
        if (lap >= 0 and lap < 5) :
            indc = random.randint(1, shape[0]-1)
        elif (lap >= 5 and lap < 10) :
            indc = random.randint(1, shape[0]-2)
        elif (lap >= 10 and lap < 15) :
            indc = random.randint(1, shape[0]-3)
        else :
            indc = 1

        for l in range(lap+1) :
            #print("A")
            #print("indc : ",indc)
            # Position in the mx_selected (= sorted_pop[0]) that will be exchanged :
            pos_x = random.randint(0, shape[1]-1) ; #print("X ",pos_x)
            pos_y = random.randint(0, shape[2]-1) ; #print("Y ",pos_y)
            pos_z = random.randint(0, shape[3]-1) ; #print("Z ",pos_z)
            # Values of mx_selected (that will be crossed) that will be exchanges :
            v_selected = sorted_pop[0][pos_x:shape[1]][0:(pos_y+1)][0:(pos_z+1)]
            #print("values_selected : ",v_selected)
            # We define a new mx cp that takes all the values of the mx at indice indc at the same position of v_selected
            cp = sorted_pop[indc][pos_x:shape[1]][0:(pos_y+1)][0:(pos_z+1)]
            #print("cp : ",cp)
            # We replace the values selected in mx_selected by this new mx cp
            new_pop[0][pos_x:shape[1]][0:(pos_y+1)][0:(pos_z+1)] = cp
            # In the mx indc, we exchange its values selected with the values of mx_selected saved in v_selected
            new_pop[indc][pos_x:shape[1]][0:(pos_y+1)][0:(pos_z+1)] = v_selected

    return new_pop[0]


def initialisation_Liste_5_premiers():
    rows = 32
    cols = 32
    width = 4
    nb_faces = 5
    Tm = 0.5
    Tc = 0.6
    lap = 0
    C = True # continue
    a = "{}".format(nb_faces - 1)
    #print(type(a))

    encoded_imgs=encodeur(x_data)
    initial_img=[]
    for i in range(nb_faces):
        initial_img.append(encoded_imgs[random.randint(0,len(encoded_imgs))])

    P=np.array(initial_img)

    List_images=saving_images_and_getting_list(P)

    return List_images


def saving_images_and_getting_list(P):
    nb_faces = 5
    List_images=[]
    decoded_imgs = decodeur.predict(P)
    plt.figure(figsize=(20, 4))
    for i in range(nb_faces):
        ##### enregistrer les images en format jpg
        # Display reconstruction
        plt.clf() ## clear le plot ?
        ax = plt.subplot(2, nb_faces, i + 1 + nb_faces)
        plt.imshow(tf.squeeze(decoded_imgs[i]))
        plt.title("reconstructed")
        plt.gray()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)   
        jpg_name="IMG/Test_Celeb_"+str(i)+".jpg"
        plt.imsave(jpg_name, decoded_imgs[i])
        im=ic.image_celeba(jpg_name, i,P[i],P)
        List_images.append(im)
        print(im.number)
        print(jpg_name)
        

    return List_images

def generate_5_new_photos (img_choosen,lap):
    rows = 32
    cols = 32
    width = 4
    nb_faces = 5
    Tm = 0.5
    Tc = 0.6
    C = True # continue
    a = "{}".format(nb_faces - 1)

    encoded_imgs=encodeur(x_data)

    #array of before, how to access ? global ?
    #P=np.array(List_img

    decoded_imgs = decodeur.predict(img_choosen.P)

    #nb = nombre image choisie commence à zero et a recuperer depuis l'interface
   
    nb=img_choosen.number
    print("algo generate:you choser image"+str(nb))
    vec_selected = img_choosen.matrix # the vector selected by the user

    sorted_P = sorted_pop(img_choosen.P, vec_selected, lap)
    new_P = np.copy(sorted_P)
    for i in range(nb_faces) :
        new_P[i] = mutation_function(vec_selected, Tm, lap)
        new_P[i] = crossing_over_function(sorted_P, Tc, lap)
    P = new_P

    #saving the new photos 
    List_new_images=saving_images_and_getting_list(P)
    
    return List_new_images



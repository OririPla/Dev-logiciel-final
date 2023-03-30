#### Import ####

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from skimage import io, transform
from skimage.transform import resize

import os, time, sys
import math, random

from importlib import reload

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import TensorBoard

from sklearn.model_selection import train_test_split

### Fonction definition ###

def load_attr():
    """
        Create the liste of filesnames and sexe of the images

        input :

        output :
            sexe (list)
            filesnames (list)

    """
    db=pd.read_csv('new_list_attr_celba.csv',sep=",",usecols=['nb_pic','Male'],low_memory=False)
    filesnames=list(db["nb_pic"])
    sexe=list(db['Male'])
    return(sexe,filesnames)


def retrain(sexe,filenames,nb_images,start,plot=0):
    """
        Fit the autoencodeur with nb_images new images, start with the start images of the dataset. Finally save the autoencodeur with the number num.

        input :
                sexe (list)
                filenames (list)
                nb_images (int)
                start (int)
                num (int)
                plot (int)

        output :

    """

    #Re-load the model to train it another time, we take another part of the dataset to do it
    #we can do it as many time as we want
    autoencoder_re=tf.keras.models.load_model(f'../modele_entraine/autoencodeur/autoencodeurFLATTEN.tf')
    x_data=import_images(nb_images,start,sexe,filenames)
    print("coucou")
    samples=[random.randint(0,len(x_data)-1) for i in range(32)]
    X_train, X_test = train_test_split(x_data,test_size=0.2,random_state=0)
    del(x_data)
    autoencoder_re.fit(X_train, X_train,
                    epochs=100,
                    shuffle=True,
                    validation_data=(X_test, X_test))


    tf.keras.models.save_model(autoencoder_re,f"../modele_entraine/autoencodeur/autoencodeurFLATTEN.tf")

    del(X_test)
    del(X_train)

    if plot==1 :
        #Print images before and after the passage in the Autoencoder
        n = 10
        skip=0
        plt.figure(figsize=(20, 4))
        for i in range(n):
            #Display the original images
            ax = plt.subplot(2, n, i + 1)
            plt.imshow(tf.squeeze(X_test[skip+i]))
            plt.title("original")
            plt.gray()
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
            #Display the reconstructed images
            ax = plt.subplot(2, n, i + 1 + n)
            plt.imshow(tf.squeeze(decoded_imgs[skip+i]))
            plt.title("reconstructed")
            plt.gray()
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        plt.show()


def import_images(nb_images,start,sexe,filesnames):
    """
        Import images of the dataset. Import nb_images, strat with the images number start and take the same number of male and female.

            input :
                nb_images (int)
                start (int)
                sexe (list)
                filesnames (list)

            output :
                x_data (numpy array)

        """
    dataset_img='img_align_celeba'
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

class AutoEncoder(Model):
    """
        A class to represent the autoencodeur model with an encoder and a decoder
        We can have different form of the latent space by commenting certain lines : we try 3 possibilities :
            matrix (32,32,4)
            matrix (16,16,2)
            vector size 2048
        

        Attributes :

        Methods :
            call 
    """ 
    def __init__(self):
        super(AutoEncoder, self).__init__()
        self.encoder = keras.Sequential([
            layers.Input(shape=(128, 128, 3)),
            layers.Conv2D(8, (3,3), activation='relu', padding='same', strides=2),
            layers.Conv2D(4, (3,3), activation='relu', padding='same', strides=2),
            #layers.Conv2D(2, (3,3), activation='relu', padding='same', strides=2), #commented to have a vector in latent space and a space (32,32,4) in latent space
            layers.Flatten(), #commented to have a matrix in the latent space
            layers.Dense(2048, activation="relu"), #commented to have a matrix in the latent space
            layers.Dense(2048, activation="relu") #commented to have a matrix in the latent space
            ])

        self.decoder = keras.Sequential([
            layers.Dense(2048,activation="relu"), #commented to have a matrix in the latent space
            layers.Dense(32 * 32 * 4, activation="relu"),#commented to have a matrix in the latent space
            layers.Reshape((32, 32, 4)), #commented to have a matrix in the latent space
            #layers.Conv2DTranspose(2, kernel_size=3, strides=2, activation='relu', padding='same'), #commented to have a vector in latent space  and a space (32,32,4) in latent space
            layers.Conv2DTranspose(4, kernel_size=3, strides=2, activation='relu', padding='same'),
            layers.Conv2DTranspose(8, kernel_size=3, strides=2, activation='relu', padding='same'),
            layers.Conv2D(3, kernel_size=(3,3), activation='sigmoid', padding='same')])

    def call(self, x):
        encoded = self.encoder(x) 
        decoded = self.decoder(encoded) 
        return decoded


### Compilation the autoencoder ###

autoencoder = AutoEncoder()

autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

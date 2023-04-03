### Import ####

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

# from sklearn.model_selection import train_test_split

### Fonction definition ###

def load_attr():
    """
    Create the liste of filesnames and sexe of the images

    output :
        sexe (list) :
            List of the sex -1 (Female) or 1 (Male)
        filesnames (list) :
            List of all the filesnames we want to import
    """
    db=pd.read_csv('../f_annexes/new_list_attr_celba.csv',sep=",",usecols=['nb_pic','Male'],low_memory=False)
    filesnames=list(db["nb_pic"])
    sexe=list(db['Male'])
    return(sexe,filesnames)


def retrain(sexe,filenames,nb_images,start,plot=0):
    """
    Fit the autoencodeur with nb_images new images, start with the start images of the dataset. Finally save the autoencodeur with the number num.

    input :
        sexe (list) :
            List of the sex -1 (Female) or 1 (Male)
        filenames (list) :
            List of all the filesnames we want to retrain
        nb_images (int) :
            Number of images we want to retrain
        start (int) :
            Retrain start at the image start
        plot (int) :
            If 1 plot the result of the autoencoder (compare before and after autoencoder)

    """

    #Re-load the model to train it another time, we take another part of the dataset to do it
    #we can do it as many time as we want
    autoencoder_re=tf.keras.models.load_model('../f_annexes/autoencodeurFLATTEN4.tf')
    x_data=import_images(nb_images,start,sexe,filenames)
    samples=[random.randint(0,len(x_data)-1) for i in range(32)]
    X_train, X_test = train_test_split(x_data,test_size=0.2,random_state=0)
    del(x_data)
    if plot==1 :
        encoded_imgs = autoencoder_re.encoder(X_test[:100]).numpy()
        decoded_imgs = autoencoder_re.decoder(encoded_imgs).numpy()
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

        autoencoder_re.fit(X_train, X_train,
                    epochs=50,
                    shuffle=True,
                    validation_data=(X_test, X_test))


    tf.keras.models.save_model(autoencoder_re,"../f_annexes/autoencodeurFLATTEN4.tf")

    del(X_test)
    del(X_train)


def import_images(nb_images,start,sexe,filesnames):
    """
    To give numerotation to the images, import images of the dataset and import nb_images, strat with the images number start and take the same number of male and female.

    input :
        nb_images (int) :
            Number of images we want Retrain start at the image start to import
        start (int) :
            Import start at the image start
        sexe (list) :
            List of the sex -1 (Female) or 1 (Male)
        filesnames (list) :
            List of all the filesnames we want to import

    output :
        x_data (numpy array) :
            List of the images in their np.array form
    """

    dataset_img='../f_annexes/img_align_celeba'
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
        vector size 4096

    Attributes :
        encoder (keras.model) :
            The encoder
        decoder (keras.model) :
            The decoder
    """
    def __init__(self):
        super(AutoEncoder, self).__init__()
        self.encoder = keras.Sequential([
            layers.Input(shape=(128, 128, 3)),
            layers.Conv2D(8, (3,3), activation='relu', padding='same', strides=2),
            layers.Conv2D(4, (3,3), activation='relu', padding='same', strides=2),
            #layers.Conv2D(2, (3,3), activation='relu', padding='same', strides=2), #commented to have a vector in latent space and a space (32,32,4) in latent space
            layers.Flatten(), #commented to have a matrix in the latent space
            layers.Dense(4096, activation="relu"), #commented to have a matrix in the latent space
            layers.Dense(4096, activation="relu") #commented to have a matrix in the latent space
            ])

        self.decoder = keras.Sequential([
            layers.Dense(4096,activation="relu"), #commented to have a matrix in the latent space
            layers.Dense(32 * 32 * 4, activation="relu"),#commented to have a matrix in the latent space
            layers.Reshape((32, 32, 4)), #commented to have a matrix in the latent space
            #layers.Conv2DTranspose(2, kernel_size=3, strides=2, activation='relu', padding='same'), #commented to have a vector in latent space  and a space (32,32,4) in latent space
            layers.Conv2DTranspose(4, kernel_size=3, strides=2, activation='relu', padding='same'),
            layers.Conv2DTranspose(8, kernel_size=3, strides=2, activation='relu', padding='same'),
            layers.Conv2D(3, kernel_size=(3,3), activation='sigmoid', padding='same')])

    def call(self, x):
        """
        This function call the encoder to decod the images given with X
        It's a test function

        input :
            x(np.array) :
                The images into their initial form (in np.array) that will be encoded and then decoded
        """
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


### Compilation the autoencoder ###

autoencoder = AutoEncoder()

autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

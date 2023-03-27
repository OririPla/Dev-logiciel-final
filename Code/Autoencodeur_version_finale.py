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

#### Code #### 

## Load the dataset ## 

dataset_img='img_align_celeba'

#Access files names of the images
filesnames=[]
with open('list_attr_celeba.txt',"r") as file:
    for line in file :
        per_line=line.split(" ")
        name=per_line[0]
        filesnames.append(name)
filesnames=filesnames[2:] #list with all files names

nb_images=1000 #The dataset is too big, so we only take 1000 images 

#Import images 
x=[]
for i in range(0,nb_images):
    image=io.imread(f'{dataset_img}/{filesnames[i]}') #download image 
    image_resize=resize(image,(128,128)) #resize picture with size 128x128 
    x.append(image_resize)

x_data=np.array(x) #transform list into numpy array
x=None

#Separation of the dataset in a training set and a test set 

samples=[random.randint(0,len(x_data)-1) for i in range(32)]

X_train, X_test = train_test_split(x_data,test_size=0.2,random_state=0)


## Autoencodeur ## 

#Creation of an autoencoder class with the encoder and the decoder 
#We can have different form of the latent space by commenting certain lines : we try 3 possibilities :
#matrix (32,32,4) (final version we take for the genetic algorithm)
#matrix (16,16,2)
#vector size 50 

class AutoEncoder(Model):
    def __init__(self):
        super(AutoEncoder, self).__init__()
        self.encoder = keras.Sequential([
            layers.Input(shape=(128, 128, 3)), 
            layers.Conv2D(8, (3,3), activation='relu', padding='same', strides=2),
            layers.Conv2D(4, (3,3), activation='relu', padding='same', strides=2),
            #layers.Conv2D(2, (3,3), activation='relu', padding='same', strides=2), #commented to have a vector in latent space and a space (32,32,4) in latent space
            #layers.Flatten(), #commented to have a matrix in the latent space 
            #layers.Dense(50, activation="relu"), #commented to have a matrix in the latent space 
            #layers.Dense(50, activation="relu") #commented to have a matrix in the latent space 
            ])
    
        self.decoder = keras.Sequential([
            #layers.Dense(100,activation="relu"), #commented to have a matrix in the latent space 
            #layers.Dense(32 * 32 * 4, activation="relu"),#commented to have a matrix in the latent space 
            #layers.Reshape((32, 32, 4)), #commented to have a matrix in the latent space 
            #layers.Conv2DTranspose(2, kernel_size=3, strides=2, activation='relu', padding='same'), #commented to have a vector in latent space  and a space (32,32,4) in latent space
            layers.Conv2DTranspose(4, kernel_size=3, strides=2, activation='relu', padding='same'),
            layers.Conv2DTranspose(8, kernel_size=3, strides=2, activation='relu', padding='same'),
            layers.Conv2D(3, kernel_size=(3,3), activation='sigmoid', padding='same')])
    
    def call(self, x):
        encoded = self.encoder(x) #method to call the encoder
        decoded = self.decoder(encoded) #method to call the decoder 
        return decoded


#Compilation et entrainement de l'autoencodeur 

autoencoder = AutoEncoder()

autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

#Train the autoencodeur with the train dataset 
autoencoder.fit(X_train, X_train,
                epochs=1000,
                shuffle=True,
                validation_data=(X_test, X_test))

#Test on the test dataset 
encoded_imgs = autoencoder.encoder(X_test[:100]).numpy()
decoded_imgs = autoencoder.decoder(encoded_imgs).numpy()
     

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
     
## Save the model ## 
tf.keras.models.save_model(autoencoder,"../modele_entraine/autoencodeur/autoencodeurNONFlatten.tf") #save autoencoder
tf.keras.models.save_model(autoencoder.encoder,"../modele_entraine/encodeur/encodeurNONFlatten.tf") #save encoder 
tf.keras.models.save_model(autoencoder.decoder,"../modele_entraine/decodeur/decodeurNONFlatten.tf") #save decoder 


## Re-train the autoencoder ## 

#Re-load the model to train it another time, we take another part of the dataset to do it 
#we can do it as many time as we want 
autoencoder_re=tf.keras.models.load_model('../modele_entraine/autoencodeur/autoencodeurNONFlatten2.tf')

nb_images=1000

def retrain(nb_images,start,num):
    """
        Fit the autoencodeur with nb_images new images, start with the start images of the dataset. Finally save the autoencodeur with the number num. 

        input :
                nb_images (int)
                start (int)
                num (int)

        output :
                
        """

    x=[]
    for i in range(start,start+nb_images):
        image=io.imread(f'{dataset_img}/{filesnames[i]}')
        image_resize=resize(image,(128,128)) #on prend les images en taille 128x128 
        x.append(image_resize)

    x_data=np.array(x)
    x=None

    samples=[random.randint(0,len(x_data)-1) for i in range(32)]
    X_train, X_test = train_test_split(x_data,test_size=0.2,random_state=0)

    autoencoder_re.fit(X_train, X_train,
                    epochs=500,
                    shuffle=True,
                    validation_data=(X_test, X_test))


    tf.keras.models.save_model(autoencoder_re,f"../modele_entraine/autoencodeur/autoencodeurNONFlatten{num}.tf")

retrain(1000,1000,2)
retrain(1000,2000,3)


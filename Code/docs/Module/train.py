# For train the autoencoder for the first time 

### Import ### 

import Autoencodeur
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import random
import tensorflow as tf


### Code ### 

nb_images=10000 #The dataset is too big, so we only take 1000 images

sexe,filenames=Autoencodeur.load_attr()
x_data=Autoencodeur.import_images(nb_images,0,sexe,filenames,)
print("ok")

#Separation of the dataset in a training set and a test set

samples=[random.randint(0,len(x_data)-1) for i in range(32)]

X_train, X_test = train_test_split(x_data,test_size=0.2,random_state=0)

del x_data

autoencoder=Autoencodeur.autoencoder

#Train the autoencodeur with the train dataset
autoencoder.fit(X_train, X_train,
                epochs=50,
                shuffle=True,
                validation_data=(X_test, X_test))

#Save the model
tf.keras.models.save_model(autoencoder,"../autoencodeurFLATTEN4.tf") #save autoencoder
# tf.keras.models.save_model(autoencoder.encoder,"../modele_entraine/encodeur/encodeurFlatten.tf") #save encoder
# tf.keras.models.save_model(autoencoder.decoder,"../modele_entraine/decodeur/decodeurFlatten.tf") #save decoder


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

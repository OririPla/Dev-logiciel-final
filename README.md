General description

The objective of this project is to create a photofit picture software. The idea is to present several images with faces to the user. The user will have to choose one or more images that is/are closest to the person they wish to report. Each time, a genetic algorithm is followed by a decoder to form new images depending on the chosen images. The decoder comes from a Variationate AutoEncoder(VAE) trained on a database of portraits (CelebrA). This AI is used to generate new images derived from the previously selected images. After several iterations of image selection-generation, a portrait established by the AI can be validated by the user, thus creating the final photofit image. This image can then be exported to a pdf along with the information of the user.
We select 607 images from the datasets CelebA to create a new dataset which will be presented to the user. We chose images with a plain background because the autoencoder work better for this type of images.


Development objectives

This is the third version of our project. It works but could use several ameliorations. First and foremost, it could use a better version of the genetic algorithm and AutoEncoder to have better quality images because ours are very blurry. We could also use another database to have better images. Indeed, the AutoEncoder works better with a plain background. Another improvement could be linked to the graphical interface : you can always make it more intuitive and user-friendly.


Requirements for the development environment to be integrated

The software can be installed on the exploitation system Linux or Mac. It needs an environment python 3. Because of its relatively important size, the user needs some space.


Instructions for installation and use

For the installation you have to run a bash script. Then, to use the software it is very simple, the user can follow the tutorial using the button “Tutoriel” in the first page. The user will then begin choosing one or more images. If no initial image is suitable, they can choose to re-initialise the images. After the choosing phase, the algorithm will generate new images with those that have been selected. You can now select one or more images and so on. When one image is suitable to what the user desires, they can stop the process by validating this image. It can be saved in a pdf document along with other information on the user.


List of the technologies used and, if applicable, links to other information about these technologies

Genetic algorithm : The genetic algorithm makes modifications on the selected images and it mixes them if the user chooses several. The mutations and the crossing-over are made on the selected images in their form vectors (= encoded form).

Autoencoder : The autoencoder combines an encoder and a decoder. The autoencoder was trained with 30 000 images and 50 epochs. You can find the summary of our autoencoder here :
Structure of the encoder:
Layer (type)                Output Shape
=================================================================
 conv2d (Conv2D)             (None, 64, 64, 8)
 conv2d_1 (Conv2D)        (None, 32, 32, 4)
 flatten (Flatten)                (None, 4096)
 dense (Dense)                (None, 4096)
 dense_1 (Dense)            (None, 4096)

 Layer (type)                Output Shape
=================================================================
Structure of the decoder:
=================================================================
dense_3 (Dense)                           (None, 4096)
dense_4 (Dense)                           (None, 4096)
reshape (Reshape)                       (None, 32, 32, 4)
conv2d (Conv2DTranspose)       (None, 32, 32, 4)
 conv2d (Conv2DTranspose)        (None, 64, 64, 8)
 conv2d_3 (Conv2D)                     (None, 128, 128, 3)
=================================================================


Known bugs and possible corrections:

The import Tensorflow has a known warning message asking the user to rebuild it in order to use it at its best. Nevertheless, we weren’t able to rebuild it because of modules’ versions confrontation, and chose to ignore this warning.

The Tensorflow installation is very long therefore we recommend the User to have it beforehand and not create a virtual environment.(Else, the installation will take about 45 min.)

The conversion of the genetic algorithm is bad. We need to retrain the autoencoder and to adapt the genetic algorithm to have better results.

Sometimes there are errors like:
AttributeError : module ‘numpy’ has no attribute ‘object’
ImportError: cannot import name ‘ImageTk’ from ‘PIL’
These errors can be solved by upgrading the package: pip install package --upgrade

There can also be these errors:
No module named ‘fpdf’
No module named ‘skimage’
No module named ‘tensorflow’
No module named ‘PIL’
No module named ‘cv2’
Respectively, they can be solved doing in the terminal:
pip install fpdf
pip install scikit-image
pip install tensorflow
pip install pillow
pip install opencv-python


FAQ

Because this is the first version presented to the Client, we don’t have any questions to relate yet.


Copyright and licensing information

See licence.txt

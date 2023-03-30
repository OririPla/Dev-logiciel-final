# For retrain an existing autoencodeur 

import Autoencodeur

sexe,filenames=Autoencodeur.load_attr()

for i in range(1,100):
    Autoencodeur.retrain(sexe,filenames,1000,i*1000)
    print(i)

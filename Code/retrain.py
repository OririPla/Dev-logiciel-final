"""
For retrain an existing autoencodeur
"""

import Autoencodeur

sexe,filenames=Autoencodeur.load_attr()

for i in range(1,10):
    Autoencodeur.retrain(sexe,filenames,10000,i*10000)
    print(i)

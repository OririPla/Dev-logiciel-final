#!/bin/bash.

python3 -m venv env1
source env1/bin/activate

pip install --upgrade setuptools
pip install --upgrade wheel

pip install Code-groupe1-laguilhon

mv f_annexes env1/lib/python3.9/site-packages/src
mv IMG env1/lib/python3.9/site-packages/src

python3 env1/lib/python3.9/site-packages/src/Code/start_software_faces.py



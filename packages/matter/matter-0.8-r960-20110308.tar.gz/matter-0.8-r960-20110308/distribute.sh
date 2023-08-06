#can optionally change version before doing this

#register
python setup.py register
#put egg in repo
./setup.py bdist_egg
cd dist
scp matter*.egg jbrkeith@login.cacr.caltech.edu:projects/danse/packages/dev_danse_us
#update docs
./docs/transfer.sh



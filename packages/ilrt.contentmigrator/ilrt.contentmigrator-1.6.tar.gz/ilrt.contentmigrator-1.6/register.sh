rm -fr build dist
hg pull
hg up
python2.6 setup.py mregister sdist bdist_egg mupload 
#-r local

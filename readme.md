scripts
=======


Requirements
------------
apt install libgdal-dev libhdf5-serial-dev libnetcdf-dev


Install
-------
ln -s Pipfile$(lsb_release -sr | tr -d '.') Pipfile
pipenv sync --dev


Pipenv
------
Any vcs checkouts are deliberately not included in any setup.py, since pip will
fail miserably in finding a suitable package for it on the web.


Gallery
-------

TODO

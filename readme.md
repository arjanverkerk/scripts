scripts
=======


Requirements
------------
```
apt install python3-gdal libhdf5-serial-dev libnetcdf-dev
```

Install
-------
```
$ virtualenv --system-site-packages .venv
$ .venv/bin/pip install -r requirements.txt
$ .venv/bin/pip install -e .
$ .venv/bin/ln_scripts

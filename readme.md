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
Create a virtualenv::


Install dependencies & package and run tests::

    $ virtualenv .venv --system-site-packages
    $ .venv/bin/pip install -r requirements.txt
    $ .venv/bin/pip install -e .[test]

Update packages::
    
    $ rm -rf .venv
    $ virtualenv .venv --system-site-packages
    $ .venv/bin/pip install -e .
    $ .venv/bin/pip freeze --local | grep -v scripts > requirements.txt
```

from setuptools import setup

import console

name='scripts'
version='0.1'

install_requires = [
    'setuptools',
    # And the rest
    'blessings',
    'flake8',
    'Flask',
    'h5py',
    'ipdb',
    'ipython',
    'jinja2',
    'markdown2',
    'mutagen',
    'numpy',
    'netCDF4',
    'Pillow',
    'Pydap',
    'pyproj',
    'requests',
    'scipy',
]

setup(
    name=name,
    version=version,
    url='',
    author='Arjan Verkerk',
    author_email='arjan.verkerk@gmail.com',
    packages=['scripts'],
    include_package_data = True,
    zip_safe = False,
    install_requires=install_requires,
    entry_points={'console_scripts': console.scripts},
)

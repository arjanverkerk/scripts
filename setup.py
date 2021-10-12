# -*- coding: utf-8 -*-

from setuptools import setup

import console

name = 'scripts'
version = '0.1'

install_requires = [
    'Pillow',
    'gdal',
    'h5py',
    'lz4',
    'numpy',
    'scipy',
    'zest.releaser',
]

tests_require = ['flake8', 'ipython', 'pytest', 'pytest-cov']

setup(
    name=name,
    version=version,
    url='',
    author='Arjan Verkerk',
    author_email='arjan.verkerk@gmail.com',
    packages=['scripts'],
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={"test": tests_require},
    entry_points={'console_scripts': console.scripts},
)

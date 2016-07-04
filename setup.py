# -*- coding: utf-8 -*-

from setuptools import setup

import console

name = 'scripts'
version = '0.1'

install_requires = [
    'flake8',
    'gdal',
    'ipdb',
    'ipython',
    'naw',
    'numpy',
    'redis',
    'scipy',
    'setuptools',
]

setup(
    name=name,
    version=version,
    url='',
    author='Arjan Verkerk',
    author_email='arjan.verkerk@gmail.com',
    packages=['scripts'],
    zip_safe=False,
    install_requires=install_requires,
    entry_points={'console_scripts': console.scripts},
)

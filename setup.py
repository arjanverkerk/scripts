from setuptools import setup
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
    'netCDF4',
    'Pydap',
    'pyproj',
    'requests',
]

entry_points = {'console_scripts': [
  'sync = openradar.scripts.sync:main',
]}

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
    entry_points=entry_points,
)

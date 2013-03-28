from setuptools import setup
name='scripts'
version='0.1'

install_requires = [
    'setuptools',
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

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Preferences",
    version = "0.05",
    url = 'http://preferences.django-development.com/',
    license = 'BSD',
    description = 'It a simple class that creates a list of dictionarries to store preferences as key value pairs.  You can use the class directly or load  the preferences from files.  The main reason I wrote it was to create an easy way of storing more than one preference with the same name and load them form files in a manner that allows for easy appending or replacing of parmeters that could have been loaded from a default prameter file.  There are also several methods to make  managing the preferences easier.',
    long_description = read('README'),

    author = 'Mark Anderson',
    author_email = 'nosrednakram@gmail.com',

    packages = find_packages('src'),
    package_dir = {'': 'src'},

    install_requires = ['setuptools'],

    classifiers = [
          "Development Status :: 3 - Alpha",
          "Operating System :: OS Independent",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python",
          "Topic :: Utilities",
    ]
)


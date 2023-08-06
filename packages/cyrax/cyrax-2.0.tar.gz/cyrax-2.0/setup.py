#!/usr/bin/env python

import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import cyrax

setup(name = 'cyrax',
      description = 'Static site generator',
      long_description = read('README'),
      license = 'BSD',
      version = cyrax.__version__,
      author = 'Alexander Solovyov',
      author_email = 'alexander@solovyov.net',
      url = 'http://hg.piranha.org.ua/cyrax/',
      install_requires = ['Jinja2', 'smartypants'],
      packages = ['cyrax', 'cyrax.template'],

      entry_points = {
        'console_scripts': ['cyrax = cyrax:main']
        },

      classifiers = [
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Editors :: Documentation',
        'Topic :: Utilities',
        ],
      platforms='any',
      )

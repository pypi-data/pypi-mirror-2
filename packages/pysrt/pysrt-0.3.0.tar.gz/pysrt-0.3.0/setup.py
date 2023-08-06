#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

README = ''
try:
    f = open('README.rst')
    README = f.read()
    f.close()
except:
    pass

setup(name='pysrt',
      version='0.3.0',
      author='Jean Boussier',
      author_email='jean.boussier@gmail.com',
      packages=find_packages(),
      description = "SubRip (.srt) subtitle parser and writer",
      long_description=README,
      license = "GPLv3",
      platforms = ["Independent"],
      keywords = "SubRip srt subtitle",
      url = "http://github.com/byroot/pysrt",
      classifiers = [
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Multimedia :: Video",
          "Topic :: Software Development :: Libraries",
          "Topic :: Text Processing :: Markup",
      ],
      )

#!/usr/bin/env python

from distutils.core import setup

setup(name='remember',
      version='0.1',
      packages=['remember', 'remember.test'],
      url='http://mikegraham.bitbucket.org/remember/',
      download_url='http://bitbucket.org/mikegraham/remember/',
      license='MIT',
      author='Mike Graham',
      author_email='mikegraham@gmail.com',
      description='Memoize callables',
      #long_description=
      platforms='any',
      classifiers=["Development Status :: 3 - Alpha",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent"]

      )


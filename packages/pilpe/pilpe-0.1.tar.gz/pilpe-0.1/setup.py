#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pilpe',
      version='0.1',
      description='A image pipeline to apply filters in one or more images.',
      author='Sergio Campos',
      author_email='seocam@seocam.net',
      packages=find_packages(),
      package_data={'': ['*.tiff', '*.tif']},
      install_requires=[],
     )


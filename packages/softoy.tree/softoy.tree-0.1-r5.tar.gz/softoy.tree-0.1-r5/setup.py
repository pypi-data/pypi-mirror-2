# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os

version = '0.1-r5'

setup(name='softoy.tree',
      version=version,
      description="",
      long_description="""\
        """,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Euh Ton-jae',
      author_email='jaeeuh@gmail.com',
      url='',
      license='BSD',
      packages=find_packages(),
      namespace_packages = ['softoy'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      """,
      )

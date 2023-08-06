# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os

version = '0.1.2-r3'

setup(name='softoy.webpage',
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
      packages=['softoy', 'softoy.webpage', 'softoy.webpage.tests'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'softoy.widgets',
      ],
      entry_points="""
      """,
      )

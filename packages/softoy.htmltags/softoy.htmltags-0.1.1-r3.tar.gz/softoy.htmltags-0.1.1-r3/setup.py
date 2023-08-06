# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import sys, os

version = '0.1.1-r3'

setup(name='softoy.htmltags',
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
      packages=['softoy', 'softoy.htmltags', 'softoy.htmltags.tests'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'softoy.tree',
        'webhelpers',
      ],
      entry_points="""
      """,
      )

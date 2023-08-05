#!/usr/bin/env python

from setuptools import setup

setup(name='pyCaBio',
      version='0.5.0',
      description='caBIO Python API',
      long_description='Pythonic API for the caBIO Database, based on caBIO 4.3 web services',
      license='caBIG Open Source Software License',
      platforms='All',
      author='Konrad Rokicki',
      author_email='rokickik@mail.nih.gov',
      url='http://cabioapi.nci.nih.gov/',
      packages=[
            'cabig',
            'cabig.cabio',
            'cabig.cabio.common',
            'cabig.cabio.common.provenance',
      ],
      install_requires=['pyCaCORE==0.3.0'],
      namespace_packages = ['cabig'],
      test_suite = 'tests.unit_tests'
     )

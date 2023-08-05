#!/usr/bin/env

import sys, distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup

setup(name='PokerSleuth',
      version='2.1.0.47',
      description='A wrapper for the Poker Sleuth Scriptable Equity Calculator',
      author='Stutzbach Enterprises, LLC',
      author_email='daniel@stutzbachenterprises.com',
      url='http://pokersleuth.com/programmable-poker-calculator.shtml',
      license = "BSD",
      keywords = "poker equity calculator odds",
      provides = ['pokersleuth'],
      py_modules = ['pokersleuth'],
      zip_safe = True,
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Operating System :: Microsoft :: Windows',
          'Environment :: Win32 (MS Windows)',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Topic :: Games/Entertainment',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          ],
      long_description=open('README.rst').read(),
      )

#!/usr/bin/env python

import sys

try:
    from setuptools import setup
except ImportError:
    print 'This module will use setuptools if available.'
    from distutils.core import setup

setup(name='tdl',
      version='1.0.5',
      author='Kyle Stewart',
      author_email='4B796C65+tdl@gmail.com',
      description='Graphical and utility library for making a roguelike or other tile-based video games',
      long_description="""
tdl is a ctypes port of The Doryen Library.

The library is used for displaying tilesets (ascii or graphical) in true color.
""",
      url='http://4b796c65.googlepages.com/tdl',
      download_url='https://launchpad.net/rlu/+download',
      packages=['tdl'],
      include_package_data=True,
      install_requires=['setuptools'],
      classifiers=['Development Status :: 4 - Beta',
                   'Programming Language :: Python',
                   'Environment :: Win32 (MS Windows)',
                   'Environment :: X11 Applications',
                   'Natural Language :: English',
                   'Intended Audience :: Developers',
                   'Topic :: Games/Entertainment',
                   'License :: OSI Approved :: zlib/libpng License',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: Microsoft :: Windows',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
      keywords = 'roguelike roguelikes console text curses doryen ascii',
      zip_safe=True,
      )

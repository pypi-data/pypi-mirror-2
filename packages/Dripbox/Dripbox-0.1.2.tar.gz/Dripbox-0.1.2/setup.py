#!/usr/bin/env python

from distutils.core import setup

setup(name='Dripbox',
      version='0.1.2',
      description='Smart one-way SFTP file synchronization',
      author='Eric Allen',
      author_email='eric@hackerengineer.net',
      maintainer='Eric Allen',
      maintainer_email='eric@hackerengineer.net',
      url='http://github.com/epall/dripbox',
      py_modules=['dripbox'],
      scripts=['scripts/drip'],
      requires=['MacFSEvents', 'paramiko'],
      install_requires=['fsevents', 'paramiko'],
      license='GPL v2.0'
     )


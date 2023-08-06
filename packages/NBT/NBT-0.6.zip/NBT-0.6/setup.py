#!/usr/bin/env python

from distutils.core import setup

setup(
      name='NBT',
      version='0.6',
      description='Named Binary Tag Reader/Writer',
      author='Thomas Woolford',
      author_email='woolford.thomas@gmail.com',
      url='http://github.com/twoolie/NBT',
      license = open("LICENSE.txt").read(),
      long_description = open("README.txt").read(),
      packages=['nbt'],
      package_data={'mypkg': ['*.nbt']},
     )

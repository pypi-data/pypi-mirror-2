#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup
#from distutils.core import setup

version = '0.5.2'
readme = open('README.rst', 'r').read()

setup(name='Argot',
      version=version,
      description=readme.split('\n')[0],
      long_description=readme,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
          'Topic :: Text Processing :: Markup :: HTML',],
      keywords='html markup markdown',
      author='Jason Moiron',
      author_email='jmoiron@jmoiron.net',
      url='http://dev.jmoiron.net/hg/argot/',
      license='MIT',
      packages=['argot'],
      scripts=['bin/argot'],
      # setuptools specific
      zip_safe=False,
      # i'm not sure how to get my virtualenv or setuptools to realize that
      # there is a perfectly fine system-wide lxml library available; until
      # i fix that, there won't be a "hard" requirement, even though lxml is
      # 100% required for argot to function
      install_requires=['markdown', 'pygments'] # , 'lxml'],
)



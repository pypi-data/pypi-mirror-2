#!/usr/bin/env python
# -*- coding: utf-8 -*-
##############################################################################
#       Copyright (C) 2010, Joel B. Mohler <joel@kiwistrawberry.us>
#
#  Distributed under the terms of the GNU General Public License (GPLv2 or later)
#                  http://www.gnu.org/licenses/
##############################################################################

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='fuzzyparsers',
      version='0.7.1',
      description='A collection of free-form input parsers (with special focus on dates)',
      license='GPLv2 or later',
      author='Joel B. Mohler',
      author_email='joel@kiwistrawberry.us',
      long_description=read('README.txt'),
      url='https://bitbucket.org/jbmohler/fuzzyparsers',
      packages=['fuzzyparsers'],
     )

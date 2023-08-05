# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Evax Software
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution. The terms
# are also available at
# http://www.evax.fr/open-source-software/evax.bitten.tools

from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='evax.bitten.tools',
      version=version,
      description="Bitten plugin adding check and lcov support",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Framework :: Trac",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing"
        ],
      keywords=['trac', 'bitten', 'check', 'lcov'],
      author='Evax Software',
      author_email='contact@evax.fr',
      url='http://www.evax.fr/open-source-software/evax.bitten.tools',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['evax', 'evax.bitten'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'bitten',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [bitten.recipe_commands]
      http://www.evax.fr/bitten/tools#check = evax.bitten.tools:check
      http://www.evax.fr/bitten/tools#lcov = evax.bitten.tools:lcov
      """,
      )

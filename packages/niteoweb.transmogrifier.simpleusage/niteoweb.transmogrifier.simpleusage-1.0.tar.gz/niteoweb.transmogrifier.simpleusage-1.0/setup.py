# -*- coding: utf-8 -*-
"""Installer for this package."""

import os
from setuptools import setup, find_packages


version = '1.0'

setup(name='niteoweb.transmogrifier.simpleusage',
      version=version,
      description="A simple example of how to use collective.transmogrifier",
      long_description=open("README").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone transmogrifier',
      author='NiteoWeb Ltd.',
      author_email='info@niteoweb.com',
      url='http://svn.plone.org/svn/collective/niteoweb.transmogrifier.simpleusage/',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      namespace_packages=['niteoweb', 'niteoweb.transmogrifier'],
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

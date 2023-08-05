# -*- coding: utf-8 -*-
"""This module contains the tool of Products.ATMediaPage."""
import os
from setuptools import setup, find_packages

version = '0.2.1'

setup(name='Products.ATMediaPage',
      version=version,
      description="Simple and easy to use Plone page with predefined layouts.",
      long_description=open("README.txt").read() + "\n\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='Zope CMF Plone Images Layout Document Article',
      author='Maik Derstappen',
      author_email='maik.derstappen@inqbus.de',
      url='http://plone.org/products/atmediapage',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.prettyphoto',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],
      )

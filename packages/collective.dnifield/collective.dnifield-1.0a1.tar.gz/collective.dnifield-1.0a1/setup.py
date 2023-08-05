# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.0a1'

setup(name='collective.dnifield',
      version=version,
      description="A field to enter a national identity number.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        ],
      keywords='dni nif field',
      author='Israel Saeta Pérez',
      author_email='israel.saeta@dukebody.com',
      url='http://svn.plone.org/svn/collective/collective.dnifield',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'zope.schema',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

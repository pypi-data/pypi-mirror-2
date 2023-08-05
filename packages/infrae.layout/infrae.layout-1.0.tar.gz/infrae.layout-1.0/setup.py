# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id: setup.py 43159 2010-06-30 14:33:21Z sylvain $

from setuptools import setup, find_packages
import os

version = '1.0'

tests_require = [
    'infrae.wsgi [test]',
    ]

setup(name='infrae.layout',
      version=version,
      description="Layout system for Zope 2",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          "Environment :: Web Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Zope Public License",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Framework :: Zope2",
          ],
      keywords='zope2 layout silva infrae',
      author='Sylvain Viollon',
      author_email='info@infrae.com',
      url='http://svn.infrae.com/infrae.layout/trunk',
      license='ZPL',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['infrae'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'Zope2 >= 2.12.4',
        'five.grok',
        'setuptools',
        'infrae.wsgi',
        ],
      tests_require = tests_require,
      extras_require = {'test': tests_require},
      )

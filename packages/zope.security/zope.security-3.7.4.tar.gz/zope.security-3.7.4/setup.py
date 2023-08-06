##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.security package

$Id: setup.py 116839 2010-09-25 11:20:03Z icemac $
"""
import os
from setuptools import setup, find_packages, Extension

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.security',
      version='3.7.4',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='Zope Security Framework',
      long_description=(
          read('README.txt')
          + '\n.. contents::\n\n' +
          read('src', 'zope', 'security', 'README.txt')
          + '\n\n' +
          read('src', 'zope', 'security', 'untrustedinterpreter.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      keywords = "zope security policy principal permission",
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://pypi.python.org/pypi/zope.security',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['zope'],
      ext_modules=[Extension("zope.security._proxy",
                             [os.path.join('src', 'zope', 'security',
                                           "_proxy.c")
                              ], include_dirs=['include']),
                   Extension("zope.security._zope_security_checker",
                             [os.path.join('src', 'zope', 'security',
                                           "_zope_security_checker.c")
                              ]),
                   ],
      install_requires=['setuptools',
                        'zope.component',
                        'zope.configuration',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.location',
                        'zope.proxy >= 3.4.2',
                        'zope.schema',
                        ],
      extras_require = dict(
          untrustedpython=["RestrictedPython"],
          test=[
              "RestrictedPython",
              "zope.testing",
              ],
          pytz=["pytz"],
          ),
      include_package_data = True,
      zip_safe = False,
      )

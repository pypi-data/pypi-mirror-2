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
"""Setup for zope.app.catalog package

$Id: setup.py 80209 2007-09-27 09:38:31Z berndroessl $
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.app.component',
      version='3.9.1',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='Local Zope Component Support',
      long_description=(
          read('README.txt')
          + '\n\n.. contents:: \n\n' +
          read('CHANGES.txt')
          ),
      keywords="zope component architecture local",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope3'],
      url='http://pypi.python.org/pypi/zope.app.component',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope', 'zope.app'],
      extras_require=dict(
          test=['zope.app.testing',
                'zope.app.securitypolicy',
                'zope.app.zcmlfiles',
                'zope.app.schema',
                'zope.testbrowser',
                'zope.login',
                ]),
      install_requires=[
          'setuptools',
          'zope.site',
          'zope.annotation',
          'zope.app.container',
          'zope.app.pagetemplate',
          'zope.cachedescriptors',
          'zope.component [hook,zcml] >= 3.8',
          'zope.configuration',
          'zope.deprecation',
          'zope.event',
          'zope.exceptions',
          'zope.filerepresentation',
          'zope.formlib',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.lifecycleevent',
          'zope.publisher>=3.12.0',
          'zope.schema',
          'zope.security',
          'zope.traversing',
          'zope.componentvocabulary',
          'ZODB3',
          ],
      include_package_data=True,
      zip_safe=False,
      )


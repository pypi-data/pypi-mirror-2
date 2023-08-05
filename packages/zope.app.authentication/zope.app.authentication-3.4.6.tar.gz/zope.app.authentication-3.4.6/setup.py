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
"""Setup for zope.app.authentication package

$Id: setup.py 112766 2010-05-27 10:26:17Z janwijbrand $
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.app.authentication',
      version='3.4.6',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='Pluggable Authentication Utility',
      long_description=(
        read('README.txt')
        + '\n\n' +
        'Detailed Documentation\n' +
        '----------------------\n'
        + '\n' +
        read('src', 'zope', 'app', 'authentication', 'README.txt')
        + '\n\n' +
        read('src', 'zope', 'app', 'authentication', 'principalfolder.txt')
        + '\n\n' +
        read('src', 'zope', 'app', 'authentication', 'vocabulary.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
      url='http://cheeseshop.python.org/pypi/zope.app.authentication',
      license='ZPL 2.1',
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
      keywords='zope3 authentication pluggable principal group',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      extras_require=dict(test=['zope.app.testing',
                                'zope.app.securitypolicy',
                                'zope.app.zcmlfiles',
                                'zope.securitypolicy',
                                'zope.testbrowser']),
      namespace_packages=['zope', 'zope.app'],
      install_requires=['setuptools',
                        'zope.app.component',
                        'zope.app.container',
                        'zope.app.form',
                        'zope.app.security',
                        'zope.dublincore',
                        'zope.event',
                        'zope.exceptions',
                        'zope.i18n',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.location',
                        'zope.publisher',
                        'zope.schema',
                        'zope.security',
                        'zope.session',
                        'zope.traversing',
                        'ZODB3',
                        ],
      include_package_data = True,
      zip_safe = False,
      )

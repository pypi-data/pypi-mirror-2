##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""Setup for zope.dublincore package

$Id: setup.py 111186 2010-04-20 19:22:34Z tseaver $
"""
from setuptools import setup, find_packages
import os.path

def read(*path):
    return open(os.path.join(*path)).read() + '\n\n'

version = '3.6.2'

long_description = (
    '.. contents::\n\n' +
    '========\n' +
    'Overview\n' +
    '========\n' +
    read('README.txt') +
    read('src', 'zope', 'dublincore', 'property.txt') +
    read('src', 'zope', 'dublincore', 'tests', 'partial.txt') +
    read('src', 'zope', 'dublincore', 'tests', 'timeannotators.txt') +
    read('CHANGES.txt')
    )

setup(
    name="zope.dublincore",
    version=version,
    url='http://pypi.python.org/pypi/zope.dublincore',
    license='ZPL 2.1',
    description='Zope Dublin Core implementation',
    long_description=long_description,
    author='Zope Foundatoin and Contributors',
    author_email='zope-dev@zope.org',

    packages=find_packages('src'),
    package_dir={'':'src'},
    namespace_packages=['zope'],
    include_package_data=True,
    extras_require=dict(
        test=['zope.testing',
              'zope.annotation',
              ]
        ),
    install_requires = ['setuptools',
                        'pytz',
                        'zope.component',
                        'zope.datetime',
                        'zope.interface',
                        'zope.lifecycleevent',
                        'zope.location',
                        'zope.schema',
                        'zope.security',
                        ],
    zip_safe = False
    )

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
"""Setup for zope.app.session package

$Id: setup.py 116098 2010-09-01 14:54:42Z menesis $
"""
import os

from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.app.session',
    version='3.6.2',
    author='Zope Corporation and Contributors',
    author_email='zope-dev@zope.org',
    description='Zope session',
    long_description=(
        read('README.txt')
        + '\n\n' +
        read('CHANGES.txt')
        ),
    license='ZPL 2.1',
    keywords = "zope3 session",
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
    url='http://pypi.python.org/pypi/zope.app.session',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    namespace_packages=['zope', 'zope.app'],
    extras_require = dict(test=['zope.site',
                                'zope.app.testing',
                                'zope.app.zptpage',
                                'zope.app.securitypolicy',
                                'zope.app.zcmlfiles']),
    install_requires=['setuptools',
                      'ZODB3',
                      'zope.annotation',
                      'zope.app.appsetup',
                      'zope.app.http',
                      'zope.component',
                      'zope.i18nmessageid',
                      'zope.interface',
                      'zope.location',
                      'zope.minmax',
                      'zope.publisher',
                      'zope.session',
                      ],
    include_package_data = True,
    zip_safe = False,
    )

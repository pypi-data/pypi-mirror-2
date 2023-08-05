"""
$Id$

Copyright (c) 2007 - 2008 ifPeople, Kapil Thangavelu, and Contributors
All rights reserved. Refer to LICENSE.txt for details of distribution and use.

Distutils setup
 
"""

import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.9'

setup(name='getpaid.discount',
      version=version,
      license = 'ZPL2.1',
      description='package for plone getpaid handling discounts',
      long_description = (
        read('README.txt')
        + '\n' +
        read('CHANGES.txt')
        + '\n' +
        'Detailed Documentation\n'
        '**********************\n'
        + '\n' +
        read('src', 'getpaid', 'discount', 'README.txt')
        + '\n' +
        'Download\n'
        '**********************\n'
        ),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='',
      author='Six Feet Up, Inc.',
      author_email='info@sixfeetup.com',
      url='http://code.google.com/p/getpaid',
      packages=find_packages('src'),
      package_dir={'':'src'},
      namespace_packages=['getpaid'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'five.formlib',
                        'plone.z3cform>=0.6.0',
                        'z3c.form>=1.9.0',
                        'zope.schema>=3.6.0',
                        'getpaid.core>=0.7.6dev',
                        'plone.app.portlets',
                        'plone.portlets',
                        'zope.annotation',
                        'zope.component',
                        'zope.container',
                        'zope.i18n>=3.4',
                        'zope.i18nmessageid',
                        'zope.interface',
                        'zope.formlib',
                        'Products.CMFCore',
                        'Products.PloneGetPaid>=0.8.6dev',
                         ],
      )

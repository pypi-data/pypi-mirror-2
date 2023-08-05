# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.buildout.cluster
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.6'

long_description = (
    read('README.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('collective', 'buildout', 'cluster', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '********\n'
    )
entry_point = 'collective.buildout.cluster:Recipe'
cluster_control = 'collective.buildout.cluster.cluster:main'
entry_points = {"zc.buildout": ["default = %s" % entry_point],
                "console_scripts": ["cluster-control = %s" % cluster_control]}

tests_require=['zope.testing', 'zc.buildout']

setup(name='collective.buildout.cluster',
      version=version,
      description="A package to introspect and manage a buildout-based cluster configuration in an object-oriented way",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        ],
      keywords='buildout cluster management introspection configuration',
      author='Sidnei da Silva',
      author_email='sidnei at enfoldsystems dot com',
      url='',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.buildout'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        # -*- Extra requirements: -*-
                        'iniparse',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'collective.buildout.cluster.tests.test_docs.test_suite',
      entry_points=entry_points,
      )

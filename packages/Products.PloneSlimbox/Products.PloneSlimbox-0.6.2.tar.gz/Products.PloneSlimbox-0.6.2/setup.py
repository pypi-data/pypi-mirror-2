# -*- coding: utf-8 -*-
"""
This module contains the tool of Products.PloneSlimbox
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = read("Products", "PloneSlimbox", "version.txt").strip()

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('Products', 'PloneSlimbox', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require=['zope.testing']

setup(name='Products.PloneSlimbox',
      version=version,
      description="Slimbox(Lightweight Lightbox clone) for atct album view and COREBlog2 attachment image view for Plone.",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='Plone PloneSlimbox Lightbox Slimbox',
      author='takanori',
      author_email='takanori@takanory.net',
      url='http://plone.org/products/plone-slimbox/',
      license='MIT License',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'Products.PloneSlimbox.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*- 
      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins = ["ZopeSkel"],
      )

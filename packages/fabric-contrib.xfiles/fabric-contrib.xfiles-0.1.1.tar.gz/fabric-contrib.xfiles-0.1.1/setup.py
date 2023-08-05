# -*- coding: utf-8 -*-

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages, Command

long_desc = '''
This package contains the xfiles - Fabric extension.
The module adds the support to work with XML files in Fabric.

Read the official documentation for installation, usage and examples:
http://packages.python.org/fabric-conrtib.xfiles
'''
from fabric.contrib import xfiles

# Optional dependency for nose
try:
  import nose
  suite = 'nose.collector'
except ImportError:
  suite = ''

setup(
    name='fabric-contrib.xfiles',
    version = xfiles.__version__,
    url = 'http://bitbucket.org/jmu/fabric-contrib',
    download_url = 'http://pypi.python.org/pypi/xfiles',
    license = 'MIT',
    author = 'Juha Mustonen',
    author_email = 'juha.p.mustonen@gmail.com',
    description = 'Fabric extension: xfiles',
    long_description = long_desc,
    zip_safe = False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
    platforms = 'any',
    packages = find_packages(),
    include_package_data = True,
    install_requires = ['Fabric>=0.9'],
    namespace_packages = ['fabric', 'fabric.contrib'],
    test_suite = suite,
    entry_points = {
        "distutils.commands": [ ],
    },
)


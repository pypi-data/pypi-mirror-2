#!/usr/bin/env python
# -*- coding: utf-8 -
#
# This file is part of restkit released under the MIT license. 
# See the NOTICE for more information.

import os
import sys

if not hasattr(sys, 'version_info') or sys.version_info < (2, 5, 0, 'final'):
    raise SystemExit("Restkit requires Python 2.5 or later.")

extras = {}
try:
    import ssl
except ImportError:
    sys.stderr.write("Warning: On python 2.5x, https support requires "
                + " ssl module (http://pypi.python.org/pypi/ssl) "
                + "to be intalled.")

from setuptools import setup, find_packages

from restkit import __version__

setup(
    name = 'restkit',
    version = __version__,
    description = 'Python REST kit',
    long_description = file(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author = 'Benoit Chesneau',
    author_email = 'benoitc@e-engura.org',
    license = 'BSD',
    url = 'http://benoitc.github.com/restkit',
    zip_safe = True,

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
    packages = find_packages(exclude=['tests']),
    entry_points = {
        'console_scripts': [
            'restcli = restkit.contrib.console:main',
        ],
        'paste.app_factory': [
            'proxy = restkit.contrib.wsgi_proxy:make_proxy',
            'host_proxy = restkit.contrib.wsgi_proxy:make_host_proxy',
            'couchdb_proxy = restkit.contrib.wsgi_proxy:make_couchdb_proxy',
        ],
    },

    test_suite = 'nose.collector',
)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from distutils.core import setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

# Dynamically get the constants.
constants = __import__('pyticli.constants').constants

setup(
    name='pyticli',
    version=constants.__version__,
    author=constants.__author__,
    author_email=constants.__email__,
    url=constants.__url__,
    description=constants.__description__,
    long_description=read('README.txt') + "\n\n" + read('CHANGES.txt'),
    license=constants.__license__,
    keywords='itl interval logic temporal python graph database gremlin query',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        ],
    zip_safe=False,
    packages=[
        "pyticli",
    ],
    include_package_data=True,
    install_requires=[
        "neo4j-rest-client"
    ],
)

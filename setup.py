#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2010 - 2011, 2013 K Richard Pixley
#
# See LICENSE for details.
#
# Time-stamp: <30-Jun-2013 19:46:32 PDT by rich@noir.com>

import os
import platform

import distribute_setup
distribute_setup.use_setuptools()

import setuptools
import elffile

me='K Richard Pixley'
memail='rich@noir.com'

setup_requirements = [
    'coding',
    'nose',
    'setuptools_hg',
    ]

version_tuple = platform.python_version_tuple()
version = platform.python_version()

if version not in [
    '3.0.1',
    '3.1.5',
    '3.3.1',
    ]:
    setup_requirements.append('setuptools_lint')

if version not in [
    '3.0.1',
    ]:
    setup_requirements.append('sphinx>=1.0.5')


setuptools.setup(
    name='elffile',
    version='0.6',
    author=me,
    maintainer=me,
    author_email=memail,
    maintainer_email=memail,
    keywords='elf object file',
    url='http://bitbucket.org/krp/elffile',
    download_url='https://bitbucket.org/krp/elffile/get/default.tar.bz2',
    description='A pure python library for reading and writing ELF format object files.',
    license='MIT',
    long_description=elffile.__doc__,
    setup_requires=setup_requirements,
    install_requires=[
        'coding',
        ],
    py_modules=['elffile'],
    include_package_data=True,
    test_suite='nose.collector',
    scripts = [
    	'objdump.py',
        'objcmp.py',
        ],
    requires=[
        ],
    provides=[
        'elffile',
        ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        ],
    )

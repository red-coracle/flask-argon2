#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Flask-Argon2
    ------------

    The Flask-Argon2 extension provides Argon2i password hashing with
    sensible defaults and a random salt for Flask.

    Links
    `````
    * `Documentation <http://flask-argon2.readthedocs.org/en/latest/>`_
    * `Development version <https://github.com/red-coracle/flask-argon2>`_
    * `argon2_cffi <https://github.com/hynek/argon2_cffi>`_
'''

import os
from setuptools import setup

MODULE_PATH = os.path.join(os.path.dirname(__file__), 'flask_argon2.py')
VERSION_LINE = tuple(f for f in open(MODULE_PATH).readlines()
                     if '__version_info__' in f)[0]

__version__ = '.'.join(eval(VERSION_LINE.split('__version_info__ = ')[-1]))

setup(
    name='Flask-Argon2',
    version=__version__,
    url='https://github.com/red-coracle/flask-argon2',
    license='MIT',
    author='DominusTemporis',
    author_email='python@dominustemporis.com',
    description='Flask-Argon2 provides convenient wrappers for Argon2 password hashing',
    long_description=__doc__,
    py_modules=['flask_argon2'],
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    install_requires=['Flask', 'argon2_cffi'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='test_flask_argon2'
)

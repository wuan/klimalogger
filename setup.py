#!/usr/bin/env python
# -*- coding: utf8 -*-

from setuptools import setup, find_packages

import glob

setup(
    name='klimalogger',
    version='0.1.22',
    packages=find_packages(),
    scripts=glob.glob('scripts/*'),
    url='',
    license='License :: OSI Approved :: Apache License 2.0',
    author='Andreas Würl',
    author_email='andreas@wuerl.net',
    description='Simple data logging client for InfluxDB',
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=['influxdb', 'injector', 'lazy'],
    tests_require=['pytest-cov', 'mock', 'assertpy']
)

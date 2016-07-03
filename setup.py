# coding=utf-8

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '1.0.0'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

PACKAGES = [
    'gateguard'
]

with open(os.path.join(BASE_DIR, 'README.rst')) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='gateguard',
    version=VERSION,
    packages=PACKAGES,
    description='Schema-based validation package',
    long_description=LONG_DESCRIPTION,
    author='Vitalii Maslov',
    author_email='me@pyvim.com',
    url='https://github.com/pyvim/gateguard',
    download_url='https://github.com/pyvim/gateguard/tarball/master',
    license='MIT',
    keywords='validate, validation, dict, json, data, protect, schema',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)

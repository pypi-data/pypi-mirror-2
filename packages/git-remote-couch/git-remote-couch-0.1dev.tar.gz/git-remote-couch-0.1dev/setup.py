#!/usr/bin/env python 
from setuptools import setup, find_packages
import platform

from os.path import join, dirname

long_description = open(join(dirname(__file__), "README.rst")).read()

name='git-remote-couch'

setup(
    name=name,
    version='0.1dev',
    url='http://www.python.org/pypi/'+name,
    license='Beerware',
    description='a git-remote-helper that allows you to push source code into a CouchDB',
    author='Filip Noetzel',
    author_email='filip+pypi@j03.de',
    long_description=long_description,
    packages=['git_remote_couch'],
    package_dir={'': 'src',},
    namespace_packages=[],
    include_package_data = True,
    install_requires=[
      'CouchDB==0.7'
    ],
    zip_safe = False,
    extras_require = dict(
        test=[
            'zope.testing',
            'lovely.testlayers==0.1.0a7',
            'livetest==0.3dev',
            ]),
    entry_points = {
        'console_scripts' : [
            'git-remote-http+couch = git_remote_couch:main',
            ]
        },
    )

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
sys.path.insert(0, os.path.dirname(__file__))

from setuptools import setup

from testmania import __version__

install_requires = []
if sys.version_info[0:2] < (2, 7):
    install_requires.append('unittest2')


f = open("README.rst")
try:
    try:
        readme_content = f.read()
    except:
        readme_content = ""
finally:
    f.close()


setup(
    name='testmania',
    version=__version__,
    description='Library of assert_xxx functions for more convenient testing',
    long_description=readme_content,
    author='Victor Nakoryakov (aka nailxx)',
    author_email='nail.xx@gmail.com',
    license='MIT',
    keywords="test unittest assert",
    url='https://github.com/nailxx/testmania',
    packages=['testmania'],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
    ],
)

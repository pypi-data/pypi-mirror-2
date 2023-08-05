#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 by Hartmut Goebel <h.goebel@goebel-consult.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import sys

if sys.version_info < (2,5) or sys.version_info >= (3,):
    sys.exit('openvas.omplib requires Python >= 2.5 but < 3.0')

from setuptools import setup, find_packages
import os

long_description="\n\n".join([
    open(os.path.join("README.txt")).read(),
    ])

setup(
    name = "openvas.omplib",
    version = "0.0.1",
    install_requires = ['setuptools', 'argparse'],

    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['openvas'],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        },

    # metadata for upload to PyPI
    author = "Hartmut Goebel",
    author_email = "h.goebel@goebel-consult.de",
    description = "An OMP (OpenVAS Management Protocol) client interface for Python",
    long_description = long_description,
    license = "GPL 3.0",
    keywords = "OpenVAS,OMP,OpenVAS Management Protocol,Nessus",
    url          = "http://www.openvas.org/",
    #download_url = "http://pdfposter.origo.ethz.ch/download",
    classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Topic :: Security',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # these are for easy_install (used by bdist_*)
    zip_safe = True,
    entry_points = {
        "console_scripts": [
            "omp-cli = openvas.omplib.cmd:run",
        ],
    },
)

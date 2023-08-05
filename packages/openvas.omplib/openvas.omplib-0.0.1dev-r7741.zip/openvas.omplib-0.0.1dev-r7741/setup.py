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
from distutils.core import Command
from distutils import log

class build_docs(Command):
    description = "build documentation from rst-files"
    user_options=[]

    def initialize_options (self): pass
    def finalize_options (self):
        self.docpages = DOCPAGES
        
    def run(self):
        substitutions = ('.. |VERSION| replace:: '
                         + self.distribution.get_version())
        for writer, rstfilename, outfilename in self.docpages:
            distutils.dir_util.mkpath(os.path.dirname(outfilename))
            log.info("creating %s page %s", writer, outfilename)
            if not self.dry_run:
                try:
                    rsttext = open(rstfilename).read()
                except IOError, e:
                    sys.exit(e)
                rsttext = '\n'.join((substitutions, rsttext))
                # docutils.core does not offer easy reading from a
                # string into a file, so we need to do it ourself :-(
                doc = docutils.core.publish_string(source=rsttext,
                                                   source_path=rstfilename,
                                                   writer_name=writer)
                try:
                    rsttext = open(outfilename, 'w').write(doc)
                except IOError, e:
                    sys.exit(e)

cmdclass = {}

try:
    import docutils.core
    import docutils.io
    import docutils.writers.manpage
    import distutils.command.build
    distutils.command.build.build.sub_commands.append(('build_docs', None))
    cmdclass['build_docs'] = build_docs
except ImportError:
    log.warning("docutils not installed, can not build man pages.")

DOCPAGES = (
    ('manpage', 'omp-cli.rst', 'doc/omp-cli.1'),
    ('html', 'omp-cli.rst', 'doc/omp-cli.html'),
    )

long_description="\n\n".join([
    open(os.path.join("README.txt")).read(),
    ])

setup(
    cmdclass=cmdclass,
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

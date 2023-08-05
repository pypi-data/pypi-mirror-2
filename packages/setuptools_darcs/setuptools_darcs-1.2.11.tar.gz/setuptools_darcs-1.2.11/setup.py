#!/usr/bin/env python

# setuptools plugin for darcs
# Author: Zooko O'Whielacronx

# Permission is hereby granted to any person obtaining a copy of this work to
# deal in this work without restriction (including the rights to use, modify,
# distribute, sublicense, and/or sell copies).

# See README.txt for instructions.

# Thanks to the authors of setuptools, setuptools_bzr, setuptools_git, and
# setuptools_mtn for documentation and examples.

import os, re, sys

from setuptools import setup, find_packages

trove_classifiers=[
    "Framework :: Setuptools Plugin",
    "Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: BSD License",
    "License :: DFSG approved",
    "Intended Audience :: Developers",
    "Operating System :: Microsoft",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: Unix",
    "Operating System :: POSIX :: Linux",
    "Operating System :: POSIX",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows :: Windows NT/2000",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.4",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Topic :: Utilities",
    "Topic :: Software Development :: Libraries",
    ]

setup_requires = []

# Note that the darcsver command from the darcsver plugin is needed to initialize the
# distribution's .version attribute correctly.  (It does this either by examining darcs history,
# or if that fails by reading the setuptools_darcs/_version.py file).
# darcsver will also write a new version stamp in setuptools_darcs/_version.py, with a version
# number derived from darcs history.
# http://pypi.python.org/pypi/darcsver
# We bundle a copy of the darcsver .egg into our source tree because of this
# issue in Distribute:
# http://bitbucket.org/tarek/distribute/issue/55/revision-control-plugin-automatically-installed-as-a-build-dependency-is-not-present-when-another-build-dependency-is-being
setup_requires.append('darcsver >= 1.2.0')

data_fnames=[ 'README.txt' ]

# In case we are building for a .deb with stdeb's sdist_dsc command, we put the
# docs in "share/doc/python-$PKG".
PKG='setuptools_darcs'
doc_loc = "share/doc/python-" + PKG
data_files = [(doc_loc, data_fnames)]

setup(
    name=PKG,
    description='setuptools plugin for darcs',
    author="Zooko O'Whielacronx",
    author_email='zooko@zooko.com',
    url='http://tahoe-lafs.org/trac/' + PKG,
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    data_files=data_files,
    setup_requires=setup_requires,
    classifiers=trove_classifiers,
    keywords='distutils setuptools setup darcs',
    entry_points={
        'setuptools.file_finders': [
            'darcs = setuptools_darcs.setuptools_darcs:find_files_for_darcs',
            ],
        },
    zip_safe=False, # I prefer unzipped for easier access.
    )

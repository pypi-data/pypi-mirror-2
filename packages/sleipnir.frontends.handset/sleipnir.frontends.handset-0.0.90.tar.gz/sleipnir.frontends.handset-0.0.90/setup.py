#!/usr/bin/env python
# -*- mode: Python; indent-tabs-mode: nil; coding: utf-8  -*-

#
# Copyright 2010, 2011 Carlos Martín
# Copyright 2010, 2011 Universidad de Salamanca
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

"""Main Setup File"""

import os
import re
import sys

if sys.version_info < (2, 6):
    sys.stderr.write("Sleipnir requires Python 2.6 or higher.")
    sys.exit(0)

# Load constants
sys.path.insert(0, 'src')
from sleipnir.frontends.handset import constants

# setuptools build required.
from os.path import normcase as _N
from setuptools import setup, find_packages


# pylint: disable-msg=R0903,E0602
class Files(object):
    """
    Custom Distribution Class to force creation of namespace dirs
    """

    @staticmethod
    def find(walk, suffix, install):
        """Find files that match suffix"""

        _files = []

        for root, dirs, files in os.walk(_N(walk)):
            _files.extend(((_N(install), [os.path.join(root, f)]) \
               for f in files if f.endswith(suffix)))
            for entry in dirs:
                _files += Files.find(
                    os.path.join(walk, entry),
                    suffix,
                    os.path.join(install, entry))
            break
        return _files

    @staticmethod
    def find_ui(walk, suffix, dest):
        """sugar method for qml files"""
        return Files.find(
            walk, suffix,
            os.path.join('share', constants.__appname__, dest))


# Peek author details
AUTHOR, EMAIL = re.match(r'^(.*) <(.*)>$', constants.__author__).groups()


# i18n files
I18N_FILES = Files.find(
    'data/po', '.mo', 'share/locale/' + constants.__appname__
)
# Desktop files
DATA_FILES = [
    (_N('share/pixmaps'), [_N('data/sleipnir.png')]),
    (_N('share/applications'), [_N('data/sleipnir.desktop')]),
]
# UI files and themes
DATA_FILES += Files.find_ui('data/ui', '.qml', 'ui')
DATA_FILES += Files.find_ui('data/ui', '.png', 'ui')

setup(
    author             = AUTHOR,
    author_email       = EMAIL,
    classifiers        = constants.__classifiers__,
    description        = constants.__summary__,
    install_requires   = constants.__requires__,
    license            = constants.__license__,
    long_description   = constants.__long_description__,
    name               = constants.__appname__,
    namespace_packages = [constants.__namespace__],
    package_dir        = {'': 'src'},
    packages           = find_packages(where='src'),
    test_suite         = 'tests',
    tests_require      = [constants.__tests_requires__],
    url                = constants.__url__,
    version            = constants.__version__,
    zip_safe           = False,
    data_files         = DATA_FILES + I18N_FILES,
    entry_points = """
    [%s]
      handset.application = sleipnir.frontends.handset.application:Application
    """ % constants.__entry_point__,
)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 KuraLabs S.R.L
# Copyright (C) 2014 Carlos Jenkins
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from setuptools import setup


def check_version():
    """
    Check that user didn't tried to install the package with Python 2.7
    (and default 'pip' instead of 'pip3').
    """
    import sys
    if sys.version_info < (3, 0):
        print('You cannot install WebDesktop with Python 2')
        print('You\'re using: {.major}.{.minor}.{.micro}'.format(
            sys.version_info
        ))
        sys.exit(1)


check_version()


def check_directory():
    """
    You must always change directory to the parent of this file before
    executing the setup.py script. setuptools will fail reading files,
    including and excluding files from the MANIFEST.in, defining the library
    path, etc, if not.
    """
    from os import chdir
    from pathlib import Path

    here = Path(__file__).parent.resolve()
    if Path.cwd().resolve() != here:
        print('Changing path to {}'.format(here))
        chdir(str(here))


check_directory()


def read(filename):
    """
    Read the content of a file.

    :param str filename: The file to read.

    :return: The content of the file.
    :rtype: str
    """
    from pathlib import Path
    return Path(filename).read_text(encoding='utf-8')


def find_version(filename):
    """
    Find version of a package.

    This will read and parse a Python module that has defined a __version__
    variable. This function does not import the file.

    ::

        setup(
            ...
            version=find_version('lib/package/__init__.py'),
            ...
        )

    :param str filename: Path to a Python module with a __version__ variable.

    :return: The version of the package.
    :rtype: str
    """
    import re

    content = read(filename)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M
    )
    if not version_match:
        raise RuntimeError('Unable to find version string.')

    version = version_match.group(1)

    print('Version found:')
    print('  {}'.format(version))
    print('--')

    return version


setup(
    name='webdesktop',
    version=find_version('lib/webdesktop/__init__.py'),

    # Data files
    package_data={'webdesktop': ['*.ui']},

    # Metadata
    author='KuraLabs S.R.L',
    author_email='info@kuralabs.io',
    description=(
        'WebDesktop is a fullscreen, jailed, unclosable web browser for '
        'kiosks or alike applications.'
    ),
    long_description=read('README.rst'),
    url='https://github.com/kuralabs/webdesktop/',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
    ],

    package_dir={'': 'lib'},
    packages=['webdesktop'],
    entry_points={
        'console_scripts': [
            'webdesktop = webdesktop.__main__:main',
        ]
    },
)

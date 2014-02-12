#!/usr/bin/env python

from distutils.core import setup

setup(
    name='webdesktop',
    version='1.0',
    package_dir={'' : 'lib'},
    packages=['webdesktop'],
    scripts=['bin/webdesktop'],
)

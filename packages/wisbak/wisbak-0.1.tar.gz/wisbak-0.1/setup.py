#!/usr/bin/env python

from distutils.core import setup

setup(
    name='wisbak',
    version='0.1',
    description='Simple *nix backup system',
    author='WiswauD',
    author_email='esj@wwd.ca',
    url='http://bitbucket.org/wiswaud/wisbak',
    requires = ['paramiko'],
    packages=['wisbak'],
    package_data={'wisbak': ['wisbak.conf']},
    scripts=['scripts/wisbak'],
    zip_safe=False
)

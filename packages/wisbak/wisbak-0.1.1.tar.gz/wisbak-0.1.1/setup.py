#!/usr/bin/env python

from distutils.core import setup

setup(
    name='wisbak',
    version='0.1.1',
    description='Simple *nix backup system',
    author='WiswauD',
    author_email='esj@wwd.ca',
    url='http://bitbucket.org/wiswaud/wisbak',
    install_requires = ['paramiko'],
    setup_requires = ['paramiko'],
    requires = ['paramiko'],
    packages=['wisbak'],
    package_data={'wisbak': ['wisbak.conf']},
    scripts=['scripts/wisbak'],
    zip_safe=False,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop', 
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: System :: Archiving :: Backup'
    ]
)

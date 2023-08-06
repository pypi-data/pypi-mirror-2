#!/usr/bin/env python

from distutils.core import setup

from mplayer import __version__


setup(
    name='PyMPlayer',
    version=__version__,
    description='Lightweight, out-of-source wrapper for MPlayer',
    author='Darwin M. Bautista',
    author_email='djclue917@gmail.com',
    url='http://code.google.com/p/python-mplayer/',
    packages=['mplayer'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.1',
        'Topic :: Multimedia :: Video :: Display',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)

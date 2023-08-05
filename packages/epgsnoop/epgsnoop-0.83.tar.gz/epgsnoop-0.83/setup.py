#!/usr/bin/python
"""
epgsnoop
========

epgsnoop is a python package which wraps the dvbsnoop program
and generates XMLTV data. The data is usable for MythTV and
other PVR systems which support the XMLTV data format.

epgsnoop is only currently known to be in use in New Zealand.
Many of the processors are possibly currently targetted to the
EIT data from there. Corrections and additions are welcome.
"""
from distutils.core import setup

setup(
    name='epgsnoop',
    version='0.83',
    description='A wrapper around the dvbsnoop program to create XMLTV comliant data.',
    long_description=__doc__,
    author='Hadley Rich',
    author_email='hads@nice.net.nz',
    url='http://nice.net.nz/epgsnoop',
    download_url='http://nice.net.nz/epgsnoop',
    packages=['epgsnoop'],
    scripts=['scripts/epgsnoop'],
    license='MIT',
    platforms='Linux',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',    
        'Development Status :: 3 - Alpha',
    ],
)

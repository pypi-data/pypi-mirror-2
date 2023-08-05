#!/usr/bin/env python

from os.path import dirname, join
from distutils.core import setup

from edpath import VERSION


NAME = 'edpath'


def read_file(filename):
    filename = join(dirname(__file__), filename)
    with open(filename) as fp:
        return fp.read()


setup(
    name=NAME,
    version=VERSION,
    description='MS Windows command line script '
        'to view & edit PATH-like environment variables.',
    long_description=read_file('README.txt'),
    keywords='terminal command-line windows path environment',
    author='Jonathan Hartley',
    author_email='tartley@tartley.com',
    url='http://code.google.com/p/edpath/',
    license='BSD',
    packages=[NAME],
    scripts=['edpath-script.py', 'edpath.bat'],
    #data_files=[('package', ['files'])],
    # see classifiers http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Terminals',
    ]
)


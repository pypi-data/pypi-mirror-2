#!/usr/bin/env python

from os.path import dirname, join
from distutils.core import setup
import py2exe

from edpath_package import VERSION


NAME = 'edpath'

MS_VISUAL_C_RUNTIME_DIR = '..\\ms-visual-c-runtimes\\Microsoft.VC90.CRT\\'
WIN_BINARY = '%s-windows-%s' % (NAME, VERSION)


def read_file(filename):
    filename = join(dirname(__file__), filename)
    with open(filename) as fp:
        lines = fp.readlines()
    return lines[0], ''.join(lines[1:])


description, long_description = read_file('README.txt')
setup(
    name=NAME,
    version=VERSION,
    description=description,
    long_description=long_description,
    keywords='terminal command-line windows path environment',
    author='Jonathan Hartley',
    author_email='tartley@tartley.com',
    url='http://code.google.com/p/edpath/',
    license='BSD',
    packages=['edpath_package'],
    scripts=[NAME+'.py', NAME+'.bat'],
    #data_files=[('package', ['files'])],
    # see classifiers http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Topic :: Terminals',
    ],

    # py2exe
    data_files = [("Microsoft.VC90.CRT", [
        MS_VISUAL_C_RUNTIME_DIR + 'Microsoft.VC90.CRT.manifest',
        MS_VISUAL_C_RUNTIME_DIR + 'msvcr90.dll',
    ] )],
    console=['edpath.py'],
    options={
        'py2exe':{
            'dist_dir': r'dist\%s' % (WIN_BINARY,),
            'optimize': 2,
            'excludes': [
                'dummy.Process',
                'email',
                'email.utils',
                'Image',
                'multiprocessing',
                'Tkinter',
                '_hashlib',
                '_ssl',
            ],            
        },
    },
)


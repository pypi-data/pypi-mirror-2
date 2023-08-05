#!/usr/bin/env python
'''
MS Windows command line script to view or edit PATH-like environment variables.

Retrieves the value of <varname> from the registry, (not the local environment)
converts semi-colons into newlines and displays the result on stdout. For
environment variables such as PATH, this format is more human-readable.

If --edit is given, the output is instead displayed in $EDITOR. Saved changes
will be written back to the registry. New processes will see the modified
value, but existing processes (including the shell that invoked edpath) will
not.

Note that on Windows, environment variables are defined in one of two places
in the registry, local machine and current user. local-machine values are
overridden by the values in current-user. The exception to this is the PATH
variable, for which the current-user value is *appended* to the local-machine
value. edpath works on current-user values, unless --machine is given.
'''
from contextlib import contextmanager
import os
import subprocess
import sys
from tempfile import mkstemp

try:
    import argparse
except ImportError:
    sys.exit("Error: 'argparse' module missing. Install it from "
        "http://pypi.python.org/pypi/argparse\n"
        "or run under Python 2.7 which has it built in.")

from .registry import get_env_registry, set_env_registry


def process_args():
    '''
    default to current user (True), -m switches to local machine (False)
    '''
    # get script description from this module's docstring
    module_docs = sys.modules['edpath_package.edpath'].__doc__.split('\n\n')
    short_desc = module_docs[0]
    long_desc = '\n\n'.join(module_docs[1:])

    parser = argparse.ArgumentParser(
        description=short_desc, epilog=long_desc, prog='edpath',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-m', '--machine', action='store_true',
        help='Local machine environment, instead of current user.')
    parser.add_argument('-e', '--edit', action='store_true',
        help='Edit PATH in $EDITOR and save changes back to registry.')
    parser.add_argument('-q', '--quiet', action='store_true',
        help='Don\'t display value on stdout.')
    parser.add_argument('varname', default='PATH', nargs='?',
        help='the name of an environment variable (defaults to PATH)')

    options = parser.parse_args(sys.argv[1:])

    if options.quiet and not options.edit:
        sys.exit('Error: --quiet without --edit '
                'produces no output and has no effect')
    return options


def get_path(options):
    path = get_env_registry(options.varname, not options.machine)
    if path is not None:
        path = path.replace(';', '\n')
    return path


@contextmanager
def tempfile():
    '''
    Create new tempfile, return handle and filename
    On exiting the 'with' block, close & delete the file if it isn't already.
    '''
    fp, filename = mkstemp()
    yield fp, filename
    try:
        os.close(fp)
        os.unlink(filename)
    except (OSError, WindowsError):
        pass # file handle was already closed or deleted


def read_from_file(filename):
    with open(filename, 'r') as fp:
        newpath = fp.read()
    if newpath != '':
        return newpath


def edit_path(path):
    with tempfile() as (fp, filename):
        if path:
            os.write(fp, path.encode())
        os.close(fp) # so that EDITOR can write to the tempfile
        subprocess.call([os.environ['EDITOR'], filename])
        return read_from_file(filename)    


def display_path(path):
    if path is None:
        print('Not set')
    else:
        print(path)


def persist_path(path, options):
    if path is not None:
        path = path.replace('\n', ';')
    set_env_registry(
        options.varname, path, not options.machine)


def main():
    options = process_args()
    path = get_path(options)
    if options.edit:
        path = edit_path(path)
    if not options.quiet:
        display_path(path)
    if options.edit:
        persist_path(path, options)


if __name__ == '__main__':
    main()


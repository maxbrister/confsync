#!/usr/bin/python3
import argparse
import os
import os.path
from os.path import join

def log(msg):
    if VERBOSE:
        print(msg)

def link_recursive(source, dest):
    for dname, sub_dlist, flist in os.walk(source):
        dest_dname = os.path.relpath(dname, start=source)
        dest_dname = join(dest, dest_dname)
        dest_dname = os.path.abspath(dest_dname)
        log('{} -> {}'.format(dname, dest_dname))
        for subdir in sub_dlist:
            dest_subdir = join(dest_dname, subdir)
            try:
                os.mkdir(dest_subdir)
            except FileExistsError:
                pass

        for fname in flist:
            source_fname = join(dname, fname)
            dest_fname = join(dest_dname, fname)
            log('{} -> {}'.format(source_fname, dest_fname))
            try:
                os.unlink(dest_fname)
            except FileNotFoundError:
                pass
            os.symlink(source_fname, dest_fname)

parser = argparse.ArgumentParser(description='Synchronize configuration files between machines')
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
parser.add_argument('-s', '--source', help='Location to copy files from. Defaults to the parent directory of this script.')
args = parser.parse_args()
VERBOSE = args.verbose

source = args.source
if source is None:
    source = os.path.dirname(os.path.realpath(__file__))
    source = os.path.abspath(join(source, os.pardir))

home_source = join(source, 'home')
if os.path.isdir(home_source):
    home_dest = os.path.expanduser('~')
    link_recursive(home_source, home_dest)
else:
    log('Skipping home. Could not find "{}".'.format(home_source))

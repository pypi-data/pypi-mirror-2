#!/usr/bin/env python

#+
#
# This file is part of quantities, a python package for handling physical
# quantities based on numpy.
#
# Copyright (C) 2009 Darren Dale
# http://packages.python.org/quantities
# License: BSD  (See doc/users/license.rst for full license)
#
# $Date$
#
#-

from __future__ import with_statement

import os
import sys

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

try:
    from setuptools import Command, setup
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import Command, setup

class constants(Command):

    description = "Convert the NIST databas of constants"

    user_options = []

    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        with file('quantities/constants/NIST_codata.txt') as f:
            data = f.read()
        data = data.split('\n')[10:-1]

        with file('quantities/constants/_codata.py', 'w') as f:
            f.write('# THIS FILE IS AUTOMATICALLY GENERATED\n')
            f.write('# ANY CHANGES MADE HERE WILL BE LOST\n\n')
            f.write('physical_constants = {}\n\n')
            for line in data:
                name = line[:55].rstrip().replace('mag.','magnetic')
                name = name.replace('mom.', 'moment')
                val = line[55:77].replace(' ','').replace('...','')
                prec = line[77:99].replace(' ','').replace('(exact)', '0')
                unit = line[99:].rstrip().replace(' ', '*').replace('^', '**')
                d = "{'value': %s, 'precision': %s, 'units': '%s'}"%(val, prec, unit)
                f.write("physical_constants['%s'] = %s\n"%(name, d))


cfg = ConfigParser()
cfg.read('setup.cfg')

with open('quantities/version.py') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line)
if __version__ != cfg.get('metadata', 'version'):
    with open('setup.cfg') as f:
        lines = f.readlines()
    with open('setup.cfg', 'w') as f:
        for line in lines:
            if line.startswith('version'):
                line = 'version = %s\n' % __version__
            f.write(line)

# Perform 2to3 if needed
local_path = os.path.dirname(os.path.abspath(sys.argv[0]))
src_path = local_path

if sys.version_info[0] == 3:
    src_path = os.path.join(local_path, 'build', 'py3k')
    import py3tool
    print("Converting to Python3 via 2to3...")
    py3tool.sync_2to3('quantities', os.path.join(src_path, 'quantities'))

try:
    old_path = os.getcwd()
    os.chdir(src_path)
    sys.path.insert(0, src_path)
    
    setup(
        author = cfg.get('metadata', 'author'),
        author_email = cfg.get('metadata', 'author_email'),
        classifiers = cfg.get('metadata', 'classifiers').split('\n'),
        cmdclass = {
            'constants' : constants,
        },
        description = cfg.get('metadata', 'description'),
        download_url = cfg.get('metadata', 'download_url'),
        keywords = cfg.get('metadata', 'keywords').split('\n'),
        license = cfg.get('metadata', 'license'),
        long_description = cfg.get('metadata', 'long_description'),
        name = cfg.get('metadata', 'name'),
        packages = [
            'quantities',
            'quantities.constants',
            'quantities.tests',
            'quantities.units',
        ],
        platforms = cfg.get('metadata', 'platforms'),
        requires = cfg.get('metadata', 'requires').split('\n'),
        test_suite = 'nose.collector',
        url = cfg.get('metadata', 'url'),
        version = cfg.get('metadata', 'version'),
        zip_safe = cfg.getboolean('metadata', 'zip_safe'),
    )
finally:
    del sys.path[0]
    os.chdir(old_path)

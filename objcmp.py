#!/usr/bin/env python -3
# -*- coding: utf-8 -*-
#
# Copyright 2010 K. Richard Pixley.
# See LICENSE for details.
#
# Time-stamp: <03-Jan-2011 17:21:27 PST by rich@noir.com>

"""
A covering script for :py:mod:`elffile`.  Compare object files.
"""

from __future__ import unicode_literals, print_function

__docformat__ = 'restructuredtext en'

import glob
import itertools
import optparse
import pprint
import sys

import elffile

if __name__ == '__main__':

    progname = sys.argv[0]
    u = ''
    u += 'usage: %prog objfile1 objfile2'

    parser = optparse.OptionParser(usage = u)

    options, args = parser.parse_args()

    assert len(args) == 2

    x = elffile.open(name=args[0])
    y = elffile.open(name=args[1])
    
    if x.close_enough(y):
        sys.exit()

    print('different')

    sys.exit(1)

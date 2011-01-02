#!/usr/bin/env python -3
# -*- coding: utf-8 -*-
#
# Copyright 2010 K. Richard Pixley.
# See LICENSE for details.
#
# Time-stamp: <02-Jan-2011 15:15:56 PST by rich@noir.com>

"""
A covering script for :py:mod:`elffile`.  Provides basic objdump ability.
"""

from __future__ import unicode_literals, print_function

__docformat__ = 'restructuredtext en'

import optparse

import elffile

if __name__ == '__main__':

    progname = sys.argv[0]
    u = ''
    u += 'usage: %prog objfile [objfile [objfile ...]]'

    parser = optparse.OptionParser(usage = u)

    options, args = parser.parse_args()

    for i in args:
        elffile.open(name=i).dump()

    sys.exit()

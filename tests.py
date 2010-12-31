#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 K. Richard Pixley.
# See LICENSE for details.
#
# Time-stamp: <30-Dec-2010 21:01:30 PST by rich@noir.com>

"""
Tests for elffile.
"""

from __future__ import unicode_literals, print_function

__docformat__ = 'restructuredtext en'

import nose
from nose.tools import assert_true, assert_false, assert_equal, assert_raises, raises

import glob
import sys
import os

import elffile

def testElfFileIdent():
    for filename in glob.glob(os.path.join('..', 'elf32-examples', '*')) + glob.glob(os.path.join('..', 'elf64-examples', '*')):
        with open(filename, 'rb') as f:
            content = f.read()

        efi = elffile.ElfFileIdent()
        efi.unpack(content)
        print(efi, file=sys.stderr)
        newcontent = bytearray(elffile.EI_NIDENT)
        efi.pack(newcontent)

        # if content != newcontent:
        #     print('len(content) = {0}, len(newcontent) = {1}'.format(len(content), len(newcontent)))

        #     for i in xrange(len(content)):
        #         if content[i] != newcontent[i]:
        #             print('differs at char {0}: {1} != {2}'.format(i, content[i], newcontent[i]))

        content.startswith(newcontent)

        efi2 = elffile.ElfFileIdent()
        efi2.unpack(str(newcontent))
        assert_equal(efi, efi2)

if __name__ == '__main__':
    nose.main()

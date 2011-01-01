#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 K. Richard Pixley.
# See LICENSE for details.
#
# Time-stamp: <31-Dec-2010 20:25:55 PST by rich@noir.com>

"""
Tests for elffile.

.. todo:: need to set up a distributable example files directory.
"""

from __future__ import unicode_literals, print_function

__docformat__ = 'restructuredtext en'

import nose
from nose.tools import assert_true, assert_false, assert_equal, assert_raises, raises

import glob
import sys
import os

import elffile

def testTestfiles():
    for filename in (glob.glob(os.path.join('testfiles', '*', '*.o'))
                     + glob.glob(os.path.join('testfiles', '*', '*', '*.o'))
                     + glob.glob(os.path.join('testfiles', '*', '*.so*'))
                     + glob.glob(os.path.join('testfiles', '*', '.libs', '*.so*'))
                     + glob.glob(os.path.join('testfiles', '*', 'hello'))):
        with open(filename, 'rb') as f:
            content = f.read()

        efi = elffile.ElfFileIdent()
        efi.unpack(content)

        if efi.magic != '\7fELF':
            continue

        print('{0}: {1}'.format(f.name, efi), file=sys.stderr)
        newcontent = bytearray(efi.size)
        efi.pack(newcontent)

        # if content != newcontent:
        #     print('len(content) = {0}, len(newcontent) = {1}'.format(len(content), len(newcontent)))

        #     for i in xrange(len(content)):
        #         if content[i] != newcontent[i]:
        #             print('differs at char {0}: {1} != {2}'.format(i, content[i], newcontent[i]))

        assert_true(content.startswith(newcontent))

        efi2 = elffile.ElfFileIdent()
        efi2.unpack(bytes(newcontent))
        assert_equal(efi, efi2)

        ef = elffile.ElfFile(f.name, efi)
        ef.unpack(content)

        newcontent = bytearray(ef.size)
        ef.pack(newcontent)

        assert_true(content.startswith(newcontent)) # FIXME: eventually need to compare equality

        ef2 = elffile.ElfFile(f.name, efi2)
        ef2.unpack(bytes(newcontent))
        assert_equal(ef, ef2)


def testFileEncoding():
    for i in elffile._fileEncodingDict:
        for j in elffile._fileEncodingDict[i]:
            ident = elffile.ElfFileIdent()
            ident.elfClass = i
            ident.elfData = j
            assert_equal(elffile._fileEncodingDict[i][j], elffile.ElfFile.encodedClass(ident))

@raises(elffile.ElfFile.NO_CLASS)
def testBogusClass():
    ident = elffile.ElfFileIdent()
    ident.elfClass = 254
    elffile.ElfFile.encodedClass(ident)

@raises(elffile.ElfFile.NO_ENCODING)
def testBogusEncoding():
    ident = elffile.ElfFileIdent()

    for ident.elfClass in elffile._fileEncodingDict:
        break

    ident.elfData = 254
    elffile.ElfFile.encodedClass(ident)


if __name__ == '__main__':
    nose.main()

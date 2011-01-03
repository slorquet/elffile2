#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 K. Richard Pixley.
# See LICENSE for details.
#
# Time-stamp: <02-Jan-2011 19:31:41 PST by rich@noir.com>

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
import mmap

import elffile

def testOpen():
    for filename in glob.glob(os.path.join('testfiles', '*', '*.o')):
        break

    byname = elffile.open(name=filename)

    with open(filename, 'rb') as fileobj:
        byfileobj = elffile.open(name=filename, fileobj=fileobj)

    with open(filename, 'rb') as fileobj:
        m = mmap.mmap(fileobj.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
        bymap = elffile.open(map=m)

        block = m[:]

    byblock = elffile.open(block=block)

    assert_equal(byname, byfileobj)
    assert_equal(byfileobj, bymap)
    assert_equal(bymap, byblock)


def testTestfiles():
    for filename in (glob.glob(os.path.join('testfiles', '*', '*.o'))
                     + glob.glob(os.path.join('testfiles', '*', '*', '*.o'))
                     + glob.glob(os.path.join('testfiles', '*', '*.so*'))
                     + glob.glob(os.path.join('testfiles', '*', '.libs', '*.so*'))
                     + glob.glob(os.path.join('testfiles', '*', 'hello'))):
        with open(filename, 'rb') as f:
            content = f.read()

        efi = elffile.ElfFileIdent()
        efi.unpack_from(content)

        if efi.magic != '\x7fELF':
            continue

        #print('{0}: {1}'.format(f.name, efi), file=sys.stderr)
        newcontent = bytearray(efi.size)
        efi.pack_into(newcontent)

        # if content != newcontent:
        #     print('len(content) = {0}, len(newcontent) = {1}'.format(len(content), len(newcontent)))

        #     for i in xrange(len(content)):
        #         if content[i] != newcontent[i]:
        #             print('differs at char {0}: {1} != {2}'.format(i, content[i], newcontent[i]))

        assert_true(content.startswith(newcontent))

        efi2 = elffile.ElfFileIdent()
        efi2.unpack_from(bytes(newcontent))
        assert_equal(efi, efi2)

        ef = elffile.ElfFile(filename, efi)
        ef.unpack_from(content)

        newcontent = bytearray(ef.size)
        ef.pack_into(newcontent)

        # FIXME: this is only true if we pack with the same order.  :\.  Maybe need 3 stage?
        #assert_true(content.startswith(newcontent)) # FIXME: eventually need to compare equality

        ef2 = elffile.ElfFile(filename, efi2)
        ef2.unpack_from(bytes(newcontent))
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

==================
 Reference Manual
==================

Overview
========

The beginning is :py:function:`open` which examines the beginning of
the file and returns an instance of :py:class:`ElfFile`.
:py:class:`ElfFile` isn't intended for direct instantiation so what's
actually returned is an instance of one of the subclasses.  There are
four - which represent all permutations of 32-bit, 64-bit, big-endian,
and little-endian.  This is their only difference.

Inheritance Diagram
===================

.. inheritance-diagram:: elffile

Reference
=========

.. automodule:: elffile
   :members:

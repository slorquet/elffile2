Welcome to elffile2!

This is a fork of the original elffile python library from rich.
This library is unmaintained and has bugs, and I had to use it.
So I have decided to fork it and fix it.

How to build from source

You need python-virtualenv

Then run:

    make clean
    make ve
    make bdist_egg

What follows is the original README.

--slorquet

.. Time-stamp: <03-Jan-2011 19:55:42 PST by rich@noir.com>

Welcome to elffile!

Elffile is a pure python implementation of a library which reads and
writes `ELF format object files
<http://en.wikipedia.org/wiki/Executable_and_Linkable_Format>`_

Current features:

* Elffile is pure `python <http://python.org>`_ so installation is
  easy.
* Elffile has been tested on python versions 2.[67] and 3.[012].
* Reads both 32 and 64 bit formats in both big and little endian
  order.
* Reads and writes file header, section header table, sections, and
  the section name string section.
* Reads program header table.

This is sufficient to compare two object files to determine if they
are equivalent aside from having been built at different times and in
different file system locations which was my initial goal.

--rich

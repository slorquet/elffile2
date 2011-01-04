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

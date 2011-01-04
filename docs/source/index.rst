.. elffile documentation master file, created by
   sphinx-quickstart on Mon Dec 27 12:59:17 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

***********************************
Welcome to elffile's documentation!
***********************************

Contents of this document:

.. toctree::
   :maxdepth: 2

   quickstart.rst
   reference.rst
   rationale.rst

Elffile is a library which reads and writes `ELF format object files
<http://en.wikipedia.org/wiki/Executable_and_Linkable_Format>`_.

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

Elffile comes with two scripts:

* objdump is the beginnings of an objdump utility.  It dumps in a
  python/s-expression sort of format so it's easy to traverse with
  emacs.

* objdmp is the beginnings of an object file comparison utility.

=====================================
 A Note on Supported Python Versions
=====================================

As I'm trying to straddle the 2 vs 3 jump, I'm relying on some of the
python-3 compatibility features from 2.6 and higher.  Supporting
earlier versions of python would be possible, but would make
supporting the python 2 vs 3 straddle somewhat more difficult.  I've
arbitrarily drawn my line in the sand at 2.6.

======
 TODO
======

.. todolist::

====================
 Indices and tables
====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

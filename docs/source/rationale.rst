===========
 Rationale
===========

If you need access to object files other than ELF format then you
probably want to look at the `GNU project <http://gnu.org>`_'s BFD
library which is distributed with `GDB
<http://www.gnu.org/software/gdb>`_ and the `binutils
<http://www.gnu.org/software/binutils>`_.  It is the only attempt at
producing a covering library for multiple object file formats of which
the author is aware.

.. note:: K Richard Pixley, the author of *elffile* was also one of
    the original authors of BFD.

As software architecture goes, it's not a very good design in the
sense that using BFD also requires an intimate understanding of the
BFD internals.  BFD based ports to new formats are typically difficult
and more time consuming than simple readers for those formats would
be. BFD doesn't cover or hide information in the way one might expect
from a traditional library but rather offers a sort of development
kit, a basis from which to write new formats.  The two primary reasons
to use BFD are:

* In support of a port of the GNU toolchain, that is, `GCC <http://www.gnu.org/software/gcc>`_,
  the `binutils <http://www.gnu.org/software/binutils>`_,
  and `GDB <http://www.gnu.org/software/gdb>`_.
* As a means of translating between multiple formats.

Luckily, most formats aside from ELF have now conveniently faded away
with the notable exception of `MACH-o
<http://en.wikipedia.org/wiki/Mach-O>`_ on `Mac Os X
<http://en.wikipedia.org/wiki/Mac_OS_X>`_, and some of the alternate
representatons like `S-Record format
<http://en.wikipedia.org/wiki/SREC_%28file_format%29>`_ which may
still be used on in-circuit emulators, logic analysers, and PROM
programmers.  This means that reading and writing ELF alone will solve
a majority of needs at a lighter weight than something as ambitious as
BFD.

Other python based ELF readers depend on the venerable libelf
interface which was originally distributed with `UNIX™ SysVr4
<http://en.wikipedia.org/wiki/System_V_Release_4>`_.  There are
several free implementations of this reference library available
including `one <http://wiki.freebsd.org/LibElf>`_ from `FreeBSD
<http://www.freebsd.org>`_, `a very popular implementation by Michael
Riepe <http://www.mr511.de/software/english.html>`_, and one that
accompanies the `Fedora <http://fedoraproject.org>`_ hosted `elfutils
<https://fedorahosted.org/elfutils>`_.

The primary benefit for using a reference library of this sort is that
changes to the underlying format can happen at the libelf level and be
hidden from upper level applications.  However, the elf format has
been quite stable over the last 15 years or so and has largely
replaced all other formats for both UNIX™ and UNIX-like operating
system families, (Linux, BSD), as well as most cross development
systems hosted on these systems.  When changes have occurred they have
primarily been as extensions to the format for new processors, new
operating systems, and new facilities, each of which require
concomitant changes in higher level code as well.

The requirement for libelf isn't particularly difficult to address but
using it in a python library requires writing a python extension for
the libelf-to-python interface.  This makes configuration and
installation somewhat more difficult for python users.  In particular,
I wasn't able to get any of the available python and libelf based
readers to work on any handy system within a few hours.

More, the paradigm presented by libelf isn't exactly "pythonic".  Most
python based applications are likely to use a different internal
format anyway so the utility of using libelf becomes questionable.

Your author also posits that the python extention necessary to
interface with any libelf impementation, (much less one which can work
with multiple installations), is more work to create and maintain than
a pure python library which simply reads elf format itself.  That's
the gamble he's making by writing this library.

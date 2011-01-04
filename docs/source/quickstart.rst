===========
Quick Start
===========

Files can be read using any of several different forms::

    # by name
    import elffile
    f = elffile.open(name='foo.o')

    # by file object
    import io
    f = io.open('foo.o', 'rb')
    e = elffile.open(fileobj=f)

    # by mmap object
    import mmap
    m = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
    d = elffile.open(map=m)

    # of as a block of memory
    b = mmap[:]
    c = elffile.open(block=b)

Once opened, you can compare two files for equality using::

    x == y

but since most files have embedded time stamps and file system
locations, you may want a weaker comparison::

    x.close_enough(y)

You can copy a file to a new chunk of memory using::

    block = x.pack()

Or write to a new file using::

    with open('new.o', 'rb') as f:
        f.write(x.pack())

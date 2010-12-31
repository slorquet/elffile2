# This file is in the public domain.

bin_PROGRAMS = hello
hello_SOURCES = hello.c
hello_LDADD = libstatic.la libdynamic.la

lib_LTLIBRARIES = libstatic.la libdynamic.la
libstatic_la_SOURCES = a.c b.c c.c
libstatic_LIBTOOLFLAGS = -static
libdynamic_la_SOURCES = d.c e.c f.c
libdynamic_LIBTOOLFLAGS = -dynamic

add:; hg add `find . -name \*.[oa] -o -name \*.so\* -o -name hello`

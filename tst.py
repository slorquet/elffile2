import yaml
import elffile
import sys
import glob
import os
import itertools

def filelist(which):
    for f in glob.iglob(os.path.join('testfiles', which, '.libs', 'hello')):
        yield f

    for f in glob.iglob(os.path.join('testfiles', which, '.libs', '*.so*')):
        yield f

    for f in glob.iglob(os.path.join('testfiles', which, '.libs', '*.o')):
        yield f

    for f in glob.iglob(os.path.join('testfiles', which, '*.o')):
        yield f

for xname, yname in itertools.izip(filelist('one'), filelist('two')):

    x = elffile.open(name=xname)
    y = elffile.open(name=yname)

    print('{0}: {1}'.format(xname, x.close_enough(y)))


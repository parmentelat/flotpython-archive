#! /usr/bin/env python

"""
a utility to estimate the size of a whole filesystem tree
this runs in 2 passes 
pass1: save the result in each directory in a .du file
pass2: an interactive tool for navigating the tree
       and spotting the files to be cleaned up
"""

import os, os.path
from operator import add

# ongoing work..
def pass1 (path):
    for root, dirs, files in os.walk (path):
        filepaths = [ os.path.join(root,file) for file in files ]
        size_for_files = reduce (add, [ os.path.getsize(filepath) 
                                        for filepath in filepaths 
                                        if os.path.exists(filepath) ], 0 )
        print "directory %s holds %s bytes in files"%(root,size_for_files)


# xxx will use argparse of course ultimately
import sys
pass1 (sys.argv[1])

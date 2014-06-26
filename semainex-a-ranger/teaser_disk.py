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

# 2**10 = 1024 = 1 kilo
POWER2_SYMBOLS = [ ( 40, 'T'), ( 30, 'G'), ( 20, 'M'), ( 10, 'k'), (0, 'b') ]
# compute 2**p
UNIT_SYMBOLS = [ ( 2**p, s) for (p, s) in POWER2_SYMBOLS ]

def repr (bytes):
    for ( unit, symbol ) in UNIT_SYMBOLS:
        if bytes >= unit:
            return "%s%s"%(bytes/unit,symbol)
    return "???"

def pass1 (path):
    # first deal with files, stores local total in a has
    local_size_by_dir = {}
    cumulated_size_by_dir = {}
    for root, dirs, files in os.walk (path, topdown=False):
        filepaths = [ os.path.join(root,file) for file in files ]
        local_size = reduce (add, [ os.path.getsize(filepath) 
                                    for filepath in filepaths 
                                    if os.path.exists(filepath) ], 0 )
        # count the directory itself
        local_size += os.path.getsize (root)
        local_size_by_dir [ root ] = local_size
        def subdir_size (subdir):
            path=os.path.join(root,subdir)
            return cumulated_size_by_dir.get(path,0) 
        cumulated_size = reduce (add, [ subdir_size (subdir) for subdir in dirs ], 0)
        cumulated_size += local_size
        cumulated_size_by_dir [ root ] = cumulated_size
        
#        print "%-8s %s"%(repr(cumulated_size),root)

# xxx will use argparse of course ultimately
import sys
pass1 (sys.argv[1])

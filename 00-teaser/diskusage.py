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

###
def pass1 (path):
    # first deal with files, stores local total in a has
    cumulated_size_by_dir = {}
    for root, dirs, files in os.walk (path, topdown=False):
        filepaths = [ os.path.join(root,file) for file in files ]
        local_size = reduce (add, [ os.path.getsize(filepath) 
                                    for filepath in filepaths 
                                    if os.path.exists(filepath) ], 0 )
        # count the directory itself
        local_size += os.path.getsize (root)
        def subdir_size (subdir):
            path=os.path.join(root,subdir)
            return cumulated_size_by_dir.get(path,0) 
        cumulated_size = reduce (add, [ subdir_size (subdir) for subdir in dirs ], 0)
        cumulated_size += local_size
        cumulated_size_by_dir [ root ] = cumulated_size
        with open(os.path.join(root,".du"),'w') as store:
            store.write("%s\n"%cumulated_size)
#        print "%-8s %s"%(repr(cumulated_size),root)
    return cumulated_size_by_dir

###
def get_size (path, cache):
    if cache.has_key(path): 
        return cache[path]
    else: 
        try: 
            with open(os.path.join(path,".du")) as f:
                return int(f.read())
        except: 
            return 0

def show_path (path,cache):
    print "Total size %s for path %s"%(repr(get_size(path,cache)),path)
    subdirs=[ (d,os.path.join(path,d)) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d)) ]
    sized_subdirs = [ (name, subdir, get_size(subdir,cache)) for (name,subdir) in subdirs ]
    # show biggest last
    def sort_sized_subdirs (t1,t2):
        (_,_,s1)=t1; (_,_,s2)=t2; return s1-s2
    sized_subdirs.sort(sort_sized_subdirs)
    counter=1
    for name,path,size in sized_subdirs:
        print "%s %s %s"%(counter,name,repr(size))
        counter +=1
    while True:
        string=raw_input("Enter number (or l(ast) or u(p)) ")
#        import pdb
#        pdb.set_trace()
        try: return sized_subdirs[int(string)-1][1]
        except: pass
        try: 
            if string.strip() in ['l']: return sized_subdirs[-1][1]
        except: pass
        print 'path',path,'res',os.path.dirname(path)
        if string.strip() in ['..','0','u']:
            return os.path.dirname(path)
        
def pass2 (path, cache):
    while True:
        path=show_path (path, cache)

# xxx will use argparse of course ultimately
import sys
cache=pass1 (sys.argv[1])
pass2 (sys.argv[1],cache)

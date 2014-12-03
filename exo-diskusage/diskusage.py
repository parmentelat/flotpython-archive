#! /usr/bin/env python

from __future__ import print_function

"""
diskusage: a utility to estimate the size of a whole filesystem tree
this runs in 2 passes 

pass1: save the total size in each directory in a .du file

pass2: an interactive tool for navigating the tree
       and spotting the files to be cleaned up
"""

import os, os.path
from argparse import ArgumentParser

# 2**10 = 1024 = 1 kilo
POWER2_SYMBOLS = [ ( 40, 'T'), ( 30, 'G'), ( 20, 'M'), ( 10, 'k'), (0, 'b') ]
# compute 2**p
UNIT_SYMBOLS = [ ( 2**p, s) for (p, s) in POWER2_SYMBOLS ]

# how to display a raw byte count nicely like 2G or 4M or 6k
def repr (bytes):
    for ( unit, symbol ) in UNIT_SYMBOLS:
        if bytes >= unit:
            return "%s%s"%(bytes/unit,symbol)
    return "???"

###
def pass1 (path):
    cumulated_size_by_dir = {}
    for root, dirs, files in os.walk (path, topdown=False):
        # first deal with files
        filepaths = [ os.path.join(root,file) for file in files ]
        local_size = sum ([ os.path.getsize(filepath) 
                            for filepath in filepaths 
                            if os.path.exists(filepath) ])
        # count the directory itself
        local_size += os.path.getsize(root)
        # because we do the traversal bottom up, we already have the size for our immediate sons
        # in cumulated_size_by_dir; however the disk is alive during this time so it might be
        # that a new son is showing up that we do not know about
        def subdir_size (subdir):
            path=os.path.join(root,subdir)
            # in which case we return 0 and not some exception
            return cumulated_size_by_dir.get(path,0) 
        # total on the immediate sons
        cumulated_size = sum ([ subdir_size (subdir) for subdir in dirs ])
        # add the local weight (files + this_dir)
        cumulated_size += local_size
        # store in dictionary for dealing with the upper directory
        cumulated_size_by_dir [ root ] = cumulated_size
        # store result in <dir>/.du for second/interactive pass
        with open(os.path.join(root,".du"),'w') as store:
            store.write("%s\n"%cumulated_size)
#        print("%-8s %s"%(repr(cumulated_size),root))
    return cumulated_size_by_dir

###
# we have a global cache object, that is a dict { dirname -> size }
# at the beginning it is empty, and we fill it as we go
# if the size is not known from the cache we look in <dir>/.du
# if it's still not known we return 0
def get_size (path, cache):
    if cache.has_key(path): 
        return cache[path]
    else: 
        try: 
            with open(os.path.join(path,".du")) as f:
                return int(f.read())
        except: 
            return 0

# during pass2, when inspecting a directory we show the immediate subdirs (with numbers for selection) 
# they are sorted so that the bigger one comes last (and can thus be selected using 'l')
def show_path (path,cache):
    print("Total size %s for path %s"%(repr(get_size(path,cache)),path))
    subdirs=[ (d,os.path.join(path,d)) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d)) ]
    sized_subdirs = [ (name, subdir, get_size(subdir,cache)) for (name,subdir) in subdirs ]
    # show biggest last
    def sort_sized_subdirs (t1,t2):
        (_,_,s1)=t1; (_,_,s2)=t2; return s1-s2
    sized_subdirs.sort(sort_sized_subdirs)
    counter=1
    for name,path,size in sized_subdirs:
        print("%s %s %s"%(counter,name,repr(size)))
        counter +=1
    # the interactive mainloop for selecting the next dir
    while True:
        string=raw_input("Enter number (or l(ast) or u(p)) or (q)uit ")
        # englobe in try/except as the input might not be an int or make no sense
        try: return sized_subdirs[int(string)-1][1]
        except: pass
        # again try/except for if subdirs is empty
        try: 
            if string.strip() in ['l']: return sized_subdirs[-1][1]
        except: pass
        # how to step up 
        if string.strip() in ['..','0','u']:
            return os.path.dirname(path)
        # xxx would make sense to accept strings as well here...
        if string.strip() in ['q','Q']:
            exit(0)

# well, that's it mostly
def pass2 (path, cache):
    while True:
        path=show_path (path, cache)

def main():
    parser = ArgumentParser()
    parser.add_argument("dirs", nargs='+')
    # by default we only run a pass2
    parser.add_argument("-1", "--pass1", dest='pass1', default=False,
                        action='store_true',
                        help="Run pass1, that computes .du in all subdirs")
    parser.add_argument("-a", "--all-passes", dest='all_passes', default=False,
                        action='store_true',
                        help="""Run pass1, that computes .du in all subdirs,
                                and then pass2 that is interactive""")

    args = parser.parse_args()
    if args.all_passes:
        run_pass1 = True; run_pass2 = True
    elif args.pass1:
        run_pass1 = True; run_pass2 = False
    else:
        run_pass1 = False; run_pass2 = True

    try:
        for dir in args.dirs:
            cache = pass1(dir) if run_pass1 else {}
            run_pass2 and pass2(dir, cache)
        return 0
    except Exception as e:
        print('Something went wrong', e)
        return 1
        
if __name__ == '__main__':
    exit(main())

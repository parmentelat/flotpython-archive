#! /usr/bin/env python

# for python3
from __future__ import print_function

try:    raw_input
except: raw_input = input

import os, os.path
from argparse import ArgumentParser


########################################
"""
diskusage: a utility to estimate the size of a whole filesystem tree

this runs in 2 passes 

pass1: save the total size in each directory in a .du file

pass2: an interactive tool for navigating the tree
       and spotting the files to be cleaned up
"""

########## helper class
# int goes to 2**64 i.e. 16 10*18
# which should abe ample enough
# using long would ruin the python3 version

class HumanReadableSize(int):
    """
    helper class for displaying size in bytes 
    in a human-readable form
    """

    # http://en.wikipedia.org/wiki/Petabyte
    ### the unit to use for a size in 2**n
    # 2**10 = 1024 = 1 kilo
    LABELS = [ (6, 'EiB'), (5, 'PiB'), ( 4, 'TiB'),
               ( 3, 'GiB'), ( 2, 'MiB'), ( 1, 'KiB'),
               (0, 'B') ]
    # compute 2**(10.n)
    UNIT_LABELS = [ (2**(10*n), s) for (n, s) in LABELS ]

    # could use some more precision (like 2 digits or so)
    def __repr__ (self):
        for ( unit, label ) in self.UNIT_LABELS:
            if self >= unit:
                # small values usually show an int
                if self%unit == 0:
                    return "{:3d} {}".format(self/unit,label)
                else:
                    return "{:3.02f} {}".format(float(self)/unit,label)
        return "???"

    # we have seen that __repr__ is used when __str__ is not defined
    # but in our case since we inherit int, __str__ does get found
    # so let's make it explicit that we want to use our own __repr__
    # for printing too
    __str__ = __repr__


class DiskWalker(object):
    """
    pass1 object
    could as well have been a simple function 
    """

    def __init__(self, path):
        self.path = path

    def pass1(self):
        """
        scans a whole tree, and returns 
        a dictionary { path : size }
        that can be used as a cache if pass2 runs in the same process
        """        
        cumulated_size_by_dir = {}
        for root, dirs, files in os.walk (self.path, topdown=False):
            # first deal with files
            filepaths = [os.path.join(root,file) for file in files]
            local_size = sum ([os.path.getsize(filepath) 
                                   for filepath in filepaths 
                                       if os.path.exists(filepath) ])
            # count the directory itself
            local_size += os.path.getsize(root)
            # because we do the traversal bottom up, we already have the size for our immediate sons
            # in cumulated_size_by_dir; however the disk is alive during this time so it might be
            # that a new son is showing up that we do not know about
            def subdir_size (subdir):
                subpath = os.path.join(root, subdir)
                # in which case we return 0 and not some exception
                return cumulated_size_by_dir.get(subpath, 0) 
            # total on the immediate sons
            cumulated_size = sum ([ subdir_size (subdir) for subdir in dirs ])
            # add the local weight (files + this_dir)
            cumulated_size += local_size
            # store in dictionary for dealing with the upper directory
            cumulated_size_by_dir [root] = cumulated_size
            # store result in <dir>/.du for second/interactive pass
            try:
                with open(os.path.join(root, ".du"), 'w') as store:
                    store.write("{}\n".format(cumulated_size))
            except IOError as e:
                # write error - permission denied - don't cache it then
                # xxx log this in verbose mode
                pass
            # log this in verbose mode
#            print("{:-8s} {}".format(HumanReadableSize(cumulated_size),root))
        return cumulated_size_by_dir

###
# we have a global cache object, that is a dict { dirname -> size }
# at the beginning it is empty, and we fill it as we go
# if the size is not known from the cache we look in <dir>/.du
# if it's still not known we return 0
def get_size (path, cache):
    if path in cache: 
        return cache[path]
    else: 
        try: 
            with open(os.path.join(path,".du")) as f:
                return int(f.read())
        except: 
            return 0

def help():
    print("""number\tgo to listed directory
+\tgo to last (and thus biggest) directory - this is the default 
u\tgo one step up - can be also '0' or '..'
q\tquit
h\tthis help
xxx to be completed...""")

        # during pass2, when inspecting a directory we show the immediate subdirs (with numbers for selection) 
# they are sorted so that the bigger one comes last (and can thus be selected using 'l')
def navigate_path (path,cache):
    print(8*'-', "Path {} has a total size of {}".format(path, HumanReadableSize(get_size(path,cache))))
    subdirs=[ (d,os.path.join(path,d)) for d in os.listdir(path) if os.path.isdir(os.path.join(path,d)) ]
    sized_subdirs = [ (name, subdir, get_size(subdir,cache)) for (name,subdir) in subdirs ]
    # show biggest last
    def sort_sized_subdirs (t1,t2):
        (_,_,s1)=t1; (_,_,s2)=t2; return s1-s2
    sized_subdirs.sort(key=lambda t: t[2])
    counter=1
    for name,path,size in sized_subdirs:
        print("{} {} {}".format(counter,name,HumanReadableSize(size)))
        counter +=1
    # the interactive mainloop for selecting the next dir
    while True:
        # '+' is the default
        answer = raw_input("Enter number (h for help) ") or '+'
        answer = answer.strip().lower()

        ### does this look like a number
        index = None
        if answer in ['+']:
            index = -1
        else:
            try:    index = int(answer)-1
            except: pass

        ### if so
        if index:
            try:
                _, path, _ = sized_subdirs[index]
                return path
            except:
                print ("No such index {}".format(answer))
        ### otherwise
        elif answer in ['..','0','u']:
            return os.path.dirname(path)
        # xxx would make sense to accept answers as well here...
        elif answer in ['q']:
            exit(0)
        elif answer in ['h']:
            help()
        else:
            print("command not understood")

# well, that's it mostly
def pass2 (path, cache):
    print ("Welcome to inspection of path {}".format(path))
    while True:
        path = navigate_path (path, cache)

def main():
    parser = ArgumentParser()
    # by default we only run a pass2
    parser.add_argument("-1", "--pass1", dest='pass1', default=False,
                        action='store_true',
                        help="Run pass1, that computes .du in all subdirs")
    parser.add_argument("-a", "--all-passes", dest='all_passes', default=False,
                        action='store_true',
                        help="""Run pass1, that computes .du in all subdirs,
                                and then pass2 that is interactive""")
    parser.add_argument("-v", "--verbose", dest='verbose', default=False,
                        action='store_true',
                        help="turn on verbose output")

    parser.add_argument("dir")

    args = parser.parse_args()
    if args.all_passes:
        run_pass1 = True; run_pass2 = True
    elif args.pass1:
        run_pass1 = True; run_pass2 = False
    else:
        run_pass1 = False; run_pass2 = True

    try:
        # initialize cache, either from pass1, or from scratch
        cache = DiskWalker(args.dir).pass1() if run_pass1 else {}
        run_pass2 and pass2(args.dir, cache)
        return 0
    except Exception as e:
        print('Something went wrong', e)
        import traceback
        traceback.print_exc()
        return 1
        
if __name__ == '__main__':
    exit(main())

#!/usr/bin/env python

import glob
from argparse import ArgumentParser

def prefixer_commentaire (in_filename):
    out_filename=in_filename.replace('.py','.comment.py')
    try:
        with open(out_filename,'w') as output:
            with open(in_filename) as input:
                for line in input.readlines():
                    output.write('#'+line)
        print '(over)wrote %s'%out_filename
        return True
    except Exception,e:
        print 'failed to deal with in_filename, %s'%e
        return False
    
def traiter_fichiers (filenames):
    results = [ prefixer_commentaire (filename) for filename in filenames ]
    failures = [ r for r in results if r is False ]
    return len(failures)==0

def main ():
    parser=ArgumentParser()
    parser.add_argument ('filenames',metavar='file',type=str,nargs='*',
                        help='input files to be commented')
    args=parser.parse_args()
    
    # sans argument on travaille sur */*.py
    filenames=args.filenames
    if not filenames:
        filenames=glob.glob('*/*.py')
    if not filenames:
        parser.print_help()
        exit(1)
    exit ( 0 if traiter_fichiers (filenames) else 1)

if __name__ == '__main__':
    main()

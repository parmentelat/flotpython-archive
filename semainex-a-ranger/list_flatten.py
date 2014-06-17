#!/usr/bin/env python

inputs=[]
inputs.append ( [ 'a', 'b', 'c' ] )
inputs.append ( xrange(4) )
inputs.append ( [ 1, 2, [3, [4, [5, 6] ,7] ,8], 9] )

def list_flatten (list_of_lists):
    result=[]
    for l in list_of_lists:
        if isinstance (l,list):
            result += list_flatten (l)
        else:
            result.append(l)
    return result

def main ():
    for input in inputs:
        print 20*'=','input:', input
        print 'iterative:', list_flatten (input)

if __name__ == '__main__': main()
